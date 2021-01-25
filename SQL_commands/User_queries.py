# add() query for registration:
register = 'INSERT INTO users(client_name,email,passkey) VALUES (%s,%s,%s)'

# validate() query 
validate = 'SELECT passkey FROM users WHERE users.email = %s;'

# old_user() query to retrieve all emails in database
old_user = 'SELECT email FROM users;'

# delete() query to delete registration for a specific user
delete = 'DELETE FROM users WHERE users.userid = %s;'

# find_userid_by_email() query to retrieve userid for given email
userid_email = 'SELECT userid FROM users WHERE email = %s;'

# get_all() query to retrieve all rows
get_all = "SELECT * FROM users"

# update() query to update a certain row specified by userid
update = 'UPDATE users SET email = %s , passkey = %s , client_name = %s'