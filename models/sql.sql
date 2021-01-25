CREATE DATABASE phonebook;

CREATE TABLE users (
	client_name VARCHAR(20) NOT NULL,
	email VARCHAR(30) UNIQUE NOT NULL,
	passkey VARCHAR(20) NOT NULL,
	USERID SERIAL PRIMARY KEY
);

CREATE TABLE contacts(
	contact_name varchar(20) NOT NULL,
	contact_phone VARCHAR(20) NOT NULL,
	row_id SERIAL NOT NULL,
	userid INT NOT NULL,
	PRIMARY KEY (row_id),+87\

	FOREIGN KEY (userid) REFERENCES users (userid) ON DELETE CASCADE
);



