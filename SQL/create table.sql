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

CREATE TABLE activities(
	"action" TEXT NOT NULL,
	"description" TEXT,
	"datetime" TIMESTAMP NOT NULL,
	user_id INT NOT NULL,
	contact_id INT NOT NULL,
	"id" SERIAL PRIMARY KEY,
	FOREIGN KEY (user_id) REFERENCES users ("id"),
	FOREIGN KEY (contact_id) REFERENCES contacts ("id")
)