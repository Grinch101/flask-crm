UPDATE
    contacts
SET
    "name" = %s,
    phone = %s
WHERE
    id = %s AND user_id = %s
    RETURNING *;