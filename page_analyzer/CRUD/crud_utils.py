from page_analyzer.CRUD.db_util import get_connection
from psycopg2 import sql


def get_url(where: str,
            value: str,
            order_by: str = 'ASC') -> tuple:
    query = sql.SQL('SELECT * FROM urls WHERE {} = %s ORDER BY "id" {}').format(
        sql.Identifier(where),
        sql.SQL(order_by))
    try:
        with get_connection().cursor() as cursor:
            cursor.execute(query, (value,))
            data = cursor.fetchone()
    except (Exception) as error:
        print(error)
    if data:
        return {'id': data[0],
                'name': data[1],
                'created_at': data[2]}


def get_column(column_name: str, where: str, value: str) -> tuple:
    query = sql.SQL('SELECT {} FROM urls WHERE {} =%s').format(
        sql.Identifier(column_name),
        sql.Identifier(where))
    try:
        with get_connection().cursor() as cursor:
            cursor.execute(query, (value,))
            data = cursor.fetchall()
    except (Exception) as error:
        print(error)
    if data:
        return data[0][0]

    return data


def get_url_pars(table_name: str, where: str, value: str) -> list:
    query = sql.SQL('SELECT * FROM {} WHERE {} = %s ORDER BY "id" DESC').format(
        sql.Identifier(table_name),
        sql.Identifier(where))
    try:
        with get_connection().cursor() as cursor:
            cursor.execute(query, (value,))
            data = cursor.fetchall()
    except (Exception) as error:
        print(error)
    if data:
        list_urls = []
        for field in data:
            list_urls.append({'id': tu_string(field[0]),
                              'url_id': tu_string(field[1]),
                              'status_code': tu_string(field[2]),
                              'h1': tu_string(field[3]),
                              'title': tu_string(field[4]),
                              'description': tu_string(field[5]),
                              'created_at': tu_string(field[6])})
        return list_urls


def get_info_url() -> list:
    try:
        with get_connection().cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT
                    u.id,
                    u.name,
                    max_uc.status_code,
                    max_uc.created_at
                FROM
                    urls AS u
                LEFT JOIN (
                    SELECT
                        uc.url_id,
                        uc.status_code,
                        uc.created_at
                    FROM
                        url_checks AS uc
                    INNER JOIN (
                        SELECT
                            url_id,
                            MAX(created_at) AS max_created_at
                        FROM
                            url_checks
                        GROUP BY
                            url_id
                    ) AS max_uc
                    ON uc.url_id = max_uc.url_id
                    AND uc.created_at = max_uc.max_created_at
                ) AS max_uc
                ON u.id = max_uc.url_id
                ORDER BY
                    u.id DESC
                """)
            data = cursor.fetchall()
    except (Exception) as error:
        raise error
    if data:
        list_urls = []
        for field in data:
            list_urls.append({'id': tu_string(field[0]),
                              'name': tu_string(field[1]),
                              'status_code': tu_string(field[2]),
                              'created_at': tu_string(field[3])})
        return list_urls


def save_url(url: str):
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url,))
            connection.commit()
            inserted_id = cursor.fetchone()
            return inserted_id[0]
    except (Exception) as error:
        print(error)


def save_info_url(url_id: str,
                  status_code: str,
                  h1: str,
                  title: str,
                  description: str):
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description
            )
            VALUES (%s, %s, %s, %s, %s)
            """, (url_id,
                  status_code,
                  h1,
                  title,
                  description,))
            connection.commit()
    except (Exception) as error:
        print(error)


def tu_string(value: str) -> str:
    if value:
        return value
    return ''
