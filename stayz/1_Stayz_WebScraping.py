
# coding: utf-8

# In[1]:


import sysconfig
import os
import numpy as np
import pandas as pd
import json
import distutils
import scrapy
import datetime
import requests
import json
import logging
import string
import re
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from requests import Request
from math import sin, cos, sqrt, atan2, radians
from decimal import Decimal
import math
from collections import Counter

# approximate radius of earth in km
R = 6373.0



# In[2]:


class Stayz_Listing(scrapy.Item):
    property_id = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    init_price = scrapy.Field()
    guests = scrapy.Field()
    heading = scrapy.Field()
    description_full = scrapy.Field()
    description_wc = scrapy.Field()
    url = scrapy.Field()
    bedrooms = scrapy.Field()
    beds = scrapy.Field()
    bathrooms = scrapy.Field()
    property_type = scrapy.Field()
    reviews = scrapy.Field()
    #rating = scrapy.Field()
    #suburb = scrapy.Field()
    #postcode = scrapy.Field()
    #google_addr = scrapy.Field()
    #house_specs = scrapy.Field()
    scraped_date = scrapy.Field()
    syd_brg_deg = scrapy.Field()
    syd_brg = scrapy.Field()
    syd_dist_km = scrapy.Field()
    
        


# In[3]:


# In[4]:


# http://www.thecodeknight.com/post_categories/search/posts/scrapy_python

