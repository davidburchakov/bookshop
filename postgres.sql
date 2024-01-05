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

INSERT INTO shopapp_category (id, name) VALUES (1, 'Fantasy');
INSERT INTO shopapp_category (id, name) VALUES (2, 'Philosophy');
INSERT INTO shopapp_category (id, name) VALUES (3, 'Classics');
INSERT INTO shopapp_category (id, name) VALUES (4, 'Novel');
INSERT INTO shopapp_category (id, name) VALUES (5, 'Absurdism');
INSERT INTO shopapp_category (id, name) VALUES (6, 'Historical Fiction');
INSERT INTO shopapp_category (id, name) VALUES (7, 'Existentialism');



INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(1, 'Lev Tolstoy', 'Russia', '1828-09-09', '1910-11-20');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(2, 'Fyodor Dostoevsky', 'Russia', '1821-11-11', '1881-02-09');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(3, 'Albert Camus', 'France', '1913-11-07', '1960-01-04');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(4, 'Franz Kafka', 'Czech Republic', '1883-07-03', '1924-06-03');
-- Seneca was born in Corduba in Hispania, and raised in Rome, where he was trained in rhetoric and philosophy.
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(5, 'Lucius Annaeus Seneca', 'Rome', '4 BC', 'AD 65');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(6, 'Haruki Murakami', 'Japan', '1949-01-12', '');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(7, 'Andrzej Sapkowski', 'Poland', '1948-06-21', '');
INSERT INTO shopapp_authors (id, fullname, country, date_of_birth, date_of_death) VALUES(8, 'J.K. Rowling', 'United Kingdom', '1965-07-31', '');



INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(1, 'crime-and-punishment', 2, 'Crime and Punishment','crime_punishment.jpg', 'Very hard existentioal book', 200, 10, false, 'English', 'Russian');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(2, 'hadji-murat', 1, 'Hadji Murat','hadji_murat.jpg', 'Very harsh russian historical book', 100, 20, false, 'Russian', 'Russian');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(3, 'camus-myth-sisyphus', 3, 'Le mythe de sisyphe','myth_sisyphus.jpg', 'Philosophical book by a 20th century existentionalist', 20, 15, false, 'English', 'French');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(4, 'kafka-metamorphosis', 4, 'Metamorphosis','metamorphosis.jpg', 'Philosophical book by a 19th century absurdist from Czech Republic', 50, 30, false, 'English', 'Czech');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(5, 'murakami-wood', 6, 'Norwegian Wood','norwegian_wood.jpg', 'A magnificent blending of the music, the mood, and the ethos that was the sixties with the story of one college student''s romantic coming of age, Norwegian Wood brilliantly recaptures a young man''s first, hopeless, and heroic love.', 12, 50, false, 'English', 'Japanese');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(6, 'seneka-letters', 5, 'Letters from a Stoic','Seneca-Letters-from-a-Stoic.jpg', 'Lucius Annaeus Seneca (often known simply as Seneca or Seneca the Younger); ca. 4 BC – 65 AD) was a Roman Stoic philosopher, statesman, and dramatist of the Silver Age of Latin literature. He was tutor and later advisor to emperor Nero, who later forced him to commit suicide for alleged complicity in the Pisonian conspiracy to have him assassinated.', 50, 35, true, 'English', 'Greek');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(7, 'krew-elfow', 7, 'Krew Elfow','krew_elfow.jpg', 'Geralt, the witcher of Rivia, is back - and this time he holds the fate of the whole land in his hands ... For more than a hundred years, humans, dwarves, gnomes and elves lived together in relative peace. But times have changed, the uneasy peace is over and now the races once again fight each other - and themselves: dwarves are killing their kinsmen, and elves are murdering humans and elves, at least those elves who are friendly to humans ... Into this tumultuous time is born a child for whom the witchers of the world have been waiting. Ciri, the granddaughter of Queen Calanthe, the Lioness of Cintra, has strange powers and a stranger destiny, for prophecy names her the Flame, one with the power to change the world - for good, or for evil ...', 120, 70, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(8, 'chrzest-ognia', 7, 'Chrzest Ognia','chrzest_ognia.jpg', 'Baptism of Fire is the third novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published in 1996 in Polish and in English in 2014. It is a sequel to the second Witcher novel Time of Contempt and is followed by The Tower of the Swallow.', 100, 65, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(9, 'czas-pogardy', 7, 'Czas Pogardy','czas-pogardy.jpg', 'Time of Contempt is the second novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published 1995 in Polish, and 2013 in English. It is a sequel to the first Witcher novel Blood of Elves and is followed by Baptism of Fire.', 130, 75, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(10, 'miecz-przeznaczenia', 7, 'Miecz Przeznaczenia','miecz-przeznaczenia.webp', 'Sword of Destiny is the second published short story collection in Polish fantasy writer Andrzej Sapkowski''s The Witcher series. Although published in 1992, it is officially considered the second entry in the series, behind The Last Wish, which was published the following year.', 170, 60, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(11, 'pani-jeziora', 7, 'Pani Jeziora','pani_jeziora.jpg', 'The Lady of the Lake is the fifth and final novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published in Poland in 1999. It is a sequel to the fourth Witcher novel, The Tower of Swallows.', 150, 55, false, 'Polish', 'Polish');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(12, 'wieza-jaskolki', 7, 'Wieza Jaskolki','wieza-jaskolki.jpg', 'The Tower of the Swallow, published as The Tower of Swallows in the United States is the fourth novel in the Witcher Saga written by Polish fantasy writer Andrzej Sapkowski, first published in Poland in 1997.', 170, 80, false, 'Polish', 'Polish');
-- INSERT INTO shopapp_books (slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES('krew-elfow', 7, 'Krew Elfow','krew_elfow.jpg', '', 120, 70, false, 'Polish', 'Polish');

INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(13, 'harry-potter-and-the-philosophers-stone', 8, 'Harry Potter and the Philosopher''s Stone','harry-potter-philosophers-stone.jpg', 'Harry Potter and the Philosopher''s Stone is the first novel in the Harry Potter series written by British author J.K. Rowling. The story follows Harry Potter, a young wizard who discovers his magical heritage as he makes close friends and a few enemies in his first year at the Hogwarts School of Witchcraft and Wizardry.', 200, 45, false, 'English', 'English');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(14, 'harry-potter-and-the-chamber-of-secrets', 8, 'Harry Potter and the Chamber of Secrets','harry-potter-chamber-secrets.jpg', 'Harry Potter and the Chamber of Secrets is the second novel in the Harry Potter series written by British author J.K. Rowling. The plot follows Harry''s second year at Hogwarts as he and his friends investigate a dark mystery that has been terrorizing the school.', 200, 45, false, 'English', 'English');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(15, 'harry-potter-and-the-prisoner-of-azkaban', 8, 'Harry Potter and the Prisoner of Azkaban','harry-potter-prisoner-azkaban.jpg', 'Harry Potter and the Prisoner of Azkaban is the third novel in the Harry Potter series written by British author J.K. Rowling. The book follows Harry Potter, a young wizard, in his third year at Hogwarts School of Witchcraft and Wizardry. Along with friends Ronald Weasley and Hermione Granger, Harry investigates Sirius Black, an escaped prisoner from Azkaban who they believe is one of Lord Voldemort''s old allies.', 200, 50, false, 'English', 'English');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(16, 'harry-potter-and-the-goblet-of-fire', 8, 'Harry Potter and the Goblet of Fire','harry-potter-goblet-fire.jpg', 'Harry Potter and the Goblet of Fire is the fourth book in the Harry Potter series by J.K. Rowling. The story follows Harry''s participation in the Triwizard Tournament, a dangerous magical competition, and the rise of Lord Voldemort.', 250, 60, false, 'English', 'English');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(17, 'harry-potter-and-the-order-of-the-phoenix', 8, 'Harry Potter and the Order of the Phoenix','harry-potter-order-phoenix.jpg', 'Harry Potter and the Order of the Phoenix is the fifth installment in the Harry Potter series by J.K. Rowling. Harry faces the challenges of the authoritarian regime of the new Hogwarts High Inquisitor and learns more about the dark past of Lord Voldemort.', 270, 65, false, 'English', 'English');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(18, 'harry-potter-and-the-half-blood-prince', 8, 'Harry Potter and the Half-Blood Prince','harry-potter-half-blood-prince.webp', 'Harry Potter and the Half-Blood Prince, the sixth book in the Harry Potter series by J.K. Rowling, delves into the history of Lord Voldemort''s dark past and Harry''s preparations for the final battle against him.', 240, 69.99, false, 'English', 'English');
INSERT INTO shopapp_books (id, slug, author_id, title, img, description, stock, price, read, language, original_language) VALUES(19, 'harry-potter-and-the-deathly-hallows', 8, 'Harry Potter and the Deathly Hallows','harry-potter-deathly-hallows.jpg', 'Harry Potter and the Deathly Hallows, the seventh and final book in the Harry Potter series by J.K. Rowling, follows Harry, Ron, and Hermione as they leave Hogwarts behind and set out to finish the quest to defeat Lord Voldemort once and for all.', 210, 59.99, false, 'English', 'English');


INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (1, 2);
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (1, 3);
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (1, 4);
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (1, 7);
-- For 'Le mythe de sisyphe' by Albert Camus
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (3, 2); -- Philosophy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (3, 7); -- Existentialism

-- For 'Metamorphosis' by Franz Kafka
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (4, 2); -- Philosophy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (4, 5); -- Absurdism

-- For 'Norwegian Wood' by Haruki Murakami
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (5, 4); -- Novel

-- For 'Letters from a Stoic' by Lucius Annaeus Seneca
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (6, 2); -- Philosophy

-- For books by Andrzej Sapkowski (assuming they are all 'Fantasy')
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (7, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (8, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (9, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (10, 1); -- Fantasy

-- For 'Harry Potter' series by J.K. Rowling
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (13, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (14, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (15, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (16, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (17, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (18, 1); -- Fantasy
INSERT INTO shopapp_bookscategories (book_id, category_id) VALUES (19, 1); -- Fantasy



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