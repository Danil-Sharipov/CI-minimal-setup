import boto3
from tqdm import tqdm
# Инициализация клиента S3
ackey,seckey = input().split()
s3_client = boto3.client('s3',
                         endpoint_url='http://minio.com',
                         aws_access_key_id=ackey,
                         aws_secret_access_key=seckey)

# Создание бакета
bucket_name = 'my-test-bucket'
try:
    s3_client.create_bucket(Bucket=bucket_name)
except Exception:
    pass

# Загрузка файла в бакет
s3_client.upload_file('file.txt', bucket_name, 'txt.txt')