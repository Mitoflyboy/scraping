import pandas as pd
import re
import lxml
from bs4 import BeautifulSoup
from datetime import datetime
import json
from calendar import monthrange
import numpy as np

import glob, os





os.chdir("/Users/taj/GitHub/scraping/stayz/WebData/nsw_processed_calendar")

#for file in glob.glob("*.json"):

for file in glob.glob("*_9168471.json_proc.json"):


    print("Filename: " + file)


    # Open the Processed Calendar file
    p = pd.read_json('/Users/taj/GitHub/scraping/stayz/WebData/nsw_processed_calendar/' + file )
    p.head()


    # Open the file for writing out the bookings details:
    fp = open('/Users/taj/GitHub/scraping/stayz/WebData/nsw_bookings/stayz_bookings_' + file, 'w')

    first_page = True

    # Iterate over each entry in the Processed Calendar file:
    for index, row in p.iterrows():  
        
        c = row['calendar']
        
        pid = row['property_id']
        
        days_count = 0
        avl_count = 0
        dep_count = 0
        arr_count = 0
        uvl_count = 0

        booking_count = 0

        dates = list(c.keys())

        min_dateIndex = 0
        max_dateIndex = len(dates)
     
        while (min_dateIndex < max_dateIndex):

            date = dates[min_dateIndex]
            status = c[date]

            # Count the total number of days
            days_count += 1

            if( status == 'AVL'):
                avl_count += 1

            if( status == 'ARR'):
                arr_count += 1
                # Iterate while the days are Unavailble until we find a Departure

                # Keep the arrival date:
                date_arr = date

                # Reset the count for this booking
                # Has to be at least one nights stay!
                booking_days = 1

                # Move to the next day.
                # Breaks if they arrive on the last day of the 6th month!!!
                min_dateIndex += 1
                #booking_days += 1
                
                if(min_dateIndex < max_dateIndex): 
                    date = dates[min_dateIndex]
                    status = c[date]
                else:
                    date = None
                    status = None
                
                # If only one night stay. be careful how to increment booking_days???
                while(( status != 'DEP') & (min_dateIndex < max_dateIndex)):
                    date = dates[min_dateIndex]
                    status = c[date]

                    # Departure date doesnt count as a booked date, but as an available date
                    #booking_days += 1

                    days_count += 1

                    min_dateIndex += 1
                    

                # Add in the last day
                avl_count += 1
                days_count += 1



                # Get the departure day details??
                
                if(min_dateIndex >= max_dateIndex): 
                    # Booking runs over the end of the month into the 7th month, which we dont track
                    # Ignore this booking or just track to the end of the month?
                    date_dep = None
                else:
                    date_dep = date


                # Calculate the days based on the dates

                #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

                booking_days = datetime.strptime(date_dep,'%Y-%M-%d') - datetime.strptime(date_arr,'%Y-%M-%d')

                # Track the total bookings.
                #booking_count += booking_days

                # Keep the date the calendar was extracted
                ext_at = str(row['ext_at'])

                # Show the booking details
                booking_detail = {
                    'property_id': pid,
                    'ext_at' : ext_at,
                    'arr_dt': date_arr,
                    'dep_dt': date_dep,
                    'book_days': str(booking_days.days)
                }

                if first_page is True:
                    fp.write('[\n')
                    first_page = False
                else:
                    fp.write('\n,')

                json.dump(booking_detail, fp)        

            if( status == 'UVL'):
                uvl_count += 1

            min_dateIndex += 1

    # Close off the JSON
    fp.write(']')

    #print("Total days: " + str(days_count))
    #print("Available days: " + str(avl_count))
    #print("Departure days: " + str(dep_count))
    #print("Arrival days: " + str(arr_count))
    #print("Booked days: " + str(booking_count))
    #print("Unavailable days: " + str(uvl_count))
    #print("Total check: " + str(avl_count + booking_count + uvl_count))

    # Tidy up file handles
    fp.close()



# In[26]:


# Do a scatter plot of distance from sydney vs bookings count???

# Distance vs revenue?
# Distance vs revenue per person (assuming full occupancy)

# Percentage occupancy for the month vs distance
# 30/60/90 day occupancy vs distance (forward bookings)
# Las 30/60/90 day actual occupance vs distance (history bookings)
