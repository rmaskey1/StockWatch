DROP TABLE stock CASCADE;
DROP TABLE watchlist CASCADE;
DROP TABLE "user";

CREATE TABLE stock (
	stock_id INT GENERATED ALWAYS AS IDENTITY,
	stock_code TEXT,
	stock_name TEXT,
	last_price DOUBLE PRECISION,
	price_change DOUBLE PRECISION,
	percent_change DOUBLE PRECISION,
	PRIMARY KEY(stock_id)
);

CREATE TABLE "user" (
	user_id INT GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(60),
	password VARCHAR(60),
	email VARCHAR(60),
	PRIMARY KEY(user_id)
);

CREATE TABLE watchlist (
	user_id INT,
	stock_id INT,
	PRIMARY KEY(user_id, stock_id),
	CONSTRAINT fk_user
		FOREIGN KEY(user_id)
			REFERENCES "user"(user_id),
	CONSTRAINT fk_stock
		FOREIGN KEY(stock_id)
			REFERENCES stock(stock_id)
);