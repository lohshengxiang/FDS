-- total participation and key constraints between orders and delivers is enforced in the front end

drop table IF EXISTS Users CASCADE;
drop table IF EXISTS Restaurant CASCADE;
drop table IF EXISTS Promotion CASCADE;
drop table IF EXISTS Food CASCADE;
drop table IF EXISTS Customer CASCADE;
drop table IF EXISTS Contain CASCADE;
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
	values ('Restaurant1','password'),('Restaurant2','password'),('Restaurant3','password'),
	('Customer1', 'password'),('Customer2', 'password'),('Customer3', 'password'), 
	('DeliveryStaff1', 'password'),('DeliveryStaff2', 'password'),('DeliveryStaff3', 'password'),('DeliveryStaff4', 'password'),
    ('Manager', 'password');

CREATE TABLE Restaurant (
	uname varchar(100) PRIMARY KEY References Users ON DELETE CASCADE,
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
	message varchar,
	runame varchar(100),
	FOREIGN KEY(runame) REFERENCES Restaurant(uname) ON DELETE CASCADE
);

insert into Promotion
	values ('promo1', '2020-01-01', '2020-01-02', 'free delivery', 'Restaurant1'),
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

insert into Food
	values ('Restaurant1','Sushi',true,20,10,'Japanese'),('Restaurant1','Ramen',true,30,10,'Japanese'),
	('Restaurant1','Mochi',true,10,10,'Dessert'),('Restaurant2','Chicken Rice',true,10,10,'Chinese'),
	('Restaurant2','Dim Sum',true,30,10,'Chinese'), ('Restaurant2','Hokkien Mee',true,40,10,'Chinese'),
	('Restaurant3','Roti Prata',true,10,10,'Indian'),('Restaurant2','Chicken Chop',true,50,10,'Western'),
	('Restaurant2','Nasi Lemak',true,20,10,'Malay');

CREATE TABLE Customer (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	cname varchar(100) NOT NULL,
	points numeric
);

insert into Customer
	values ('Customer1', 'Abby', 10),
	('Customer2', 'Bob', 20),
	('Customer3', 'Cassey', 5);

CREATE TABLE Orders (
	cuname varchar(100) REFERENCES Customer(uname) ON DELETE CASCADE,
	payment_type varchar NOT NULL,
	total_cost numeric NOT NULL,
	address varchar NOT NULL,
	is_delivered boolean DEFAULT false,
	review varchar,
	order_date date,
	order_time time, 
	PRIMARY KEY(cuname, order_date, order_time)
);

insert into Orders
	values ('Customer1', 'Cash', 60, 'Blk 123 Serangoon Avenue 3 #01-01', true, '', '2020-01-01', '09:01:01'),
	('Customer2', 'Credit Card', 30, 'Blk 456 Serangoon Avenue 10 #01-01', true, '', '2020-02-01', '10:01:01');

CREATE TABLE Contain (
	cuname varchar(100),
	order_date date,
	order_time time,
	runame varchar(100),
	fname varchar(100),
    quantity varchar(100),
	PRIMARY KEY(cuname, order_date, order_time, runame, fname),
	FOREIGN KEY(cuname, order_date, order_time) REFERENCES Orders,
	FOREIGN KEY(runame, fname) REFERENCES Food	
);

insert into Contain
	values ('Customer1', '2020-01-01', '09:01:01', 'Restaurant1', 'Sushi', '1'),
	('Customer1', '2020-01-01', '09:01:01', 'Restaurant1', 'Mochi', '1'),
	('Customer1', '2020-01-01', '09:01:01', 'Restaurant1', 'Ramen', '1'),
	('Customer2', '2020-02-01', '10:01:01', 'Restaurant2', 'Dim Sum', '1');

CREATE TABLE Delivery_Staff (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	dname varchar(100) NOT NULL,
	avg_rating numeric
);

insert into Delivery_Staff
	values ('DeliveryStaff1', 'Don', 5.0),
	('DeliveryStaff2', 'Esther', 4.5),
	('DeliveryStaff3', 'Faith', 4.0),
	('DeliveryStaff4', 'Glenn', 4.7);

CREATE TABLE Delivers (
	order_date date, 
	order_time time, 
	duname varchar(100) REFERENCES Delivery_Staff(uname), 
	cuname varchar(100),
	rating numeric,
	depart_restaurant time,
	arrive_restaurant time,
	depart_customer time,
	arrive_customer time,
	PRIMARY KEY(cuname, order_date, order_time),
	FOREIGN KEY(cuname, order_date, order_time) REFERENCES Orders
);

insert into Delivers
	values ('2020-01-01', '09:01:01', 'DeliveryStaff1', 'Customer1', 5.0, '09:10:00', '09:20:00', '09:25:00', '09:35:00'), 
	('2020-02-01', '10:01:01', 'DeliveryStaff2', 'Customer2', 5.0, '10:10:00', '10:20:00', '10:25:00', '10:35:00');
	
CREATE TABLE Part_Time (
	duname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff(uname) ON DELETE CASCADE
);

insert into Part_Time 
	values ('DeliveryStaff1'), ('DeliveryStaff2'); 
	
CREATE TABLE Full_Time (
	duname varchar(100) PRIMARY KEY REFERENCES Delivery_Staff(uname) ON DELETE CASCADE
);

insert into Full_Time
	values ('DeliveryStaff3'), ('DeliveryStaff4');

CREATE TABLE WWS (
	duname varchar(100) REFERENCES Part_Time ON DELETE CASCADE,
	shift_date date NOT NULL,
	shift_day varchar NOT NULL,
	start_hour time,
	end_hour time,
	PRIMARY KEY (duname, shift_date, start_hour, end_hour)
);

insert into WWS 
	values ('DeliveryStaff1', '2020-01-01', 'Wednesday', '09:00:00', '13:00:00'), 
	('DeliveryStaff1', '2020-01-01', 'Wednesday', '14:00:00', '18:00:00'), 
	('DeliveryStaff1', '2020-01-01', 'Thursday', '19:00:00', '23:00:00'), 
	('DeliveryStaff2', '2020-02-01', 'Thursday', '10:00:00', '13:00:00'), 
	('DeliveryStaff2', '2020-02-01', 'Thursday', '14:00:00', '18:00:00'),
	('DeliveryStaff2', '2020-02-01', 'Thursday', '19:00:00', '23:00:00'); 

CREATE TABLE MWS (
	duname varchar(100) REFERENCES Full_Time ON DELETE CASCADE,
	work_month varchar NOT NULL,
	day_option numeric NOT NULL,
	shift numeric NOT NULL,
	work_year numeric NOT NULL,
	PRIMARY KEY (duname, work_month, work_year)
);

insert into MWS
	values ('DeliveryStaff3', 'January', 1, 4, 2020),
	('DeliveryStaff4', 'January', 4, 1, 2020);

CREATE TABLE FDS_Manager (
	uname varchar(100) PRIMARY KEY REFERENCES Users ON DELETE CASCADE,
	mname varchar(100) NOT NULL
);

insert into FDS_Manager 
	values ('Manager', 'Bob'); 