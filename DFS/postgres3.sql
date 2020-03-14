-- total participation and key constraints between orders and delivers is enforced in the front end

drop table IF EXISTS Users CASCADE;
drop table IF EXISTS FDS_Manager CASCADE;
drop table IF EXISTS FDS_Promo CASCADE;
drop table IF EXISTS Restaurant CASCADE;
drop table IF EXISTS Promotion CASCADE;
drop table IF EXISTS Food CASCADE;
drop table IF EXISTS Customer CASCADE;
drop table IF EXISTS Contain CASCADE;
drop table IF EXISTS Orders CASCADE;
drop table IF EXISTS Reviews CASCADE;
drop table IF EXISTS Delivery_Staff CASCADE;
drop table IF EXISTS Delivers CASCADE;
drop table IF EXISTS Part_Time CASCADE;
drop table IF EXISTS Full_Time CASCADE;
drop table IF EXISTS WWS CASCADE;
drop table IF EXISTS MWS CASCADE;
drop table IF EXISTS CreditCard CASCADE;

CREATE TABLE Users (
	uname varchar(100) PRIMARY KEY,
	password varchar(100)
);

INSERT INTO Users values
	('Restaurant1','password'), ('Restaurant2','password'), ('Restaurant3','password'),
	('Customer1', 'password'),('Customer2', 'password'),('Customer3', 'password'), 
	('PartTime1', 'password'),('PartTime2', 'password'),('FullTime1', 'password'),('FullTime2', 'password'),
    ('Manager', 'password');

CREATE TABLE Restaurant (
	uname varchar(100) PRIMARY KEY References Users ON DELETE CASCADE,
	rname varchar(100) NOT NULL UNIQUE,
	address varchar(100) NOT NULL,
	min_amt numeric NOT NULL
);

INSERT INTO Restaurant values
	('Restaurant1', 'Kenki Sushi','NUS',20),
	('Restaurant2', 'Tin Tai Feng','NTU',30),
	('Restaurant3', 'Prada Wala','SMU',20);


CREATE TABLE Promotion (
	promoid varchar(10) PRIMARY KEY,
	start_date date NOT NULL,
	end_date date NOT NULL,
	message varchar,
	runame varchar(100),
	FOREIGN KEY(runame) REFERENCES Restaurant(uname) ON DELETE CASCADE
);

INSERT INTO Promotion values
	('promo1', '2020-01-01', '2020-01-02', 'free delivery', 'Restaurant1'),
	('promo2', '2020-01-02', '2020-01-03', '10% off', 'Restaurant2'),
	('promo3', '2020-01-03', '2020-01-04', '20% off', 'Restaurant3');

CREATE TABLE Food (
	runame varchar(100),
	fname varchar(100),
	availability boolean DEFAULT false,
	price numeric NOT NULL,
	order_limit numeric,
	category varchar(100),
	PRIMARY KEY (runame, fname),
	FOREIGN KEY (runame) REFERENCES Restaurant(uname) ON DELETE CASCADE
);

INSERT INTO Food values 
	('Restaurant1','Sushi',true,20,10,'Japanese'),('Restaurant1','Ramen',true,30,5,'Japanese'), ('Restaurant1','Mochi',true,10,10,'Dessert'),
	('Restaurant2','Chicken Rice',true,10,10,'Chinese'), ('Restaurant2','Dim Sum',true,30,10,'Chinese'), ('Restaurant2','Hokkien Mee',true,40,10,'Chinese'), 
	('Restaurant2','Chicken Chop',true,50,10,'Western'), ('Restaurant2','Nasi Lemak',true,20,10,'Malay'),
	('Restaurant3','Roti Prata',true,10,10,'Indian');

CREATE TABLE Customer (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	cname varchar(100) NOT NULL,
	points numeric
);

INSERT INTO Customer values 
	('Customer1', 'Abby', 10),
	('Customer2', 'Bob', 20),
	('Customer3', 'Cassey', 5);

CREATE TABLE CreditCard (
	uname varchar(100),
	ccNumber varchar NOT NULL,
	cardType varchar NOT NULL,
	PRIMARY KEY(uname, ccNumber) ,
	FOREIGN KEY(uname) REFERENCES Customer(uname) ON DELETE CASCADE
);

INSERT INTO CreditCard values
	('Customer1', '123456789', 'POSB'),
	('Customer1', '999999999', 'DBS'),
	('Customer2', '000000000', 'DBS');

