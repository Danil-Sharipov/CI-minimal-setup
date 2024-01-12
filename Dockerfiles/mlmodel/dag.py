import pandas as pd

def get_data():
   from minio import Minio

   access_key = "airflow"
   secret_key = 'airflowpass'
   bucket = "mlflow"
   
   
   client = Minio("127.0.0.1:9000", access_key=access_key, secret_key=secret_key, secure=False)
   
   objects = client.list_objects(bucket)
   df = None
   for i in objects:
      obj = client.get_object(
         bucket,
         f"{i._object_name}",
      )
      temp = pd.read_csv(obj)
      if df is None:
         df = temp
         continue
      df = pd.concat([df,temp]).drop_duplicates().reset_index(drop=True)
   return df

def transform_data(time):
   
   # изменить обработку
   time = time[['end','close']]
   time.dropna(inplace=True)
   return time

def model(time):
   from requests import post
   time = time.to_dict(orient="index")
   
   post('http://127.0.0.1:5000/add',json=time)
model(transform_data(get_data()))