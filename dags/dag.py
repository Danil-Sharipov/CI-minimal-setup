import pandas as pd
from datetime import datetime, timedelta
from airflow.decorators import dag, task
@task
def get_data():
   from minio import Minio

   access_key =  os.getenv("MINIO_ROOT_USER")
   secret_key = os.getenv("MINIO_ROOT_PASSWORD")
   bucket = os.getenv("MINIO_SECOND_BUCKET_NAME")
   minio = "minio.com"
   
   
   client = Minio(minio, access_key=access_key, secret_key=secret_key, secure=False)
   
   objects = client.list_objects(bucket)
   df = None
   for i in objects:
      obj = client.get_object(
         bucket,
         i._object_name)
      minio.remove_object(bucket,
                          i._object_name)
      temp = pd.read_csv(obj)
      if df is None:
         df = temp
         continue
      df = pd.concat([df,temp]).drop_duplicates().reset_index(drop=True)
   return df
@task
def transform_data(df):
   df['end'] = pd.to_datetime(df['end'],format='%Y-%m-%d %H:%M:%S')
   df.set_index('end',inplace=True)
   df = df.resample('D').mean().interpolate().reset_index()
   df_new = None
   for i in df.columns[:-2]:
      if df_new is None:
         df_new = df[[i,'end']]
         df_new['ident'] = i
         df_new['target'] = df[i]
         df_new.drop(columns=[i],inplace=True)
         continue
      df_temp = df[[i,'end']]
      df_temp['ident'] = i
      df_temp['target'] = df[i]
      df_temp.drop(columns=[i],inplace=True)
      df_new = pd.concat([df_new,df_temp])
   return df_new.dropna().sort_values('end')
@task
def model(time):
   from requests import post
   time = time.to_dict(orient="index")
   
   post('http://ml.com/add',json=time)
@dag(
   schedule="@daily",
   start_date=datetime.datetime(2024, 1, 1, 23, 59),
   catchup=False,
   tags=["YNDX", "ML"],
)
def ML():
   model(transform_data(get_data()))