class StayzSpider(scrapy.Spider):
    name = 'stayz_crawler'
    
    # Full scrape - NSW
    start_urls = ['https://www.stayz.com.au/accommodation/nsw']

    #start_urls = ['https://www.stayz.com.au/accommodation/nsw/hunter/newcastle/9185654']
    
    # Forbes - has 3 properties on one listing page
    #start_urls = ['https://www.stayz.com.au/accommodation/nsw/explorer-country/forbes']
    
    # Orange - has 122 properties on 3 listing pages
    #start_urls = ['https://www.stayz.com.au/accommodation/nsw/explorer-country/orange/']
    
    #start_urls = ['https://www.stayz.com.au/accommodation/nsw/explorer-country/mudgee'
    #             ,'https://www.stayz.com.au/accommodation/nsw/explorer-country/bathurst'
    #             ,'https://www.stayz.com.au/accommodation/nsw/north-coast/coffs-harbour'
    #             ,'https://www.stayz.com.au/accommodation/nsw/north-coast/port-macquarie']
    
    #start_urls = ['https://www.stayz.com.au/accommodation/nsw/central-coast/gosford/'
    #              ,'https://www.stayz.com.au/accommodation/nsw/explorer-country/orange/'
    #             ]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        #'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, #Used for pipeline 1
        'FEED_FORMAT':'json', # Used for pipeline 2
        'FEED_URI': '/Users/taj/GitHub/scraping/stayz/WebData/nsw_extract/stayz_nsw_extract_' + datetime.datetime.now().strftime("%Y-%m-%d") + '.json' #Used for pipeline 2
    }
    
    url_pages = []


    # Filter the description and get the word count
    def description_word_count(self, text):
    
	    # Cleaning text
	    for char in '-.,\n':
	        text=text.replace(char,' ')
	        
	    # All words lower case
	    text = text.lower()
	    
	    # split returns a list of words delimited by sequences of whitespace (including tabs, newlines, etc, like re's \s) 
	    word_list = text.split()

	    cn = Counter(word_list).most_common()

	    tot = sum(Counter(cn).values())
	    
	    return tot

    
    def calculate_initial_compass_bearing(self, pointA, pointB):
        """
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                      cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        :Parameters:
          - `pointA: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
          - `pointB: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees
        :Returns:
          The bearing in degrees
        :Returns Type:
          float
        """
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])
        
        lon1 = math.radians(pointA[1])
        lon2 = math.radians(pointB[1])

        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        
        
        # Calculate the straight line distance in km
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        syd_distance_km = int(R * c)
        
        
        if compass_bearing >= 0.00 and compass_bearing < 22.50:
            compass_dir = 'N'
        elif compass_bearing >= 22.50 and compass_bearing < 67.5:
            compass_dir = 'NE'
        elif compass_bearing >= 67.5 and compass_bearing < 112.50:
            compass_dir = 'E'
        elif compass_bearing >= 112.5 and compass_bearing < 157.50:
            compass_dir = 'SE'
        elif compass_bearing >= 157.5 and compass_bearing < 202.50:
            compass_dir = 'S'
        elif compass_bearing >= 202.5 and compass_bearing < 247.50:
            compass_dir = 'SW'
        elif compass_bearing >= 247.5 and compass_bearing < 292.50:
            compass_dir = 'W'
        elif compass_bearing >= 292.5 and compass_bearing < 337.50:
            compass_dir = 'NW'
        elif compass_bearing >= 337.5 and compass_bearing <= 360.00:
            compass_dir = 'N'
        else:
            compass_dir = 'UN'

        return (int(compass_bearing), compass_dir, int(syd_distance_km))
    
    def parse(self, response):
        
        sel = Selector(response)
               
        urls = sel.xpath('//section[@class="c-search-results__main"]/div/article/div/div/div/h3/a/@href').extract()
                
        for u in urls:
        
            request = scrapy.Request('https://www.stayz.com.au/'+ u, callback=self.parse_results )
            
            yield request
            
        # Get the link to the 'Next' page of listings
        url_pages = sel.xpath('/html/body/div/main/div/section/div/nav/ul/li/a/@href').extract()
        
        if len(url_pages) > 0:
            nextPage = url_pages[-1]
        
            nextPageURL = 'https://www.stayz.com.au/'+ nextPage
        
            print("Next URL: " + str(nextPage))
        
            yield(scrapy.Request(nextPageURL, callback=self.parse))
            
    def strip_whitespace(self, st):
    
        st1 = re.sub('\n','',st.string() )
        st2 = re.sub(' +',' ', st1.string() )
        return st2    
                
    def parse_results(self, response):
        
        # Property ID - unique for each property
        p_id1 = response.selector.xpath('//article/header/ol/li/span/span/text()').extract_first()
        p_id2 = re.sub('\n','',p_id1)
        p_id3 = re.sub(' +',' ', p_id2)
        p_id4 = re.search('\d+',p_id3)
        p_id = p_id4.group(0)

        # Geographic location - not exact location, within a block of actual
        # Error handling - if no lat/lon specified place in middle of Botany Harbour
        p_lat = response.selector.xpath('//*[@class="c-map__container"]/@lat').extract_first()
        if p_lat is None:
            p_lat = '-33.990'
        p_lng = response.selector.xpath('//*[@class="c-map__container"]/@lng').extract_first() 
        if p_lng is None:
            p_lng = '151.180'

        #print("Distance to Sydney: {0} km" .format(p_syd_distance_km))
        
        p_compass_bearing, p_dir, p_syd_distance_km = self.calculate_initial_compass_bearing((Decimal(-33.990),Decimal(151.180)),(Decimal(p_lat),Decimal(p_lng)))
        #print("Distance: {2} Compass: {0} Heading: {1}" .format(p_compass_bearing, p_dir, p_syd_distance_km))
        

        # House configuration - number of guests
        p_configuration = response.css(".c-facet__label.u-display--block::text").extract_first()
        p_configuration = re.sub('\n','',p_configuration)
        p_configuration = re.sub(' +',' ', p_configuration)
        p_group = re.search('\d+', p_configuration)
        p_guests = p_group.group(0)
        
        p_heading = response.css(".c-heading--brand.u-h2::text").extract_first()
        
        # Property type from the sub-heading - 'House, Mudgee'
        p_pt_1 = response.selector.xpath('///html/body/main/section/div/article/header/p/small/text()').extract_first()
        
        if p_pt_1 is not None:
            p_pt_1 = re.sub('\n','', p_pt_1)
            p_pt_1 = re.sub(' +',' ', p_pt_1)
            if re.search('B&B', p_pt_1):
                p_property_type = 'B&B'
            else:
                p_pt_2 = re.search('\w+',p_pt_1)
                p_property_type = p_pt_2.group(0)
        else:
            p_property_type = 'Unknown'
        
        p_house_specs = response.selector.xpath('//div[@class="c-facets c-facets--inline"]/div/span/span/text()').extract()
        
        # Initialize variables
        n_bedrooms = 0
        n_beds = 0
        n_bathrooms = 0
        
        for j in p_house_specs:
            if re.search('bedroom',j):
                # Extract number of guests
                n_br = re.search('\d+',j)
                n_bedrooms = n_br.group(0)
                
            if re.search('bed[s]?$',j):
                # Extract number of guests
                n_bd = re.search('\d+',j)
                n_beds = n_bd.group(0)
                
            if re.search('bathroom',j):
                # Extract number of guests
                n_bath = re.search('\d+',j)
                n_bathrooms = n_bath.group(0)
                
                
        # The basic price - 'From $xxx per night'        
        p_ip_1 = response.selector.xpath('//header[@class="c-quote__header"]/p/span/span/span[@class="u-h1"]/text()').extract_first()
        
        p_init_price = 0
        
        if p_ip_1 is not None:
            p_ip_3 = p_ip_1.replace(',','')
            p_ip_4 = re.search('\d+',p_ip_3)
            p_init_price = p_ip_4.group(0)
        else:
            p_init_price = 0
        
        # Ratings and reviews
        p_rating = response.selector.xpath('//header[@class="c-reviews__header"]/span/span/span[@class="c-facet__label"]/span/text()').extract_first()
        
        p_r1 = response.selector.xpath('//html/body/main/section/div/article/header/p[2]/span/span[2]/small/text()').extract_first()
        
        # Initialise
        p_reviews = 0
        
        if p_r1 is not None:
            p_r2 = re.sub('\n','',p_r1)
            p_r2 = re.sub(' +',' ',p_r2)
            p_r3 = re.search('\d+', p_r2)
            p_reviews = p_r3.group(0)
        else:
            p_reviews = 0
        
        # Full text of property details
        p_description_full = response.xpath('//div[@id="property-description-body"]/p/text()').extract()

        p_description_text = '\n'.join(p_description_full)

        # Do a word count of the description

        p_description_wc = self.description_word_count(p_description_text)


        # Reverse geocoding on Google API for street address:
        latlng = "" + p_lat + "," + p_lng 
        
        print("Scanning Property ID: " + p_id + "-" + response.url)
        
        p = Stayz_Listing()
        p['property_id'] = p_id
        p['lat'] = p_lat
        p['lng'] = p_lng
        p['guests'] = p_guests
        p['heading'] = p_heading
        p['url'] = response.url
        p['init_price'] = p_init_price
        p['bedrooms'] = n_bedrooms
        p['beds'] = n_beds
        p['bathrooms'] = n_bathrooms
        p['description_full'] = p_description_full
        p['description_wc'] = p_description_wc
        p['property_type'] = p_property_type
        #p['rating'] = p_rating
        p['reviews'] = p_reviews
        #p['suburb'] = p_suburb
        #p['postcode'] = p_postcode
        #p['house_specs'] = p_house_specs
        #p['google_addr'] = google_addr.text
        p['syd_dist_km'] = p_syd_distance_km
        p['syd_brg_deg'] = p_compass_bearing
        p['syd_brg'] = p_dir
        p['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        yield p        


# In[5]:


process = CrawlerProcess({ 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)' })

process.crawl(StayzSpider) 
process.start()

