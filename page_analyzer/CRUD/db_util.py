import psycopg2
import os
from dotenv import load_dotenv

def get_connection():
    try:
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        port = os.getenv('PORT')
        database_name = os.getenv('DBNAME')
        connection = psycopg2.connect(f'postgresql://{user}:{password}@{host}:{port}/{database_name}')
    except (Exception) as error:
        print(error)

    return connection
