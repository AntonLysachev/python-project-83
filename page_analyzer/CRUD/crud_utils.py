from page_analyzer.CRUD.db_util import get_connection
from datetime import date
from psycopg2 import sql
from page_analyzer.constants import (GET_COLUMN,
                                     GET_FIELD,
                                     GET_TABLE,
                                     INSERT_URL_TABLE,
                                     INSERT_URL_CHECKS_TABLE,
                                     GET_CHECK,
                                     GET_INFO_URL)


def get_table(table_name: str, order_by: str = 'ASC') -> tuple:
    query = sql.SQL(GET_TABLE).format(sql.Identifier(table_name),
                                      sql.SQL(order_by))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)

    return data


def get_field(table_name: str,
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
    return data


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


def get_url(table_name: str, where: str, value: str) -> dict:
    data = get_field(table_name, where, value)
    if data:
        return {'id': data[0],
                'name': data[1],
                'created_at': data[2]}


def get_url_check(table_name: str, where: str, value: str) -> list:
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


def save_url(url: str, created_at: str):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(INSERT_URL_TABLE, (url, created_at,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)


def save_check(url_id: str,
               status_code: str,
               h1: str,
               title: str,
               description: str,
               date: date):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(INSERT_URL_CHECKS_TABLE, (url_id,
                                                 status_code,
                                                 h1,
                                                 title,
                                                 description,
                                                 date,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)


def to_dict_table(table: str) -> list:
    users = []
    data = get_table(table, 'DESC')
    for url in data:
        users.append({'id': url[0],
                      'name': url[1],
                      'created_at': url[2]})
    return users


def tu_string(value: str) -> str:
    if value:
        return value
    return ''
