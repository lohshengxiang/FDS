drop table IF EXISTS Users CASCADE;
drop table IF EXISTS Restaurant CASCADE;
drop table IF EXISTS Promotion CASCADE;
drop table IF EXISTS Food CASCADE;
drop table IF EXISTS Customer CASCADE;
drop table IF EXISTS Orders CASCADE;
drop table IF EXISTS Delivery_Staff CASCADE;
drop table IF EXISTS Delivers CASCADE;
drop table IF EXISTS Part_Time CASCADE;
drop table IF EXISTS Full_Time CASCADE;
drop table IF EXISTS WWS CASCADE;
drop table IF EXISTS MWS CASCADE;

CREATE TABLE Users (
	uname varchar(100) PRIMARY KEY,
	password varchar(100)
);

insert into Users
	values ('Restaurant1','password'),('Restaurant2','password'),('Restaurant3','password');

CREATE TABLE Restaurant (
	uname varchar(100) PRIMARY KEY References Users,
	rname varchar(100) NOT NULL UNIQUE,
	address varchar(100) NOT NULL,
	min_amt numeric NOT NULL
);

insert into Restaurant
	values ('Restaurant1', 'Restaurant1','NUS',20),
	('Restaurant2', 'Restaurant2','NTU',30),
	('Restaurant3', 'Restaurant3','SMU',20);


CREATE TABLE Promotion (
	promoid varchar(10) PRIMARY KEY,
	start_date date NOT NULL,
	end_date date NOT NULL,
	message varchar
);

CREATE TABLE Food (
	rname varchar(100),
	fname varchar(100),
	availability boolean DEFAULT false,
	price numeric NOT NULL,
	order_limit numeric,
	category varchar(100),
	PRIMARY KEY (rname, fname),
	FOREIGN KEY (rname) REFERENCES Restaurant ON DELETE CASCADE
);

insert into Food
	values ('Restaurant1','Sushi',true,20,10,'Japanese'),('Restaurant1','Ramen',true,30,10,'Japanese'),
	('Restaurant1','Mochi',true,10,10,'Dessert'),('Restaurant2','Chicken Rice',true,10,10,'Chinese'),
	('Restaurant2','Dim Sum',true,30,10,'Chinese'), ('Restaurant2','Soba',true,40,10,'Japanese'),
	('Restaurant3','Roti Prata',true,10,10,'Indian'),('Restaurant3','Chicken Chop',true,50,10,'Western'),
	('Restaurant3','Nasi Lemak',true,20,10,'Malay');

CREATE TABLE Customer (
	uname varchar(100) PRIMARY KEY REFERENCES Users,
	cname varchar(100) NOT NULL,
	points numeric
);

CREATE TABLE Orders (
	cuname varchar(100) REFERENCES Customer(uname) ON DELETE CASCADE,
	rname varchar(100), --error here
	order_time time NOT NULL,
	payment_type varchar NOT NULL,
	total_cost numeric NOT NULL,
	order_date date NOT NULL,
	dropoff varchar NOT NULL,
	is_delivered boolean DEFAULT false,
	review varchar,
	date date NOT NULL,
	time time NOT NULL,
	PRIMARY KEY(cuname, date, time)
);

CREATE TABLE Delivery_Staff (
	uname varchar(100) PRIMARY KEY REFERENCES Users,
	avg_rating numeric
);

CREATE TABLE Delivers (
	duname varchar(100) REFERENCES Delivery_Staff(uname),
	cuname varchar(100),
	rating numeric,
	depart_restaurant time,
	arrive_restaurant time,
	depart_customer time,
	arrive_customer time,
	date date,
	time time,
	FOREIGN KEY (cuname, date, time) REFERENCES Orders,
	PRIMARY KEY (cuname, date, time)
);
	

CREATE TABLE Part_Time (
	uname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff ON DELETE CASCADE
);
	
CREATE TABLE Full_Time (
	uname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff ON DELETE CASCADE
);

CREATE TABLE WWS (
	uname varchar(100) REFERENCES Part_Time ON DELETE CASCADE,
	date date NOT NULL,
	day varchar NOT NULL,
	start_hour time,
	end_hour time,
	PRIMARY KEY (uname, date, start_hour, end_hour)
);

CREATE TABLE MWS (
	uname varchar(100) REFERENCES Part_Time ON DELETE CASCADE,
	month varchar NOT NULL,
	day_option numeric NOT NULL,
	shift numeric NOT NULL,
	year numeric NOT NULL,
	PRIMARY KEY (uname, month, year)
);
