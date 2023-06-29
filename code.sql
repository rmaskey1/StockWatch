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

CREATE TABLE watchlist (
	watchlist_id INT UNIQUE,
	stock_id INT,
	PRIMARY KEY(watchlist_id, stock_id),
	CONSTRAINT fk_stock
		FOREIGN KEY(stock_id)
			REFERENCES stock(stock_id)
);

CREATE TABLE "user" (
	user_id INT GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(60),
	password VARCHAR(60),
	email VARCHAR(60),
	watchlist_id INT,
	PRIMARY KEY(user_id),
	CONSTRAINT fk_watchlist
		FOREIGN KEY(watchlist_id)
			REFERENCES watchlist(watchlist_id)
);

