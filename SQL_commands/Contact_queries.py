# find_book() query:
find = 'SELECT u.client_name,c.contact_name, c.contact_phone, c.row_id as id FROM contacts AS c JOIN users AS u ON c.userid = u.userid WHERE c.userid  = %s;'

# add() a contact query:
add = 'INSERT INTO contacts(userid, contact_name, contact_phone) VALUES (%s,%s,%s)'

# get_all() query to retrieve all rows of a table
get_all = "SELECT * FROM contacts"

# clear_all() query to truncate a table
truncate = 'TRUNCATE contacts RESTART IDENTITY'

# delete() query to delete a row specified by
delete = 'DELETE FROM contacts WHERE row_id = %s'

# update() query to update rows using their id
update = 'UPDATE contacts SET contact_name = %s , contact_phone = %s , userid = %s'
