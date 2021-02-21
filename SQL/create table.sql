CREATE DATABASE phonebook;

CREATE TABLE users (
	client_name TEXT NOT NULL,
	email TEXT UNIQUE NOT NULL,
	passkey TEXT NOT NULL,
	id SERIAL PRIMARY KEY
);

CREATE TABLE contacts(
	contact_name TEXT NOT NULL,
	contact_phone TEXT NOT NULL,
	id SERIAL NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY (id),

	FOREIGN KEY (user_id) REFERENCES users (id)
);



