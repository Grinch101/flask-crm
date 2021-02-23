CREATE TABLE users (
	client_name TEXT NOT NULL,
	email TEXT UNIQUE NOT NULL,
	passkey TEXT NOT NULL,
	id SERIAL PRIMARY KEY
);

CREATE TABLE contacts(
	"name" TEXT NOT NULL,
	phone TEXT NOT NULL,
	id SERIAL NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY (id),

	FOREIGN KEY (user_id) REFERENCES users (id)
);

