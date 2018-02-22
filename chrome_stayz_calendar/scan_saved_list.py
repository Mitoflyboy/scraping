# Read the list of URLs from the previously saved input list
import json

with open('WebData/stayz_nsw_extract.json') as json_data:
    d = json.load(json_data)
    
    for a in d:
    	print("URL: " + a['url'])
