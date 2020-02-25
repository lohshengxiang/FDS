drop table web_user cascade;
drop table orders;
drop table restaurants2;
drop table 

CREATE TABLE web_user(
    username VARCHAR PRIMARY KEY NOT NULL,
    firstName VARCHAR NOT NULL,
    lastName VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE orders(
	orderid INTEGER NOT NULL primary key,
	username VARCHAR NOT NULL references web_user(username),
	food_cost DECIMAL,
	delivery_cost DECIMAL,
	total_cost DECIMAL,
	payment_method VARCHAR NOT NULL,
	order_time timestamp not null,
	rider_depart_to_rest_time timestamp,
	rider_arrive_at_rest_time timestamp,
	rider_depart_to_location timestamp,
	rider_arrive_at_location timestamp
);

CREATE TABLE restaurants2(
	rname varchar not null primary key,
	address varchar not null,
	min_amount decimal,
	order_limit integer
);

CREATE TABLE food2(
	fname varchar not null primary key
);

CREATE TABLE sells2(
	rnmame varchar not null references restaurants2,
	fname varchar not null references food2,
	price decimal not null,
	category varchar,
	availability boolean not null ,
	(rname, fname) primary key
);