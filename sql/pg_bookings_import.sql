-- Import CSV data files for the 'stayz_bookings' table
-- Version 0.1
-- Date: 2018-04-19

COPY stayzdb.stayz_bookings FROM '/Users/taj/GitHub/scraping/stayz/WebData/nsw_bookings/test_book_2018-04-17.csv' WITH (FORMAT csv, HEADER);
COMMIT;

select * from stayzdb.stayz_bookings
order by 1,3
;


select property_id, count(*),sum(book_days)
from stayzdb.stayz_bookings
where property_id = 9202601
group by 1
order by 2 desc



-- Cleanup table if required
-- truncate stayzdb.stayz_bookings;
