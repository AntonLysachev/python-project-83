from page_analyzer.CRUD.db_util import get_connection
from psycopg2 import sql, extras


def get_url(where: str, value: str, order_by: str = "ASC") -> tuple:
    query = sql.SQL('SELECT * FROM urls WHERE {} = %s ORDER BY "id" {}').format(
        sql.Identifier(where), sql.SQL(order_by)
    )
    with get_connection().cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute(query, (value,))
        data = cursor.fetchone()
        if data:
            return {
                "id": data["id"],
                "name": data["name"],
                "created_at": data["created_at"],
            }


def get_url_list(value: str) -> list:
    list_urls = []
    with get_connection().cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute(
            'SELECT * FROM url_checks WHERE url_id = %s ORDER BY "id" DESC', (value,)
        )
        data = cursor.fetchall()
        if data:
            for field in data:
                list_urls.append(
                    {
                        "id": field["id"],
                        "url_id": field["url_id"],
                        "status_code": field["status_code"],
                        "h1": field["h1"],
                        "title": field["title"],
                        "description": field["description"],
                        "created_at": field["created_at"],
                    }
                )
    return list_urls


def get_info_url() -> list:
    list_urls = []
    with get_connection().cursor(cursor_factory=extras.DictCursor) as cursor:
        cursor.execute("SELECT id, name FROM urls ORDER BY id  DESC")
        urls = cursor.fetchall()
        cursor.execute(
            """SELECT DISTINCT uc.url_id, uc.status_code, uc.created_at
                            FROM url_checks uc
                            JOIN (
                                SELECT url_id, MAX(created_at) AS max_created_at
                                    FROM url_checks
                                    GROUP BY url_id) AS max_created_at
                            ON uc.url_id = max_created_at.url_id AND uc.created_at = max_created_at.max_created_at
                            ORDER BY uc.url_id  DESC"""
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
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,))
        connection.commit()
        inserted_id = cursor.fetchone()
        return inserted_id[0]


def save_info_url(url_id: str, status_code: str, h1: str, title: str, description: str):
    with get_connection() as connection:
        cursor = connection.cursor()
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
