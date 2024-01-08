import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from airflow.decorators import dag, task
import os

def request(today,base):
    response = requests.get(f'{base}?from={today}')
    response = json.loads(response.content)['candles']
    data = response["data"]
    return data

def column(base):
    response = requests.get(f'{base}?from=2024-01-01')
    response = json.loads(response.content)['candles']
    return response['columns']

@task
def make_csv(today):
    base = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities/YNDX/candles.json'
    data = request(today,base)
    if len(data) == 0:
        return
    columns = column(base)
    df = pd.DataFrame(data = data, columns = columns)
    csv = df.to_csv(index=False).encode("utf-8")
    return csv

@task
def dump_data_to_bucket(csv):

    if csv is None:
        return

    from minio import Minio
    from io import BytesIO

    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")

    client = Minio("minio.com", access_key=MINIO_ROOT_USER, secret_key=MINIO_ROOT_PASSWORD, secure=False)

    client.put_object(
        MINIO_BUCKET_NAME, f"{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}_yandex.csv", data=BytesIO(csv), length=len(csv), content_type="application/csv"
    )

@dag(
    schedule="@daily",
    start_date=datetime.datetime(2024, 1, 1, 23, 59),
    catchup=False,
    tags=["YNDX", "etl"],
)
def YNDX_etl():
    today = datetime.today().strftime('%Y-%m-%d')
    dump_data_to_bucket(make_csv(today))

YNDX_etl()
# отредактировать shedule 23:59 каждый день
