import psycopg2
import json

host = '127.0.0.1'
user = 'postgres'
password = '****'
db_name = 'aggregator'
port = 5432

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM Users;'
        )

        print(cursor.fetchall())

except Exception as _ex:
    print('error')
finally:
    if connection:
        connection.close()
        print('closed')