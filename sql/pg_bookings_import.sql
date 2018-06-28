-- Import CSV data files for the 'stayz_bookings' table
-- Version 0.1
-- Date: 2018-04-19



-- Truncate stayzdb.stayz_bookings_load;
-- Truncate stayzdb.stayz_bookings;
-- Truncate stayzdb.stayz_bookings_concat;


select * from stayzdb.stayz_bookings_load

COPY stayzdb.stayz_bookings_load FROM '/Users/taj/GitHub/scraping/stayz/WebData/nsw_bookings/csv/all_bookings.csv' WITH (FORMAT csv, HEADER);
COMMIT;


-- Check the loaded rows
SELECT
	count(*)
FROM
	stayzdb.stayz_bookings_load
;

--select * from stayzdb.stayz_bookings
--order by 1,3
--;


select * from stayzdb.stayz_bookings_load 
where property_id = 9062114
group by 1,2,3,4,5



-- Get the original all data rows
select *
from stayzdb.stayz_bookings
where property_id = 9136503
order by arr_dt asc, ext_at asc

-- Concatenate where possible
create table stayzdb.stayz_bookings_concat as 
select * from stayzdb.stayz_bookings_load limit 0


TRUNCATE stayzdb.stayz_bookings_concat;

-- Truncate stayzdb.stayz_bookings_concat;
Insert into stayzdb.stayz_bookings_concat
Select
	property_id
	, min(ext_at) as ext_at
	, arr_dt
	, dep_dt
	, book_days
from
	stayzdb.stayz_bookings_load
group by 1,3,4,5
order by arr_dt asc
;

-- Check a property
select * from stayzdb.stayz_bookings_concat
where property_id = 9168471
order by arr_dt asc, ext_at desc
;

-- From the raw data, find the maximum extraction date, and use only those booking values??
Select
	max(ext_at) as last_extract_date
From
	stayzdb.stayz_bookings_load
Where
	property_id = 9168471
	and EXTRACT(MONTH FROM ext_at) = '03'
;

-- Gives the date as 2018-06-23
-- Now get all bookings with that extract date:
Select
	*
From
	stayzdb.stayz_bookings_load
Where
	property_id = 9168471
	and ext_at = '2018-03-31'
	and EXTRACT(MONTH FROM arr_dt) = EXTRACT(MONTH FROM CAST('2018-03-31' as DATE))
Order by arr_dt asc
;

-- For each property_id/month, get the maximum ext_at date


-- Get the unique ext_at months




truncate stayzdb.stayz_extract_dates
;


Insert into stayzdb.stayz_extract_dates
Select
	property_id
	,EXTRACT(MONTH from ext_at) as mth
	,max(ext_at)
From
	stayzdb.stayz_bookings_load
--Where
--	property_id = 9168471
Group by 1,2
;

select * from stayzdb.stayz_extract_dates
limit 10


-- Join it back to the loaded data to get the last records, then sum days by month


Select
	A.property_id
	,EXTRACT(MONTH from A.arr_dt) as Mth
	,sum(A.book_days)
	--,A.*
From
	stayzdb.stayz_bookings_load A
	Inner Join stayzdb.stayz_extract_dates B
	On A.property_id = B.property_id
	And A.ext_at = B.ext_at
	And EXTRACT(MONTH from A.arr_dt) = B.mth
Where
	A.property_id = 9168471
Group By 1,2


create or replace function last_day(date) returns date as 
'select cast(date_trunc(''month'', $1) + ''1 month''::interval as date) - 1'
language sql;

-- Split up the bookings which run over the end of the month into two

TRUNCATE stayzdb.stayz_bookins_month_split
;

INSERT INTO stayzdb.stayz_bookins_month_split
Select
	A.property_id
	--,sum(A.book_days)
	,A.ext_at
	,A.arr_dt
	,A.dep_dt
	,A.book_days
	,(CASE WHEN EXTRACT(MONTH from A.dep_dt) > B.mth THEN 'C' ELSE 'O' END) as calc_status
	,(CASE WHEN EXTRACT(MONTH from A.dep_dt) > B.mth THEN date_part('day',age(last_day(A.arr_dt), A.arr_dt))+1
	 ELSE A.book_days
	 END) as book_days_split
	,B.mth as month_code
From
	stayzdb.stayz_bookings_load A
	Inner Join stayzdb.stayz_extract_dates B
	On A.property_id = B.property_id
	And A.ext_at = B.ext_at
	And EXTRACT(MONTH from A.arr_dt) = B.mth
--Where
--	A.property_id = 9168471

UNION ALL
-- The second month generate the rows for overlapping

Select
	A.*
From
	(
		Select
			A.property_id
			--,sum(A.book_days)
			,A.ext_at
			,A.arr_dt
			,A.dep_dt
			,A.book_days
			,(CASE WHEN EXTRACT(MONTH from A.dep_dt) > B.mth THEN 'C' ELSE 'O' END) as calc_status
			,(CASE WHEN EXTRACT(MONTH from A.dep_dt) > B.mth THEN date_part('day',age(A.dep_dt, cast(date_trunc('month', A.dep_dt) as date)))
			 ELSE A.book_days
			 END) as book_days_split
			,EXTRACT(MONTH from A.dep_dt) as month_code
		From
			stayzdb.stayz_bookings_load A
			Inner Join stayzdb.stayz_extract_dates B
			On A.property_id = B.property_id
			And A.ext_at = B.ext_at
			And EXTRACT(MONTH from A.arr_dt) = B.mth
		--Where
		--	A.property_id = 9168471
	) A

Where
	A.calc_status = 'C'
;



-- Now sum up the dates by month code:


Truncate stayzdb.stayz_bookings_month_sum
;

Insert into stayzdb.stayz_bookings_month_sum
Select
	property_id
	,month_code
	,sum(book_days_split) as days_booked
From
	stayzdb.stayz_bookins_month_split
Group By 1,2
;

-- Select the results ordered by month
Select * from stayzdb.stayz_bookings_month_sum
Where
	property_id  = '9202004' --in(9148674, 9168471, 9169308, 9062114, 9137336, 9168471)
Order by 1,2 asc
;


-- Create the oversize bookings > 14 days in length to ensure they are not part of the calculation
Delete from stayzdb.stayz_bookings_load
Where
	--property_id = '9202004'
	book_days > 14
;


-- Check the oversize bookings before they are deleted
Select * from stayzdb.stayz_bookings_oversize
;

-- Cleanup table if required
-- truncate stayzdb.stayz_bookings;

COPY stayzdb.stayz_bookings_month_sum TO '/Users/taj/GitHub/scraping/stayz_analysis/monthly_bookings.csv' DELIMITER ',' CSV HEADER;



