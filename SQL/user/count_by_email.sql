SELECT
    COUNT(email)
FROM
    users
WHERE
    email = %s: