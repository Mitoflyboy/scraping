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

browser = webdriver.Chrome(executable_path='/Users/taj/GitHub/scraping/chrome_stayz_calendar/chromedriver', chrome_options=option)
p_browser = webdriver.Chrome(executable_path='/Users/taj/GitHub/scraping/chrome_stayz_calendar/chromedriver', chrome_options=option)


# Setup the logging:
logging.basicConfig(filename='/Users/taj/GitHub/scraping/chrome_stayz_calendar/WebData/stayz_log_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") + '.log', level=logging.INFO)
log = logging.getLogger("ex")


# Go to desired website
#browser.get("https://github.com/TheDancerCodes")



#urls = sel.xpath('//section[@class="c-search-results__main"]/div/article/div/div/div/h3/a/@href').extract()

#browser = webdriver.Chrome(executable_path='/Users/taj/Documents/Tims Documents/Jupyter/stayz_calendar/chromedriver', chrome_options=option)

#cal = browser.find_elements_by_xpath('//div[@id="calendar"]/div/div/table')


# Wait 20 seconds for page to load
#timeout = 10
#try:
	# Wait until the final element [Avatar link] is loaded.
	# Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
	# the last things to be loaded.
#    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='avatar width-full rounded-2']")))
#except TimeoutException:
#    print("Timed out waiting for page to load")
#    browser.quit()

# Get all of the titles for the pinned repositories
# We are not just getting pure titles but we are getting a selenium object
# with selenium elements of the titles.




#with open('WebData/stayz_calendar' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") + '.txt', "a") as myfile:

# -------------------------------------------------------------------------------
# Orange: 122 listings over 3 pages
# - https://www.stayz.com.au/accommodation/nsw/explorer-country/orange/
#
# Forbes: 3 listings over 1 page
# - https://www.stayz.com.au/accommodation/nsw/explorer-country/forbes

# Full extract 18k properties in nsw
# 'https://www.stayz.com.au/accommodation/nsw'

start_url = 'https://www.stayz.com.au/accommodation/nsw/'

browser.get(start_url)

pages = {}
property_data = {}

pages[start_url] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")



# Get the link to the 'Next' page of listings
url_pages = browser.find_elements_by_xpath('/html/body/div/main/div/section/div/nav/ul/li/a[@href]')


fp = open('/Users/taj/GitHub/scraping/chrome_stayz_calendar/WebData/stayz_calendar' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") + '.json', 'w')

fp.write('[\n')

first_page = True

page_number = 1
property_number = 1



if len(url_pages) > 0:
	nextPage = url_pages[-1]

	nextPageURL = nextPage.get_attribute("href")

	if nextPageURL in pages:
		log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Already scanned the next page... quit")

		b_nextPage = False
	else:
		b_nextPage = True


	#print("Next Page: " + str(nextPage))
else:
	b_nextPage = False


while( b_nextPage ):

	# Get the link to the 'Next' page of listings
	url_pages = browser.find_elements_by_xpath('/html/body/div/main/div/section/div/nav/ul/li/a[@href]')


	if len(url_pages) > 0:
		nextPage = url_pages[-1]



		nextPageURL = nextPage.get_attribute("href")

		if nextPageURL in pages:
			log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Already scanned the next page... quit")
			b_nextPage = False
		else:
			b_nextPage = True


		#print("Next Page: " + str(nextPage))
	else:
		log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : No URL's on the page: " + nextPageURL)
		b_nextPage = False

	# find_elements_by_xpath - Returns an array of selenium objects.
	property_urls = browser.find_elements_by_xpath('//section[@class="c-search-results__main"]/div/article/div/div/div/h3/a[@href]')

	for p in property_urls:
		property_url = p.get_attribute("href")
		log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Scanning: " + property_url)

		try:
			# Get the property page in the browser
			try:
				p_browser.get(property_url)
			except selenium.common.exceptions.TimeoutException as te:
				log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Timed out... retry...")
				p_browser.get(property_url)
				time.sleep(1)


			# Wait for 1 second to ensure all page is rendered
			time.sleep(1)

			p_id = ''

			# Property ID - unique for each property
			p_id1 = p_browser.find_elements_by_xpath('//article/header/ol/li/span/span')
			p_id1a = [x.text for x in p_id1]
			for p in p_id1a:
				#print("Property data: " + p)
				p_id2 = re.sub('\n','',p)
				p_id3 = re.sub(' +',' ', p_id2)
				p_id4 = re.search('\d+',p_id3)
				p_id = p_id4.group(0)

			#print("Property ID: " + p_id)

			cal = p_browser.find_elements_by_xpath('//div[@id="calendar"]/div/div/table')

			#review_rating = p_browser.find_elements_by_class_name('c-facet__label')
			
			#for i in cal.find_elements_by_xpath('.//tr'):
			#    print(i.get_attribute('innerHTML'))

			try:
				cal2 = [x.get_attribute('innerHTML') for x in cal]

			except selenium.common.exceptions.StaleElementReferenceException as wde:
				log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : Error getting calendar: " + property_url)
				print(type(wde))
				print(wde.args)
				print(wde)


			try:
				cal_text = cal2[0]
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

			#print("Review count: " + review_count)


			# Check the current rating out of 5
			#review_rating = p_browser.find_elements_by_xpath('//span[@class="c-facet c-review__rating"]/span/span[@class="c-facet__label"]')
			#review_rating = p_browser.find_elements_by_xpath('//*[@id="reviews"]/div[2]/header/span/span/span[2]')

			review_rating = p_browser.find_elements_by_xpath('//*[@id="reviews"]/div[2]/header/span/span/span[2]/span[1]')
			#print("Review rating raw:")
			#print(review_rating)

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
				'page_nbr' : page_number,
				'p_nbr' : property_number,
				'calendar' : cal_text
			}



			#pd[p_id] = ( review_value, review_count, cal_text )
			if first_page is True:
				fp.write('\n')
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

	log.error(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") + "Getting next page: " + nextPageURL)
	browser.get(nextPageURL)
	page_number += 1



	pages[nextPageURL] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")



	

#with open('WebData/stayz_calendar' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") + '.json', 'w') as fp:
#    json.dump(property_data, fp, indent=2)
log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : Completed extract...")

p_browser.close()
	
browser.close()

# Property ID - unique for each property
#p_id1 = response.selector.xpath('//article/header/ol/li/span/span/text()').extract_first()
#p_id2 = re.sub('\n','',p_id1)
#p_id3 = re.sub(' +',' ', p_id2)
#p_id4 = re.search('\d+',p_id3)
#p_id = p_id4.group(0)
