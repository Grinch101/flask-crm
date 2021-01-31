SELECT u.client_name,c.contact_name, c.contact_phone, c.row_id as id FROM contacts AS c JOIN users AS u ON c.userid = u.userid WHERE c.userid  = %s;
