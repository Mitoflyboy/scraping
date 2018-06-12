select
property_id
,max(ext_at)
,arr_dt
,dep_dt
,book_days
from stayzdb.stayz_bookings
where property_id = 9168471
group by 1,3,4,5
order by arr_dt asc
;


-- Step 1 - Get all the extracts for the earliest date
select 
	*
from
	stayzdb.stayz_bookings
where
	ext_at = '2018-04-06'
	and property_id = 9168471
group by 1,2,3,4,5
order by arr_dt asc
;