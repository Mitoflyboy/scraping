
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
import datetime
import re
import lxml
from bs4 import BeautifulSoup
import json
from calendar import monthrange
import numpy as np


# In[2]:


#date_str = datetime.datetime.now().strftime("%Y-%m-%d")
date_str = '2018-03-12'

js = pd.read_json('/Users/taj/GitHub/scraping/stayz/WebData/nsw_calendar/stayz_calendar_' + date_str + '.json.zip')

#js = js.reset_index(drop=True)
#js = js.set_index('property_id')

# Change values of -1.0 into NaN for stats analysis
#js.loc[js['review_count'] == -1.0, 'review_count'] = np.nan
#js.loc[js['review_value'] == -1.0, 'review_value'] = np.nan


# In[3]:


js.head()


# In[4]:


d = datetime.date.today()
mr = monthrange(d.year, d.month )

cur_month = d.month
cur_year = d.year


first_page = True



fp = open('/Users/taj/GitHub/scraping/stayz/WebData/nsw_processed_calendar/stayz_processed_calendar_' + date_str + '.json', 'w')


for index, row in js.iterrows():   
    
    all_months = {}
    
    cur_month = d.month

    raw_cal = "<html><body><table>" + row['calendar'] + "</table></body></html>"
    
    
    soup = BeautifulSoup(raw_cal,'lxml') # Parse the HTML as a string
    soup_tables = soup.findAll('tbody')# Grab the first table
    
    
    month_tb_count = 1

    for month_tb in soup_tables:
 
        cells = month_tb.findAll("td")
        
        for td in cells:
            try:
                day_val = int(td.text)

                date_full = datetime.date(cur_year,cur_month,day_val)

                m1 = None
                m2 = None
                m3 = None
                m4 = None

                #----------------------------------------------------------
                # Check if DEP and ARR can both be on the same day
                # for consecutive bookings?

                # If its an unavailable date then mark: 
                m1 = re.search('c-calendar--unavailable', str(td))

                if m1 is not None:
                    all_months[str(date_full)] = 'UVL' # Unavailable day

                # If its an unavailable date then mark: 
                m2 = re.search('c-calendar--arrival-day', str(td))

                if m2 is not None:
                    all_months[str(date_full)] = 'ARR' # Arrival day

                # If its an unavailable date then mark: 
                m3 = re.search('c-calendar--departure-day', str(td))

                if m3 is not None:
                    all_months[str(date_full)] = 'DEP' # Departure day

                m4 = re.search('c-calendar--available', str(td))
                if m4 is not None:
                    all_months[str(date_full)] = 'AVL' # Available day


            except ValueError:
                day_val = None

        # Move to the next month
        cur_month += 1
        month_tb_count += 1

    
    cal_details = {}
    cal_details['property_id'] = row['property_id']
    cal_details['calendar'] = all_months
    
    if first_page is True:
        fp.write('[\n')
        first_page = False
    else:
        fp.write('\n,')
        
    # Write the data to JSON
    json.dump(cal_details, fp)


    
# Close out the JSON format
fp.write('\n]')    

# Tidy up
fp.close()


# In[5]:


# Open the Processed Calendar file
p = pd.read_json('/Users/taj/GitHub/scraping/stayz/WebData/stays_processed_calendar/stayz_processed_calendar_' + date_str + '.json')
p.head()


# In[6]:


# Open the file for writing out the bookings details:
fp = open('/Users/taj/GitHub/scraping/stayz/WebData/nsw_bookings/stayz_bookings_' + date_str + '.json', 'w')

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
            booking_days = 0

            # Move to the next day.
            # Breaks if they arrive on the last day of the 6th month!!!
            min_dateIndex += 1
            booking_days += 1
            
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
                booking_days += 1

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

            # Track the total bookings.
            booking_count += booking_days

            # Show the booking details
            booking_detail = {
                'property_id': pid,
                'arr_dt': date_arr,
                'dep_dt': date_dep,
                'book_days': booking_days
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


# In[45]:


# Read the bookings file
b = pd.read_json('/Users/taj/GitHub/scraping/stayz/WebData/stayz_bookings/stayz_bookings_' + date_str + '.json'
                ,convert_dates=['arr_dt','dep_dt'])

# Change the index to property id
b.set_index('property_id',inplace=True)

# Sort the dataset so that all property id bookings are together
b2 = b.sort_index()


# If the booking is greater than 7 days then may not be a customer
# If the booking is greater than 14 days then assume it is blocked out and not a booking
b2['book_type'] = b2['book_days'].map(lambda x: 'Host' if x > 14 else 'Cust')

b3 = b2[b2['book_type'] == 'Cust']

b3.tail(100)


# In[26]:


# Do a scatter plot of distance from sydney vs bookings count???

# Distance vs revenue?
# Distance vs revenue per person (assuming full occupancy)

# Percentage occupancy for the month vs distance
# 30/60/90 day occupancy vs distance (forward bookings)
# Las 30/60/90 day actual occupance vs distance (history bookings)



# In[46]:


# Check a particular property
b4 = b3.loc[9227458]

b4.head()

