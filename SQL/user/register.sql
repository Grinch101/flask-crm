INSERT INTO
    users(client_name, email, passkey)
VALUES
    (%s, %s, %s)
RETURNING
id AS user_id;