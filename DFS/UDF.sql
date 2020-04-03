-- trigger for when a customer adds a rating for delivery staff -> calculate avg driver rating
DROP TRIGGER IF EXISTS update_avgRating ON Delivery_Staff CASCADE;
DROP FUNCTION IF EXISTS calculate_avgRating CASCADE;

CREATE OR REPLACE FUNCTION calculate_avgRating()
RETURNS TRIGGER AS $$ DECLARE newAvg numeric;
BEGIN
RAISE NOTICE 'TRIGGER CALLED';

SELECT AVG(rating) INTO newAvg 
FROM Delivers d
WHERE d.duname = NEW.duname;

UPDATE Delivery_Staff d SET avg_rating = newAvg WHERE d.uname = NEW.duname;
RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_avgRating
AFTER UPDATE ON Delivers
FOR EACH ROW EXECUTE PROCEDURE calculate_avgRating();


-- trigger for when food is delivered, is_delivering = false for Delivery driver
DROP TRIGGER IF EXISTS update_is_delivering ON Delivery_Staff CASCADE;
DROP FUNCTION IF EXISTS set_is_delivering CASCADE;

CREATE OR REPLACE FUNCTION set_is_delivering()
RETURNS TRIGGER AS $$ DECLARE driver_uname varchar;
BEGIN

SELECT d.duname INTO driver_uname
FROM Delivers d JOIN Orders o USING (orderid)
WHERE d.orderid = NEW.orderid
LIMIT 1;


UPDATE Delivery_Staff d SET is_delivering = false WHERE d.uname = driver_uname;
RETURN NULL;
END;
$$ LANGUAGE plpgsql;

 CREATE TRIGGER update_is_delivering
 AFTER UPDATE ON Orders
 FOR EACH ROW EXECUTE PROCEDURE set_is_delivering();

-- trigger to check if order_limit has reached
DROP TRIGGER IF EXISTS check_food_maxLimit ON Orders CASCADE;
DROP FUNCTION IF EXISTS change_availability CASCADE;

CREATE OR REPLACE FUNCTION change_availability()
RETURNS TRIGGER AS $$ DECLARE current_order_limit numeric;
BEGIN

SELECT order_limit INTO current_order_limit
FROM Food f
WHERE f.fname = NEW.fname AND f.runame = NEW.runame;

UPDATE Food f SET order_limit = current_order_limit - NEW.quantity WHERE f.fname = NEW.fname AND f.runame = NEW.runame;
RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_food_maxLimit
AFTER INSERT ON Contain
FOR EACH ROW EXECUTE PROCEDURE change_availability();

INSERT INTO Orders values (10,'Customer1', 'Cash', 'Blk 123 Serangoon Ave 3 #01-01', '530123','North-East', true, '2020-01-03', '09:01:01', 5,180, null);
INSERT INTO contain values (10,'Restaurant1', 'Sushi', '9');
select * from food;
select * from contain;

 -- trigger to ensure orders are not added in between 10pm - 10am
DROP TRIGGER IF EXISTS check_order_timing ON Orders CASCADE;
DROP FUNCTION IF EXISTS order_timing CASCADE;

CREATE OR REPLACE FUNCTION order_timing()
RETURNS TRIGGER AS $$ DECLARE current_orderTime time;
BEGIN

IF NEW.order_time < '10:00:00' OR new.order_time >= '22:00:00' THEN
	RAISE EXCEPTION 'Our delivery service is not available.';
ELSE
	RETURN NEW;
END IF;

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_order_timing
BEFORE INSERT ON Orders
FOR EACH ROW EXECUTE PROCEDURE order_timing();

--test
INSERT INTO Orders values
(10,'Customer1', 'Cash', 'Blk 123 Serangoon Ave 3 #01-01', '530123','North-East', true, '2020-01-03', '10:00:00', 5,20, '10OFF');




--Function to assign workers when order is inserted
DROP TRIGGER IF EXISTS check_if_workers_avail ON Orders CASCADE;
DROP FUNCTION if exists get_workers;
CREATE OR REPLACE FUNCTION get_workers(today_date date, today_time time, today_month text, today_year numeric, day_option1 numeric,
day_option2 numeric, day_option3 numeric, day_option4 numeric, day_option5 numeric, day_option6 numeric, day_option7 numeric, shift1 numeric,
shift2 numeric, shift3 numeric, shift4 numeric)
returns table(available varchar(100)) as $$
	WITH working_pt as (
		SELECT distinct duname from WWS where shift_date = today_date and start_hour < today_time and end_hour > today_time
		), available_pt as (
		SELECT uname from Delivery_Staff where uname in (select duname from working_PT) and is_delivering = false
		), working_ft as (
		SELECT distinct duname from MWS where work_month = today_month and work_year = today_year and day_option in (day_option1, day_option2, day_option3,
		day_option4, day_option5, day_option6, day_option7) and shift in (shift1, shift2, shift3, shift4)
		), available_ft as (
		SELECT uname from Delivery_Staff where uname in (select duname from working_FT) and is_delivering = false
		), available_union as (
		SELECT uname, 1 as ord from available_pt union all SELECT uname, 2 as ord from available_ft
		), orders_today as (
		SELECT a.uname, a.ord , count(*) as order_count from available_union a join 
		(select d.orderid, d.duname from Delivers d join Orders o using (orderId) where o.order_date = today_date) u
		on a.uname = u.duname group by a.uname, a.ord
		) select uname from orders_today order by order_count, ord

$$ language sql;