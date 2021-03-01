DELETE FROM
    activities
WHERE
    contact_id = %s;

DELETE FROM
    contacts
WHERE
    id = %s;

