-- trigger for when a customer adds a rating for delivery staff
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

--select * from get_workers('2020-03-29','15:26:22','March',2020,0,0,3,4,5,6,7,1,0,3,4);

-- UPDATE Delivers SET rating = 3.0 WHERE orderid = 1;
-- SELECT * FROM Delivery_Staff;

-- trigger for when order is submitted -> add a row in Delivers
-- DROP TRIGGER IF EXISTS assign_deliveryStaff ON Delivers CASCADE;
-- DROP FUNCTION IF EXISTS find_deliveryStaff CASCADE;

-- CREATE OR REPLACE FUNCTION find_deliveryStaff()
-- RETURNS TRIGGER AS $$ DECLARE delivery_staff varchar;
-- BEGIN
-- RAISE NOTICE 'TRIGGER CALLED'


-- SELECT duname INTO delivery_staff 
-- FROM WWS w, Delivery_Staff d
-- WHERE w.duname = d.duname AND is_delivering = false AND 
-- NEW.order_date = w.shift_date AND
-- NEW.order_time > w.start_hour AND 
-- NEW.order_time < w.end_hour
-- LIMIT 1;

-- IF delivery_staff IS NULL THEN
-- RAISE NOTICE 'MWS';
-- SELECT duname INTO delivery_staff 
-- FROM MWS m, Delivery_Staff d
-- WHERE m.duname = d.duname AND is_delivering = false AND 
-- NEW.order_date = w.shift_date AND
-- NEW.order_time > w.start_hour AND 
-- NEW.order_time < w.end_hour;

-- INSERT INTO Delivers VALUES (NEW.orderId, NEW.duname, 0, null, null, null, null);
-- RETURN NULL;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER assign_deliveryStaff
-- AFTER INSERT ON Orders
-- FOR EACH ROW EXECUTE PROCEDURE find_deliveryStaff();