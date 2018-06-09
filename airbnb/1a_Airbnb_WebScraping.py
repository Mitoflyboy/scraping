
# coding: utf-8

# In[1]:


import sysconfig
import os
import numpy as np
import pandas as pd
import json
import distutils
import scrapy
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
from datetime import datetime, timedelta
import math

# approximate radius of earth in km
R = 6373.0



# In[2]:


class Stayz_Listing(scrapy.Item):
    property_id = scrapy.Field()
    page_nbr = scrapy.Field()
    page_pos = scrapy.Field()
    scraped_date = scrapy.Field()    
        


# In[3]:
date_str = datetime.now().strftime("%Y-%m-%d")

def get_base_urls(by_area=False):

    # Use the previous days extract to run todays suburbs
    date_str_prev1 = datetime.now() - timedelta(days=1)

    date_str_prev = date_str_prev1.strftime("%Y-%m-%d")

    #date_str ='2018-04-01'

    # Read the data file and display
    nsw_data = pd.read_json('/Users/taj/GitHub/scraping/stayz/WebData/nsw_extract/stayz_nsw_extract_' + date_str_prev + '.json')

    nsw_urls = nsw_data['url']

    # List to keep all the base urls
    base_urls = []

    # If we want the breakdown by individual area then call with by_area = True
    if by_area:

        print("Collecting by individual area...")

        for u in nsw_urls:

            u_s = u.split('/')

            suburb = u_s[-2]
            area = u_s[-3]

            url = 'https://www.stayz.com.au/accommodation/nsw/' + area + '/' + suburb

            if url not in base_urls:
                base_urls.append(url)
    else:
        print("Collecing for whole state of NSW")
        base_urls.append('https://www.stayz.com.au/accommodation/nsw')


    # Find why the others were not identified?? 4k missing??

    #rint(base_urls)
    return base_urls



# In[4]:


# http://www.thecodeknight.com/post_categories/search/posts/scrapy_python

class StayzSpider(scrapy.Spider):
    name = 'stayz_crawler'
    
    # Full scrape - NSW
    #start_urls = ['https://www.stayz.com.au/accommodation/nsw']

    #start_urls = ['https://www.stayz.com.au/accommodation/nsw/south-coast/mollymook'
    #,'https://www.stayz.com.au/accommodation/nsw/sydney/liverpool'
    #,'https://www.stayz.com.au/accommodation/nsw/central-coast/bulli']

    start_urls = get_base_urls(True)
    

    # Check each of the 
    
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
        'FEED_URI': '/Users/taj/GitHub/scraping/stayz/WebData/nsw_extract/c_stayz_nsw_extract_' + datetime.now().strftime("%Y-%m-%d") + '.json' #Used for pipeline 2
    }
    
    url_pages = []
    
    
    
    def parse(self, response):
        
        sel = Selector(response)

        # Get the page number here from the metadata!
        # Just get page number from the URL!
        url = response.url

        # IF it matches page=1 then get the page number
        pn = re.search('\d+', url)

        if pn is None:
            #print("NO PAGE NUMBER FOUND")
            page_nbr = 1

        else:
            #print("Found page: " + pn.group(0))
            page_nbr = pn.group(0)
            
               
        urls = sel.xpath('//section[@class="c-search-results__main"]/div/article/div/div/div/h3/a/@href').extract()

        page_pos = 1
                
        for u in urls:

            # Pass the page number as a parameter. Count the number of items on each page
            request = scrapy.Request('https://www.stayz.com.au'+ u, callback=self.parse_results, meta={'page_nbr': page_nbr, 'page_pos': page_pos } )

            page_pos += 1
            
            yield request
            
        # Get the link to the 'Next' page of listings
        url_pages = sel.xpath('/html/body/div/main/div/section/div/nav/ul/li/a/@href').extract()
        
        if len(url_pages) > 0:
            nextPage = url_pages[-1]
        
            nextPageURL = 'https://www.stayz.com.au'+ nextPage
        
            print("Next URL: " + str(nextPage))


            # Parse the next front page
            request = scrapy.Request(nextPageURL, callback=self.parse, )
        
            yield request
            
    def strip_whitespace(self, st):
    
        st1 = re.sub('\n','',st.string() )
        st2 = re.sub(' +',' ', st1.string() )
        return st2    
                
    def parse_results(self, response):

        # Get the page number details
        n_page_nbr = response.meta['page_nbr']
        n_page_pos = response.meta['page_pos']

        
        # Property ID - unique for each property
        p_id1 = response.selector.xpath('//article/header/ol/li/span/span/text()').extract_first()
        p_id2 = re.sub('\n','',p_id1)
        p_id3 = re.sub(' +',' ', p_id2)
        p_id4 = re.search('\d+',p_id3)
        p_id = p_id4.group(0)
        
        
        print("Scanning Property ID: " + p_id + "-" + response.url)
        
        p = Stayz_Listing()
        p['property_id'] = p_id
        p['scraped_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p['page_nbr'] = n_page_nbr
        p['page_pos'] = n_page_pos
        
        yield p        


process = CrawlerProcess({ 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)' })

process.crawl(StayzSpider) 
process.start()
