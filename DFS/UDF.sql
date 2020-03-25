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