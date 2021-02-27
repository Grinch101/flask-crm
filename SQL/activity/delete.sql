DELETE FROM
    activities
WHERE
    id = %s
    AND contact_id = %s
    AND user_id = %s;