-- sudo -i -u postgres 
-- Gpsql
-- \list
-- CREATE DATABASE bookshop;
-- \c bookshop;
-- \dt
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bookshop_admin;



DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id serial PRIMARY KEY,
	username VARCHAR(25),
	password TEXT,
	date_created timestamp with time zone DEFAULT current_timestamp
);

DROP TABLE IF EXISTS authors;

CREATE TABLE authors(
	id serial PRIMARY KEY,
	fullname VARCHAR(25)
);

DROP TABLE IF EXISTS books;

CREATE TABLE books(
	id serial PRIMARY KEY,
	slug TEXT,
	author_id INT,
	title TEXT,
	img VARCHAR(35),
	description TEXT,
	stock int,

	FOREIGN KEY (author_id) REFERENCES authors(id)
);


INSERT INTO users (username, password) VALUES('admin', 'admin');
INSERT INTO users (username, password) VALUES('user', 'user');
INSERT INTO users (username, password) VALUES('david', 'david');
INSERT INTO shopapp_authors (fullname) VALUES('Lev Tolstoy');
INSERT INTO shopapp_authors (fullname) VALUES('Fyodor Dostoevsky');
INSERT INTO shopapp_authors (fullname) VALUES('Albert Camus');
INSERT INTO shopapp_authors (fullname) VALUES('Franz Kafka');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock) VALUES('crime-and-punishment', 2, 'Crime and Punishment','crime_punishment.jpg', 'Very hard existentioal book', 200);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock) VALUES('hadji-murat', 1, 'Hadji Murat','hadji_murat.jpg', 'Very harsh russian historical book', 100);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock) VALUES('camus-myth-sisyphus', 3, 'Le mythe de sisyphe','myth_sisyphus.jpg', 'Philosophical book by a 20th century existentionalist', 20);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock) VALUES('kafka-metamorphosis', 4, 'Metamorphosis','metamorphosis.jpg', 'Philosophical book by a 19th century absurdist from Czech Republic', 50);

INSERT INTO shopapp_faq (question, answer) VALUES('How can I proceed with the payment?', 'You can you any valid MASTERCARD or VISA card');