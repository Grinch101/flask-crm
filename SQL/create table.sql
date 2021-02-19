CREATE DATABASE phonebook;

CREATE TABLE users (
	client_name VARCHAR(20) NOT NULL,
	email VARCHAR(30) UNIQUE NOT NULL,
	passkey VARCHAR(20) NOT NULL,
	id SERIAL PRIMARY KEY
);

CREATE TABLE contacts(
	contact_name varchar(20) NOT NULL,
	contact_phone VARCHAR(20) NOT NULL,
	id SERIAL NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY (id),

	FOREIGN KEY (user_id) REFERENCES users (id)
);



