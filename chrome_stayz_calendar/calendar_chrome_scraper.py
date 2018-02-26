import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import datetime
import time
import json
import logging



# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

prefs = {"profile.managed_default_content_settings.images":2}
option.add_experimental_option("prefs",prefs)

#driver = webdriver.Chrome(chrome_options=option)

# Create new Instance of Chrome in incognito mode

p_browser = webdriver.Chrome(executable_path='/Users/taj/GitHub/scraping/chrome_stayz_calendar/chromedriver', chrome_options=option)

p_browser.implicitly_wait(1)

# Setup the logging:
logging.basicConfig(filename='/Users/taj/GitHub/scraping/chrome_stayz_calendar/WebData/stayz_log_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") + '.log', level=logging.INFO)
log = logging.getLogger("ex")



#ages = {}
#property_data = {}

#pages[start_url] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")


fp = open('/Users/taj/GitHub/scraping/chrome_stayz_calendar/WebData/stayz_calendar' + datetime.datetime.now().strftime("%Y-%m-%d") + '.json', 'a')



first_page = True

page_number = 1
property_number = 1



# Read the list of URLs from the previously saved input list
with open('/Users/taj/GitHub/scraping/stayz_analysis/WebData/stayz_nsw_extract_2018-02-26_10-23.json') as json_data:
	property_urls = json.load(json_data)

	for p in property_urls:

		# Get the actual page link
		property_url = p['url']

		print("Scanning: " + property_url)

		#property_url = p.get_attribute("href")
		log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Scanning: " + property_url)

		try:
			# Get the property page in the browser
			try:
				p_browser.get(property_url)

				p_id = ''

				# Property ID - unique for each property
				p_id1 = p_browser.find_elements_by_xpath('//article/header/ol/li/span/span')


				p_id1a = [x.text for x in p_id1]
				for p in p_id1a:
					p_id2 = re.sub('\n','',p)
					p_id3 = re.sub(' +',' ', p_id2)
					p_id4 = re.search('\d+',p_id3)
					p_id = p_id4.group(0)

				
				# Get the calenders for all 6 months
				cal = p_browser.find_elements_by_xpath('//div[@id="calendar"]/div/div/table')


				try:
					cal2 = [x.get_attribute('innerHTML') for x in cal]

				except selenium.common.exceptions.StaleElementReferenceException as wde:
					log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : Error getting calendar: " + property_url)
					print(type(wde))
					print(wde.args)
					print(wde)


				try:
					# Make sure get all the 6 months of the calendars which are available
					cal_text = ''
					for c in cal2:
						cal_text = cal_text + c

				except IndexError as ie:
					cal_text = 'Unknown'

				# Number of reviews:
				rc1 = p_browser.find_elements_by_xpath('/html/body/main/section/div/article/header/p[2]/span/span[2]/small')
				try:
					rc_2 = rc1[0].text

					rc_3 = re.search('\d+',rc_2)
					review_count = rc_3.group(0)


				except IndexError as ie:
					review_count = '-1'

				# Check the current rating out of 5
				review_rating = p_browser.find_elements_by_xpath('//*[@id="reviews"]/div[2]/header/span/span/span[2]/span[1]')

				# Find the review which also has the decimal rating. This is the first review
				rev = [x.text for x in review_rating]

				review_value = -1

				for r in rev:

					#print("Review: " + r)

					matchObj = re.match( r'\((\d.\d)\).*', r)

					if matchObj:
						review_value = matchObj.group(1)

				# Write the values to the dictionary:
				#property_data[property_url] = (review_value, cal2[0])
				pd = {
					'property_id' : p_id,
					'ext_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
					'review_value' : review_value,
					'review_count' : review_count,
					#'page_nbr' : page_number,
					#'p_nbr' : property_number,
					'calendar' : cal_text
				}

			except selenium.common.exceptions.TimeoutException as te:
				log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Timed out... skipping " + property_url)
				pd = {
					'property_id' : '0000',
					'ext_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
					'review_value' : '0',
					'review_count' : '0',
					#'page_nbr' : page_number,
					#'p_nbr' : property_number,
					'calendar' : property_url
				}

			#pd[p_id] = ( review_value, review_count, cal_text )
			if first_page is True:
				fp.write('[\n')
				first_page = False
			else:
				fp.write('\n,')

			json.dump(pd, fp)

			property_number += 1


			


			#myfile.write(property_url + ',' + review_value + ',' + cal2[0] + '\n')
		except NameError as wde:
			log.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Error loading page: " + property_url)
			log.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + type(wde))
			log.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + wde.args)
			log.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + wde)



# Close off the JSON
fp.write(']')

# Mark as completed	
log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Completed extract...")

p_browser.close()
