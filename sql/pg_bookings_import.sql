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
	and EXTRACT(MONTH FROM ext_at) = '05'
;

-- Gives the date as 2018-05-28
-- Now get all bookings with that extract date:


-- Identify duplicates and take the latest values
Select
	A.*
	,B.ext_at
	,B.arr_dt
	,B.dep_dt
	,B.book_days
	,RANK() OVER (PARTITION BY A.property_id ORDER BY A.arr_dt desc, A.dep_dt desc)
From
	stayzdb.stayz_bookings_concat A
	, stayzdb.stayz_bookings_concat B
Where
	A.property_id = B.property_id
	And (A.arr_dt, A.dep_dt) OVERLAPS (B.arr_dt,B.dep_dt)
	And ((A.arr_dt <> B.arr_dt) OR (A.dep_dt <> B.dep_dt))
	And A.property_id = 9136503

-- If dates overlap then take this as a modification, and get the latest values based on ext_at date



-- Check the final result
select property_id, count(*),sum(book_days)
from stayzdb.stayz_bookings
where property_id = 9136503
group by 1
order by 2 desc

-- Cleanup table if required
-- truncate stayzdb.stayz_bookings;
