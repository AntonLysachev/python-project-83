from psycopg2 import sql, extras
import psycopg2
import os


def get_connection() -> psycopg2.connect:
    database_url = os.getenv("DATABASE_URL")
    connection = psycopg2.connect(database_url)
    return connection


def get_url_by_id(value: str, order_by: str = "ASC") -> tuple:
    query = sql.SQL('SELECT * FROM urls WHERE id = %s ORDER BY "id" {}').format(
        sql.SQL(order_by)
    )
    with get_connection().cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute(query, (value,))
        data = cursor.fetchone()
        if data:
            return data


def get_url_by_name(value: str, order_by: str = "ASC") -> tuple:
    query = sql.SQL('SELECT * FROM urls WHERE name = %s ORDER BY "id" {}').format(
        sql.SQL(order_by)
    )
    with get_connection().cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute(query, (value,))
        data = cursor.fetchone()
        if data:
            return data


def get_url(value: str) -> list:
    with get_connection().cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute(
            'SELECT * FROM url_checks WHERE url_id = %s ORDER BY "id" DESC', (value,)
        )
        data = cursor.fetchall()
        if data:
            return data


def get_urls_with_last_check() -> list:
    list_urls = []
    with get_connection().cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute("SELECT id, name FROM urls ORDER BY id  DESC")
        urls = cursor.fetchall()
        cursor.execute(
            """SELECT DISTINCT url_id, status_code, max(created_at)as created_at
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
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,))
        connection.commit()
        inserted_id = cursor.fetchone()
        return inserted_id[0]


def save_info_url(url_id: str, status_code: str, h1: str, title: str, description: str):
    with get_connection() as connection, connection.cursor() as cursor:
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
