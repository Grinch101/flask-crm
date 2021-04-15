INSERT INTO
    contacts(user_id, "name", phone)
VALUES
    (%s, %s, %s)
RETURNING
id AS contact_id;