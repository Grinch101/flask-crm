DELETE FROM
    activities
WHERE
    id = %s
RETURNING
id AS activity_id;