CREATE TABLE Orders (
	orderId varchar PRIMARY KEY,
	cuname varchar(100) REFERENCES Customer(uname) ON DELETE CASCADE,
	payment_type varchar NOT NULL,
	deliveryAddress varchar NOT NULL,
	is_delivered boolean DEFAULT false,
	order_date date,
	order_time time,
	deliveryFee numeric NOT NULL,
	foodCost numeric NOT NULL,
	promoCode varchar
);

INSERT INTO Orders values
	('1','Customer1', 'Cash', 'Blk 123 Serangoon Ave 3 #01-01', true, '2020-01-01', '09:01:01', 5,10, null),
	('2','Customer2', 'Credit Card', 'Blk 456 Serangoon Ave 10 #01-01', true, '2020-02-01', '10:01:01', 5,20, null);

CREATE TABLE Reviews (
	orderId varchar REFERENCES Orders(orderId) ON DELETE CASCADE,
	review varchar,
	PRIMARY KEY(orderId)
);

CREATE TABLE Contain (
	orderId varchar,
	runame varchar(100),
	fname varchar(100),
    quantity varchar(100),
	PRIMARY KEY(orderId, runame, fname),
	FOREIGN KEY(orderId) REFERENCES Orders,
	FOREIGN KEY(runame, fname) REFERENCES Food	
);

INSERT INTO Contain values
	('1','Restaurant1', 'Sushi', '1'),
	('1','Restaurant1', 'Mochi', '1'),
	('1','Restaurant1', 'Ramen', '1'),
	('2','Restaurant2', 'Dim Sum', '1');

CREATE TABLE Delivery_Staff (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	dname varchar(100) NOT NULL,
	avg_rating numeric,
	flatRate numeric
);

INSERT INTO Delivery_Staff values
	('PartTime1', 'Don', 5.0,'3'),
	('PartTime2', 'Esther', 4.5,'3'),
	('FullTime1', 'Faith', 4.0,'4'),
	('FullTime2', 'Glenn', 4.7,'4');

CREATE TABLE Delivers ( 
	orderId varchar PRIMARY KEY,
	duname varchar(100) REFERENCES Delivery_Staff(uname), 
	rating numeric,
	depart_restaurant time,
	arrive_restaurant time,
	depart_customer time,
	arrive_customer time,
	FOREIGN KEY(orderId) REFERENCES Orders
);

INSERT INTO Delivers values
	('1','PartTime1', 5.0, '09:10:00', '09:20:00', '09:25:00', '09:35:00'), 
	('2','PartTime2', 5.0, '10:10:00', '10:20:00', '10:25:00', '10:35:00');
	
CREATE TABLE Part_Time (
	duname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff(uname) ON DELETE CASCADE
);

INSERT INTO Part_Time values
	('PartTime1'), ('PartTime2'); 
	
CREATE TABLE Full_Time (
	duname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff(uname) ON DELETE CASCADE
);

INSERT INTO Full_Time values
	('FullTime1'), ('FullTime2');

CREATE TABLE WWS (
	wws_serialNum varchar NOT NULL,
	duname varchar(100) REFERENCES Part_Time ON DELETE CASCADE,
	shift_date date NOT NULL,
	shift_day varchar NOT NULL,
	start_hour time,
	end_hour time,
	PRIMARY KEY (duname, wws_serialNum)
);

INSERT INTO WWS values
	('1','PartTime1', '2020-01-01', 'Wednesday', '09:00:00', '13:00:00'), 
	('2','PartTime1', '2020-01-01', 'Wednesday', '14:00:00', '18:00:00'), 
	('3','PartTime1', '2020-01-01', 'Thursday', '19:00:00', '23:00:00'), 
	('1','PartTime2', '2020-02-01', 'Thursday', '10:00:00', '13:00:00'), 
	('2','PartTime2', '2020-02-01', 'Thursday', '14:00:00', '18:00:00'),
	('3','PartTime2', '2020-02-01', 'Thursday', '19:00:00', '23:00:00'); 

CREATE TABLE MWS (
	mws_serialNum varchar NOT NULL,
	duname varchar(100) REFERENCES Full_Time ON DELETE CASCADE,
	work_month varchar NOT NULL,
	day_option numeric NOT NULL,
	shift numeric NOT NULL,
	work_year numeric NOT NULL,
	PRIMARY KEY (duname, mws_serialNum)
);

INSERT INTO MWS values
	('1','FullTime1', 'January', 1, 4, 2020),
	('2','FullTime2', 'January', 4, 1, 2020);

CREATE TABLE FDS_Manager (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	mname varchar(100) NOT NULL
);

INSERT INTO FDS_Manager values
	('Manager', 'Bob'); 