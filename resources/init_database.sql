CREATE TABLE users(
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) UNIQUE,
	password VARCHAR(60)
);

CREATE TABLE coments(
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT NOT NULL,
	type_id INT NOT NULL,
	type VARCHAR(20) NOT NULL,
	text TEXT NOT NULL,
	date DATE,
	CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id),
	CONSTRAINT check_type CHECK (type IN ('photos', 'films')),
    UNIQUE (id, type, type_id)
);

CREATE TABLE films(
	id INT PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(100) UNIQUE NOT NULL,
	sinopse TEXT,
	date DATE,
	duration TIME,
	classification SMALLINT
);

CREATE TABLE photos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    image_url VARCHAR(255) NOT NULL,
    caption TEXT,
    date DATE
);