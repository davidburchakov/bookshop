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


INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(1, 'Lev Tolstoy', 'Russia', '1828-09-09', '1910-11-20');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(2, 'Fyodor Dostoevsky', 'Russia', '1821-11-11', '1881-02-09');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(3, 'Albert Camus', 'France', '1913-11-07', '1960-01-04');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(4, 'Franz Kafka', 'Czech Republic', '1883-07-03', '1924-06-03');
-- Seneca was born in Corduba in Hispania, and raised in Rome, where he was trained in rhetoric and philosophy.
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(5, 'Lucius Annaeus Seneca', 'Rome', '4 BC', 'AD 65');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(6, 'Haruki Murakami', 'Japan', '1949-01-12', '');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(7, 'Andrzej Sapkowski', 'Poland', '1948-06-21', '');


INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('crime-and-punishment', 2, 'Crime and Punishment','crime_punishment.jpg', 'Very hard existentioal book', 200, 10, false, 'English', 'Russian');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('hadji-murat', 1, 'Hadji Murat','hadji_murat.jpg', 'Very harsh russian historical book', 100, 20, false, 'Russian', 'Russian');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('camus-myth-sisyphus', 3, 'Le mythe de sisyphe','myth_sisyphus.jpg', 'Philosophical book by a 20th century existentionalist', 20, 15, false, 'English', 'French');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('kafka-metamorphosis', 4, 'Metamorphosis','metamorphosis.jpg', 'Philosophical book by a 19th century absurdist from Czech Republic', 50, 30, false, 'English', 'Czech');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('murakami-wood', 6, 'Norwegian Wood','norwegian_wood.jpg', 'A magnificent blending of the music, the mood, and the ethos that was the sixties with the story of one college student''s romantic coming of age, Norwegian Wood brilliantly recaptures a young man''s first, hopeless, and heroic love.', 12, 50, false, 'English', 'Japanese');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('seneka-letters', 5, 'Letters from a Stoic','Seneca-Letters-from-a-Stoic.jpg', 'Lucius Annaeus Seneca (often known simply as Seneca or Seneca the Younger); ca. 4 BC – 65 AD) was a Roman Stoic philosopher, statesman, and dramatist of the Silver Age of Latin literature. He was tutor and later advisor to emperor Nero, who later forced him to commit suicide for alleged complicity in the Pisonian conspiracy to have him assassinated.', 50, 35, true, 'English', 'Greek');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('krew-elfow', 7, 'Krew Elfow','krew_elfow.jpg', 'Geralt, the witcher of Rivia, is back - and this time he holds the fate of the whole land in his hands ... For more than a hundred years, humans, dwarves, gnomes and elves lived together in relative peace. But times have changed, the uneasy peace is over and now the races once again fight each other - and themselves: dwarves are killing their kinsmen, and elves are murdering humans and elves, at least those elves who are friendly to humans ... Into this tumultuous time is born a child for whom the witchers of the world have been waiting. Ciri, the granddaughter of Queen Calanthe, the Lioness of Cintra, has strange powers and a stranger destiny, for prophecy names her the Flame, one with the power to change the world - for good, or for evil ...', 120, 70, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('chrzest-ognia', 7, 'Chrzest Ognia','chrzest_ognia.jpg', 'Baptism of Fire is the third novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published in 1996 in Polish and in English in 2014. It is a sequel to the second Witcher novel Time of Contempt and is followed by The Tower of the Swallow.', 100, 65, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('czas-pogardy', 7, 'Czas Pogardy','czas-pogardy.jpg', 'Time of Contempt is the second novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published 1995 in Polish, and 2013 in English. It is a sequel to the first Witcher novel Blood of Elves and is followed by Baptism of Fire.', 130, 75, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('miecz-przeznaczenia', 7, 'Miecz Przeznaczenia','miecz-przeznaczenia.webp', 'Sword of Destiny is the second published short story collection in Polish fantasy writer Andrzej Sapkowski''s The Witcher series. Although published in 1992, it is officially considered the second entry in the series, behind The Last Wish, which was published the following year.', 170, 60, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('pani-jeziora', 7, 'Pani Jeziora','pani_jeziora.jpg', 'The Lady of the Lake is the fifth and final novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published in Poland in 1999. It is a sequel to the fourth Witcher novel, The Tower of Swallows.', 150, 55, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('wieza-jaskolki', 7, 'Wieza Jaskolki','wieza-jaskolki.jpg', 'The Tower of the Swallow, published as The Tower of Swallows in the United States is the fourth novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published in Poland in 1997.', 170, 80, false, 'Polish', 'Polish');
-- INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('krew-elfow', 7, 'Krew Elfow','krew_elfow.jpg', '', 120, 70, false, 'Polish', 'Polish');

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