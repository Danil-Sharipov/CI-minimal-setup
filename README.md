# MLOps
Развертки ML-стэнда для CI. Стэк:
- k3s
- Airflow
- Mlflow
- Minio
- Postgresql

## Установка collections
```bash
ansible-galaxy install -r collections/requirements.yml 
```
## Развертка стэнда
```bash
ansible-playbook main.yml
```
Доступ к UI AIRFLOW: https://192.168.56.10/
## Настройка
- ### Настройка соединения с minio s3.
Для простоты воспользуемся UI AIRFLOW:
![alt text](./screenshots/1.png)
![alt text](./screenshots/2.png)
- ### Работа с minio api 
- ### ~~Дописать~~
## Мониторинг
## Тестирование
