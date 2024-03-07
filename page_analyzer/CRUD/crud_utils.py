from page_analyzer.CRUD.db_util import get_connection
from psycopg2 import sql


def get_url(where: str,
            value: str,
            order_by: str = 'ASC') -> tuple:
    query = sql.SQL('SELECT * FROM urls WHERE {} = %s ORDER BY "id" {}').format(
        sql.Identifier(where),
        sql.SQL(order_by))
    with get_connection().cursor() as cursor:
        cursor.execute(query, (value,))
        data = cursor.fetchone()
    if data:
        return {'id': data[0],
                'name': data[1],
                'created_at': data[2]}


def get_column(column_name: str, where: str, value: str) -> tuple:
    query = sql.SQL('SELECT {} FROM urls WHERE {} =%s').format(
        sql.Identifier(column_name),
        sql.Identifier(where))
    with get_connection().cursor() as cursor:
        cursor.execute(query, (value,))
        data = cursor.fetchall()
    if data:
        return data[0][0]

    return data


def get_url_pars(table_name: str, where: str, value: str) -> list:
    query = sql.SQL('SELECT * FROM {} WHERE {} = %s ORDER BY "id" DESC').format(
        sql.Identifier(table_name),
        sql.Identifier(where))
    with get_connection().cursor() as cursor:
        cursor.execute(query, (value,))
        data = cursor.fetchall()
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
    list_urls = []
    with get_connection().cursor() as cursor:
        cursor.execute('SELECT id, name FROM urls ORDER BY id  DESC')
        urls = cursor.fetchall()
        cursor.execute("""SELECT DISTINCT uc.url_id, uc.status_code, uc.created_at
                            FROM url_checks uc
                            JOIN (
                                SELECT url_id, MAX(created_at) AS max_created_at
                                    FROM url_checks
                                    GROUP BY url_id) AS max_created_at
                            ON uc.url_id = max_created_at.url_id AND uc.created_at = max_created_at.max_created_at
                            ORDER BY uc.url_id  DESC""")
        url_checks = cursor.fetchall()
    url_checks_dict = {item[0]: item for item in url_checks}
    for url_id, name in urls:
        data = {}
        data['id'] = url_id
        data['name'] = name
        data['status_code'] = ''
        data['create_at'] = ''
        if url_id in url_checks_dict:
            data['status_code'] = url_checks_dict[url_id][1]
            data['create_at'] = url_checks_dict[url_id][2]
        list_urls.append(data)
    return list_urls


def save_url(url: str):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url,))
        connection.commit()
        inserted_id = cursor.fetchone()
        return inserted_id[0]


def save_info_url(url_id: str,
                  status_code: str,
                  h1: str,
                  title: str,
                  description: str):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO url_checks (
            url_id,
            status_code,
            h1,
            title,
            description)
        VALUES (%s, %s, %s, %s, %s)
        """, (url_id,
              status_code,
              h1,
              title,
              description,))
        connection.commit()


def tu_string(value: str) -> str:
    if value:
        return value
    return ''
