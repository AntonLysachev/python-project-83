from psycopg2 import extras
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection(database_url) -> psycopg2.connect:
    connection = psycopg2.connect(database_url)
    return connection


def get_url_by_id(url_id: str) -> tuple:
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        return cursor.fetchone()


def get_url_by_name(name: str, order_by: str = "ASC") -> tuple:
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE name = %s', (name,))
        return cursor.fetchone()


def get_url_checks_by_id(url_id: str) -> list:
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute(
            'SELECT * FROM url_checks WHERE url_id = %s ORDER BY "id" DESC', (url_id,)
        )
        data = cursor.fetchall()
        if data:
            return data


def get_urls_with_last_check() -> list:
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute("SELECT id, name FROM urls ORDER BY id  DESC")
        urls = cursor.fetchall()
        cursor.execute(
            """SELECT url_id, status_code, max(created_at)as created_at
                    FROM url_checks
                    GROUP BY url_id, status_code"""
        )
        url_checks = cursor.fetchall()

        url_checks_dict = {
            data["url_id"]: {
                "status_code": data["status_code"],
                "created_at": data["created_at"],
            }
            for data in url_checks
        }

        records = []

        for data in urls:
            id = data["id"]
            check_data = url_checks_dict.get(id, {})
            records.append(
                {'id': data["id"],
                 'name': data['name'],
                 'status_code': check_data.get('status_code', ''),
                 'created_at': check_data.get('created_at', '')
                 }
            )

    return records


def add_url(url: str):
    with get_connection(DATABASE_URL) as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,))
        connection.commit()
        inserted_id = cursor.fetchone()
        return inserted_id[0]


def add_info_url(url_id: str, status_code: str, h1: str, title: str, description: str):
    with get_connection(DATABASE_URL) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
        INSERT INTO url_checks (
            url_id,
            status_code,
            h1,
            title,
            description)
        VALUES (%s, %s, %s, %s, %s)
        """,
            (
                url_id,
                status_code,
                h1,
                title,
                description,
            ),
        )
        connection.commit()
