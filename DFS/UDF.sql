drop function if exists get_orders;

create or replace function get_orders(username varchar(100)) 
	returns setof Orders as 
	$$

	select * from Orders where cuname = username;

	$$ language sql;