
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

import glob, os


# In[2]:


#date_str = datetime.datetime.now().strftime("%Y-%m-%d")
#date_str = '2018-03-12'

#js = pd.read_json('/Users/taj/GitHub/scraping/stayz/WebData/nsw_calendar/stayz_calendar_' + date_str + '.json')

#js = js.reset_index(drop=True)
#js = js.set_index('property_id')

# Change values of -1.0 into NaN for stats analysis
#js.loc[js['review_count'] == -1.0, 'review_count'] = np.nan
#js.loc[js['review_value'] == -1.0, 'review_value'] = np.nan


# In[3]:


#js.head()


# In[4]:







os.chdir("/Users/taj/GitHub/scraping/stayz/WebData/nsw_calendar")


#for file in glob.glob("*2018-05-20.json"):

for file in glob.glob("*.json.zip"):
#for file in glob.glob("stayz_calendar_9168471.json"):


    print("Filename: " + file)

    first_page = True

    # THIS IS NOT TRUE!!!!
    # GET THE date from the filename, or the ext_at field??
    #d = datetime.date.today()
    #mr = monthrange(d.year, d.month )

    #cur_month = d.month
    #cur_year = d.year


    js = pd.read_json('/Users/taj/GitHub/scraping/stayz/WebData/nsw_calendar/' + file)

    fp = open('/Users/taj/GitHub/scraping/stayz/WebData/nsw_processed_calendar/' + file + '_proc.json', 'w')


    for index, row in js.iterrows():   
        
        all_months = {}
        
        #cur_month = d.month

        raw_cal = "<html><body><table>" + row['calendar'] + "</table></body></html>"

        extracted_date = row['ext_at']

        #print("Extracted Date: " + extracted_date.strftime("%Y-%m-%d") )

        cur_year = extracted_date.year
        cur_month = extracted_date.month
        
        
        soup = BeautifulSoup(raw_cal,'lxml') # Parse the HTML as a string
        soup_tables = soup.findAll('tbody')# Grab the first table
        
        
        month_tb_count = 1

        for month_tb in soup_tables:
     
            cells = month_tb.findAll("td")

            # Missing the first table??

            #print("Extracting data for date:" + cur_month)
            
            for td in cells:
                try:
                    day_val = int(td.text)

                    date_full = datetime.date(cur_year,cur_month,day_val)

                    #print("Full date: " + date_full.strftime("%Y-%m-%d"))

                    m1 = None
                    m2 = None
                    m3 = None
                    m4 = None

                    #----------------------------------------------------------
                    # Check if DEP and ARR can both be on the same day
                    # for consecutive bookings?

                    # If its an unavailable date then mark: 
                    # Unavailable means this is the middle of a booking.
                    m1 = re.search('c-calendar--unavailable', str(td))

                    # Want to include all the bookings for the month, since can only see the actuall bookings on the last day of month!

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


        # Keep the extracted date variable as well

        cal_details = {}
        cal_details['property_id'] = row['property_id']
        cal_details['calendar'] = all_months
        cal_details['ext_at'] = str(row['ext_at'])

        #print("Found details:" + str(cal_details))
        
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


#------------------------------




