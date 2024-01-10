# MLOps
Развертки ML-стэнда для CI. Стэк:
- k3s
- Airflow
- Mlflow
- Minio
- Postgresql

## Установка collections

Установка необходимых коллекций производится с помощью команды:

```bash
ansible-galaxy install -r collections/requirements.yml 
```
## Развертка стэнда

Развернем стэнд с помощью команды:

```bash
ansible-playbook main.yml
```

Доступ к UI AIRFLOW: https://192.168.56.10/. 
## Добавить buckets

Стоит отметить, что создается автоматически только один bucket в minio, но это можно исправить двумя способами:
- Отредактировать **roles/minio/templates/values.yaml**
```yaml
tenant:
buckets:
- name: {{ defaultBuckets }}
- name: #ADD_NAME
```
- Использовать **make_bucket** в minio api
```python
client = Minio("minio:9000", 
access_key=MINIO_ROOT_USER,
secret_key=MINIO_ROOT_PASSWORD,
secure=False)

# Make MINIO_BUCKET_NAME if not exist.
found = client.bucket_exists(MINIO_BUCKET_NAME)
if not found:
client.make_bucket(MINIO_BUCKET_NAME)
else:
print(f"Bucket '{MINIO_BUCKET_NAME}' already exists!")
```
## Свой образ для airflow

Для установки дополнительных библиотек или редактирования образа можно отредактировать **Dockerfiles/airflow/Dockerfile**:
```dockerfile
FROM apache/airflow

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt
```
Предварительно необходимо удалить (если запускали основной playbook) **roles/airflow/files/airflow.tar**.
## Настройка соединения с minio s3.

Для простоты воспользуемся UI AIRFLOW:

![alt text](screenshots/1.png)
![alt text](screenshots/2.png)
## Подключенные dags

Написанные DAG'и Gitsync загружает их из GitHub в каждый POD airflow - web server, scheduler и worker. Отредактировать репозиторий, branch и папку можно в файле:
##### **roles/airflow/templates/values.yaml**
```yaml
dags:
gitSync:
enabled: true
repo: https://github.com/Danil-Sharipov/First_in_MLOps.git
branch: main
subPath: "dags"
```
## Переменные db & minio

Переменные minio можно найти в файле:
##### **group_vars/k3s_nodes.yaml**
```yaml
MINIO_BUCKET_NAME: airflow-bucket
MINIO_SECOND_BUCKET_NAME: mlflow-bucket
MINIO_ROOT_USER: CxrzoH4Ye0Cgiwm1znpp
MINIO_ROOT_PASSWORD: frASzoho4X76UbqWSIw7GHuTbQ5fmKT2sv3Qftml
```

Здесь же лежит ip k3s-server и токен для подключения агентов:
```yaml
host_master: 192.168.56.10
token: 'my_token'
```

Переменные db можно найти в файле:
##### **group_vars/all_nodes.yaml**
```yaml
db_user: flow
db_password: flow
db_name: mlflow
db_name2: airflow
host_db: 192.168.56.12
```
