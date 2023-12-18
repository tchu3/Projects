"""
Created on Sat May 23 08:15:05 2020

@author: Tommy Chu
"""

import scrapy
import math
from scrapy_splash import SplashRequest

#from ..items import grocery_name
from ..items import houseItem

### docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 3600 

class MySpider(scrapy.Spider):
    name = 'scrapeMLS1'
    # Change this hyperparameter for the number of listings
    numListings = 6248
    start_urls = []
    # Define a flag that will turn 1 if the spider finds a duplicate row
    updateFlag = 0
    
    # 12 listings per page - create a url list - rounding up the number of pages
    for i in range(1,math.ceil(numListings/12)+1):
        start_urls.append(str('https://www.calgarylistings.com/calgary-homes-for-sale/?pg=') + str(i))
        
    # Reverse the list so the oldest is at the top
    # start_urls.reverse()
    
    # Create a list of pre-existing data stored in database
    file = open(r'C:\Users\Tommy Chu\Dropbox\(3) Python\(2) YYCRealEstate\scrapeMLS1.txt','r')
    try:
        _tempList = file.readlines()
    except:
        _tempList = []
    file.close()

    script = """
        function main(splash, args)
            -- set private mode to allow website to load    
            splash.private_mode_enabled = false
            -- go to website and wait
            assert (splash:go(args.url))
            assert (splash:wait(2))
        
            return {
                html = splash: html(),
        }                  
        end
              """

    def start_requests(self):
        for url in self.start_urls:
            # If the updateFlag is 1 then break out of the page loop
            if self.updateFlag == 1:
                break
            yield SplashRequest(
                    url=url,
                    callback=self.parse,
                    endpoint='execute',
                    args={'html': 1,'lua_source': self.script, 'wait': 10 }
                    )
            

    def parse(self, response):
        '''
        # Writes the parsed html to a file
        with open('page.html', 'wb') as html_file:
            html_file.write(response.body)
        '''
        
        # Create a house item to store all the data
        item = houseItem()
                
        # Go in reverse order to start from the oldest to the newest
        for x in response.xpath('//div[contains(@data-url,"/listing/")]'):
            # using .// selects the nodes continuing from the previous node in the for loop
            # single line if statement, if the query is empty enter "", else use the element
            # [1:] removes the first character of the string
            item["address"] = str(x.xpath('.//a[contains(@href,"/listing/")]//div[@class="si-listing__title-main"]//text()').extract()[0])
            item["price"] = str(x.xpath('.//div[@class="si-listing__photo-price"]//span/text()').extract()[0])
            item["link"] = str(x.xpath('./@data-url').extract()[0])
            item["img"] = str(x.xpath('.//img/@src').extract()[0])
            try:
                item["beds"] = str(x.xpath('.//div[@class="si-listing__info-value"]//span//text()').extract()[0])
                item["baths"] = str(x.xpath('.//div[@class="si-listing__info-value"]//span//text()').extract()[1])
                item["sqrt"] = str(x.xpath('.//div[@class="si-listing__info-value"]//span//text()').extract()[-1])
            # Except if there is no information available for an acreage
            except:
                item["beds"] = str(0)
                item["baths"] = str(0)
                item["sqrt"] = str(0)

            # Open file with append function
            with open(r'C:\Users\Tommy Chu\Dropbox\(3) Python\(2) YYCRealEstate\scrapeMLS1.txt','a+') as file:
                # Check if the string being added is in the databse already
                _tempString = item["link"] + '\t' + item["address"] + '\t'+ item["price"] + '\t'+ item["beds"] + '\t'+ item["baths"] + '\t' + item["sqrt"] + '\t' + item["img"] + '\n'
                if (_tempString in self._tempList) or self.updateFlag == 1:    
                    print (item["address"])
                    self.updateFlag = 1
                    break
                else:
                    file.write(_tempString)
            file.close()

            
        

