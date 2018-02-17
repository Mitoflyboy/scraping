# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash
import datetime
import logging
import datetime
from scrapy.shell import inspect_response
from scrapy.shell import open_in_browser
from scrapy_splash import SplashRequest


# Setup a pipeline
class JsonWriterPipeline(object):
    def open_spider(self, spider):

        now = datetime.datetime.now()
        # Filename reflects current timestamp
        self.file = open('stayz_calendar' + now.strftime("%Y-%m-%d_%H-%M") + '.jl','w')
        
    def close_spider(self, spider):
        self.file.close()
        
    def processitem(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item