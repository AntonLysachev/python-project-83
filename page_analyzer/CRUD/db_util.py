import psycopg2
import os

def get_connection() -> psycopg2.connect:
    try:
        database_url = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(database_url)
    except (Exception) as error:
        print(error)
    return connection
