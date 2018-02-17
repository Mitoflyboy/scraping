# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash
import logging
import re
import datetime
import time

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

from lxml import etree
from xml.etree import ElementTree as ET
from scrapy.shell import inspect_response
from scrapy.shell import open_in_browser
from scrapy_splash import SplashRequest
from scrapy.selector import Selector


class StayzCalendarSpider(scrapy.Spider):
    name = "stayzcalendar"
    allowed_domains = ["stayz.com.au"]
    
    start_urls = ['https://www.stayz.com.au/accommodation/nsw/explorer-country/forbes']
    #start_urls = ['https://www.stayz.com.au/accommodation/nsw']


    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        #'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, #Used for pipeline 1
        'FEED_FORMAT':'json', # Used for pipeline 2
        'FEED_URI': 'Data/stayz_calendar' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") + '.json' #Used for pipeline 2
    }
    

    def parse(self, response):
        #url = 'https://www.stayz.com.au/accommodation/nsw/explorer-country/orange/222161'

        #driver = webdriver.PhantomJS()

        sel = Selector(response)
               
        urls = sel.xpath('//section[@class="c-search-results__main"]/div/article/div/div/div/h3/a/@href').extract()

        #print(urls)
                
        for u in urls:
        
            #request = scrapy.Request('https://www.stayz.com.au/'+ u, callback=self.parse_item )
            #print("Scraping: " + u)
            print("Render start:\t\t" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

            #driver.get('https://www.stayz.com.au/'+ u)
            #p_element = driver.find_element_by_id(id_='calendar')

            #print("Calendar:" + p_element)

            # Using Splash to render request:
            yield SplashRequest(url='https://www.stayz.com.au/'+ u, callback=self.parse_item, args={'images': 0})

            #print("Render finished:\t" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

            #yield request
            
        # Get the link to the 'Next' page of listings
        url_pages = sel.xpath('/html/body/div/main/div/section/div/nav/ul/li/a/@href').extract()
        
        if len(url_pages) > 0:
            nextPage = url_pages[-1]
        
            nextPageURL = 'https://www.stayz.com.au/'+ nextPage
        
            print("Next URL: " + str(nextPage))

            print("Yield start:\t\t" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        
            yield(scrapy.Request(nextPageURL, callback=self.parse))
            



        

    def parse_item(self, response):
        
        #time.sleep(0.25)

        
        #if ( open_in_browser(response) ):
        
        #assert ("www.dbcj-avocats.com" in response.body), "XHR request not loaded"

        #time.sleep(0.25)
        
        # Inspect means open in scrapy shell for interactive parsing!
        #inspect_response(response, self)

        print("Scraping: " + response.url )
        print("Scraping started\t: " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

        # Property ID - unique for each property
        p_id1 = response.selector.xpath('//article/header/ol/li/span/span/text()').extract_first()
        p_id2 = re.sub('\n','',p_id1)
        p_id3 = re.sub(' +',' ', p_id2)
        p_id4 = re.search('\d+',p_id3)
        p_id = p_id4.group(0)

        cal = response.selector.xpath('//div[@id="calendar"]/div/div/table').extract_first()

        review_rating = response.selector.xpath('//span[@class="c-facet c-review__rating"]/span/span[@class="c-facet__label"]').extract_first()

        #print(cal)

        #h = html2text.HTML2Text()
        # Ignore converting links from HTML
        #h.ignore_links = True
        #cal2 = h.handle(cal)


        #print("Parsing the HTML table...\n")
        #soup = BeautifulSoup(cal[0])

        #b.close()

        print("Scraping finished:\t" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

        yield {
            'property_id' : p_id,
            'extract_time' : datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'review_rating': review_rating,
            'calendar_raw' : cal
            #'calendar_txt' : cal2
        }