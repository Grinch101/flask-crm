INSERT INTO
    activities(action, description, datetime, user_id, contact_id)
VALUES
(%s, %s, %s, %s, %s)
RETURNING
id AS activity_id;