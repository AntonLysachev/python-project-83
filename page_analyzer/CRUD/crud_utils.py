from page_analyzer.CRUD.db_util import get_connection
from psycopg2 import sql
from page_analyzer.constants import GET_COLUMN, GET_FIELD, GET_TABLE, INSERT


def get_table(table_name):
    query = sql.SQL(GET_TABLE).format(sql.Identifier(table_name))
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


def get_field(table_name, where, value):
    query = sql.SQL(GET_FIELD).format(
        sql.Identifier(table_name),
        sql.Identifier(where))
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



def get_column(column_name, table_name, where, value):
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


def get_url(table_name, where, value):
    user_data = {}
    data = get_field(table_name, where, value)
    if data:
        user_data.update({'id': data[0],
                          'name': data[1],
                          'created_at': data[2],})

    return user_data


def save(args, url, created_at):
    list_args = map(sql.Identifier, args)
    query = sql.SQL(INSERT).format(*list_args)
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (url,
                               created_at,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
        return False

    return True


def to_dict_table(table):
    users = []
    data = get_table(table)
    for url in data:
        users.append({'id': url[0],
                      'name': url[1],
                      'created_at': url[2],})

    return users
