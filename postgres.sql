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
INSERT INTO shopapp_authors (fullname) VALUES('Lucius Annaeus Seneca');
INSERT INTO shopapp_authors (fullname) VALUES('Haruki Murakami');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read) VALUES('crime-and-punishment', 2, 'Crime and Punishment','crime_punishment.jpg', 'Very hard existentioal book', 200, 10, false);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read) VALUES('hadji-murat', 1, 'Hadji Murat','hadji_murat.jpg', 'Very harsh russian historical book', 100, 20, false);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read) VALUES('camus-myth-sisyphus', 3, 'Le mythe de sisyphe','myth_sisyphus.jpg', 'Philosophical book by a 20th century existentionalist', 20, 15, false);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read) VALUES('kafka-metamorphosis', 4, 'Metamorphosis','metamorphosis.jpg', 'Philosophical book by a 19th century absurdist from Czech Republic', 50, 30, false);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read) VALUES('murakami-wood', 6, 'Norwegian Wood','norwegian_wood.jpg', 'A magnificent blending of the music, the mood, and the ethos that was the sixties with the story of one college student''s romantic coming of age, Norwegian Wood brilliantly recaptures a young man''s first, hopeless, and heroic love.', 12, 50, false);
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read) VALUES('seneka-letters', 5, 'Letters from a Stoic','Seneca-Letters-from-a-Stoic.jpg', 'Lucius Annaeus Seneca (often known simply as Seneca or Seneca the Younger); ca. 4 BC – 65 AD) was a Roman Stoic philosopher, statesman, and dramatist of the Silver Age of Latin literature. He was tutor and later advisor to emperor Nero, who later forced him to commit suicide for alleged complicity in the Pisonian conspiracy to have him assassinated.', 50, 35, true);

INSERT INTO shopapp_faq (question, answer) VALUES('How can I proceed with the payment?', 'You can you any valid MASTERCARD or VISA card');

INSERT INTO shopapp_faq (question, answer) VALUES('What shipping options are available?', 'We offer standard, expedited, and international shipping options.');
INSERT INTO shopapp_faq (question, answer) VALUES('Can I return a book if I''m not satisfied?', 'Yes, returns are accepted within 30 days of purchase in their original condition.');
INSERT INTO shopapp_faq (question, answer) VALUES('How do I track my order?', 'Once your order is shipped, a tracking number will be sent to your email.');
INSERT INTO shopapp_faq (question, answer) VALUES('Is it safe to provide my credit card details on your website?', 'Yes, our website uses secure encryption to protect all your personal information.');
INSERT INTO shopapp_faq (question, answer) VALUES('Are there any discounts for bulk purchases?', 'Yes, we offer discounts on bulk purchases. Please contact our support team for more details.');
INSERT INTO shopapp_faq (question, answer) VALUES('Do you offer gift wrapping services?', 'Yes, we provide gift wrapping at an additional cost.');
INSERT INTO shopapp_faq (question, answer) VALUES('How often do you update your book collection?', 'Our book collection is updated weekly with new releases and bestsellers.');
INSERT INTO shopapp_faq (question, answer) VALUES('Can I request a book that''s not listed on your website?', 'Yes, you can request a book through our special order service.');
INSERT INTO shopapp_faq (question, answer) VALUES('Do you have an e-book section?', 'Yes, we have a wide range of e-books available for instant download.');
INSERT INTO shopapp_faq (question, answer) VALUES('What should I do if I receive a damaged book?', 'Please contact our customer service immediately to arrange a replacement or refund.');