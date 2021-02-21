SELECT
    u.client_name,
    c.contact_name,
    c.contact_phone,
    c.id as id
FROM
    contacts AS c
    JOIN users AS u ON c.user_id = u.id
WHERE
    c.user_id = %s;