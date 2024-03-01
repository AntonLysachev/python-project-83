GET_TABLE = 'SELECT * FROM {} ORDER BY "id" {}'
GET_FIELD = 'SELECT * FROM {} WHERE {} = %s ORDER BY "id" {}'
GET_CHECK = 'SELECT * FROM {} WHERE {} = %s ORDER BY "id" DESC'
GET_COLUMN = 'SELECT {} FROM {} WHERE {} =%s'
INSERT_URL_TABLE = 'INSERT INTO urls (name) VALUES (%s)'
INSERT_URL_CHECKS_TABLE = """
INSERT INTO url_checks (
    url_id,
    status_code,
    h1,
    title,
    description
)
VALUES (%s, %s, %s, %s, %s)
"""

GET_INFO_URL = """
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
"""
