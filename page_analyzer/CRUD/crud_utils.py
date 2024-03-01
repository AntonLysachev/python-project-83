from page_analyzer.CRUD.db_util import get_connection
from psycopg2 import sql
from page_analyzer.constants import (GET_COLUMN,
                                     GET_FIELD,
                                     INSERT_URL_TABLE,
                                     INSERT_URL_CHECKS_TABLE,
                                     GET_CHECK,
                                     GET_INFO_URL)


def get_url(table_name: str,
            where: str,
            value: str,
            order_by: str = 'ASC') -> tuple:
    query = sql.SQL(GET_FIELD).format(
        sql.Identifier(table_name),
        sql.Identifier(where),
        sql.SQL(order_by))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        data = cursor.fetchone()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
    if data:
        return {'id': data[0],
                'name': data[1],
                'created_at': data[2]}


def get_column(column_name: str, table_name: str, where, value: str) -> tuple:
    query = sql.SQL(GET_COLUMN).format(sql.Identifier(column_name),
                                       sql.Identifier(table_name),
                                       sql.Identifier(where))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
    if data:
        return data[0][0]

    return data


def get_url_pars(table_name: str, where: str, value: str) -> list:
    query = sql.SQL(GET_CHECK).format(
        sql.Identifier(table_name),
        sql.Identifier(where))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(GET_INFO_URL)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(INSERT_URL_TABLE, (url,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)


def save_pars(url_id: str,
               status_code: str,
               h1: str,
               title: str,
               description: str):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(INSERT_URL_CHECKS_TABLE, (url_id,
                                                 status_code,
                                                 h1,
                                                 title,
                                                 description,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)


def tu_string(value: str) -> str:
    if value:
        return value
    return ''
