GET_TABLE = 'SELECT * FROM {} ORDER BY "id" {}'
GET_FIELD = 'SELECT * FROM {} WHERE {} = %s'
GET_COLUMN = 'SELECT {} FROM {} WHERE {} =%s'
INSERT = 'INSERT INTO {} ({}, {}) VALUES (%s, %s)'

INSERT_URL_TABLE = ('urls', 'name', 'created_at')