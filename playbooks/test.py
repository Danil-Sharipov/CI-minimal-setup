import psycopg2

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='mlflow', user='mlflow', password='mlflow', host='192.168.56.12')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')