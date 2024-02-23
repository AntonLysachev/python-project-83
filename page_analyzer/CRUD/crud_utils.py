from page_analyzer.CRUD.db_util import get_connection
from psycopg2 import sql
from page_analyzer.constants import GET_COLUMN, GET_FIELD, GET_TABLE, INSERT_URL_TABLE, INSERT_URL_CHECKS_TABLE, GET_CHECK 


def get_table(table_name, order_by='ASC'):
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


def get_field(table_name, where, value, order_by='ASC'):
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



def get_column(column_name, table_name, where, value):
    query = sql.SQL(GET_COLUMN).format(sql.Identifier(column_name),
                                       sql.Identifier(table_name),
                                       sql.Identifier(where))
    try:
        print(query)
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
    data = get_field(table_name, where, value)
    if data:
        return {'id': data[0],
                'name': data[1],
                'created_at': data[2],}


def get_url_check(table_name, where, value):
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
        to_dict = []
        print(data)
        for field in data:
            to_dict.append({'id': field[0],
                            'url_id': field[1],
                            'status_code': field[2],
                            ' h1': field[3],
                            'title': field[4],
                            'description': field[5],
                            'created_at': field[6],})
    return to_dict


def save_url(url, created_at):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(INSERT_URL_TABLE, (url,
                               created_at,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
        return False

    return True

def save_check(url_id, status_code, date):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(INSERT_URL_CHECKS_TABLE, (url_id,
                                                 status_code,
                                                 '',
                                                 '',
                                                 '',
                                                 date,))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception) as error:
        print(error)
        return False

    return True


def to_dict_table(table):
    users = []
    data = get_table(table, 'DESC')
    for url in data:
        users.append({'id': url[0],
                      'name': url[1],
                      'created_at': url[2],})

    return users
