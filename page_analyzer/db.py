from psycopg2 import sql, extras
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection(database_url) -> psycopg2.connect:
    connection = psycopg2.connect(database_url)
    return connection


def get_url_by_id(value: str) -> tuple:
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE id = %s', (value,))
        return cursor.fetchone()


def get_url_by_name(value: str, order_by: str = "ASC") -> tuple:
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE name = %s', (value,))
        return cursor.fetchone()


def get_url(value: str) -> list:
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute(
            'SELECT * FROM url_checks WHERE url_id = %s ORDER BY "id" DESC', (value,)
        )
        data = cursor.fetchall()
        if data:
            return data


def get_urls_with_last_check() -> list:
    list_urls = []
    with get_connection(DATABASE_URL).cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute("SELECT id, name FROM urls ORDER BY id  DESC")
        urls = cursor.fetchall()
        cursor.execute(
            """SELECT url_id, status_code, max(created_at)as created_at
                    FROM url_checks
                    GROUP BY url_id, status_code
                    ORDER BY url_id  DESC"""
        )
        url_checks = cursor.fetchall()
        urls_dict = [{"id": data["id"], "name": data["name"]} for data in urls]

        url_checks_dict = {
            data["url_id"]: {
                "status_code": data["status_code"],
                "created_at": data["created_at"],
            }
            for data in url_checks
        }

        for data in urls_dict:
            id = data["id"]
            data["status_code"] = ""
            data["create_at"] = ""
            if id in url_checks_dict:
                data["status_code"] = url_checks_dict[id]["status_code"]
                data["created_at"] = url_checks_dict[id]["created_at"]
            list_urls.append(data)

    return list_urls


def save_url(url: str):
    with get_connection(DATABASE_URL) as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,))
        connection.commit()
        inserted_id = cursor.fetchone()
        return inserted_id[0]


def save_info_url(url_id: str, status_code: str, h1: str, title: str, description: str):
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
