# -*- coding: utf-8 -*-
"""
Created on Sat May 23 08:15:05 2020

@author: Tommy Chu
"""

import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime, timedelta

#from ..items import grocery_name
from ..items import houseItem

### docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 3600 

class MySpider(scrapy.Spider):
    name = 'scrapeMLS2'
    start_urls = []
    # Define a flag that will turn 1 if the spider finds a duplicate row
    updateFlag = 0
    
    # Open the previous MLS1 scrape data to gather all the links
    file = open(r'C:\Users\Tommy Chu\Dropbox\(3) Python\(2) YYCRealEstate\scrapeMLS1.txt')
    lines = file.readlines()
    for line in reversed(lines):
        currentLine = line.split()[0]
        start_urls.append('https://www.calgarylistings.com' + currentLine)
    file.close()
    
    # Initialize list to hold pre-existing addresses
    addressList = []
    
    # Read the last address from the previous MLS scrape data
    file = open(r'C:\Users\Tommy Chu\Dropbox\(3) Python\(2) YYCRealEstate\scrapeMLS2.txt','r', encoding="utf-8")
    try:
        _tempList = file.readlines()
        # Append the link address to the pre-existing list
        for line in _tempList:
            addressList.append(line.split("\t")[0])
    except:
        addressList = []
        
    file.close()

        
    script = """
        function main(splash, args)
        -- set private mode to allow website to load    
        splash.private_mode_enabled = false
        -- go to website and wait
        assert (splash:go(args.url))
        assert (splash:wait(2))
        
        --if splash:select('a[href="#"]') ~= nil then
        --    local submit_button = splash:select('a[href="#"]')
        --    submit_button:click()
        --end
        --assert (splash:wait(2))
        
          return {
            html = splash: html(),
        }
                    
    end
              """

    def start_requests(self):
        for url in self.start_urls:
            # If the currrent url being passed is in the address list already skip
            if (str(url[31:-1] + "/") in self.addressList):
                print(str(url[31:-1] + "/"))
                continue
            else:        
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

        # Initialize subDivision + posted date in case it is not available
        item["subdivision"] = ""
        item["postDate"] = ""
        item["style"] = ""
        item["year"] = ""
        item["mls"] = ""
   
        # using .// selects the nodes continuing from the previous node in the for loop
        # single line if statement, if the query is empty enter "", else use the element
        # [1:] removes the first character of the string
        try: 
            tempPath = '//div[@class="si-ld-primary__info clearfix"]//div//text()'
            for index, x in enumerate(response.xpath(tempPath)):
                # If the index equals MLS the next index would be the MLS #
                if str(x.extract())[0:3] == "MLS":
                   item["mls"] = str(response.xpath(tempPath).extract()[index+1])
                # If the index equals to On Site: how many dats
                if str(x.extract()) == "On Site:":
                   tempPostDate = str(response.xpath(tempPath).extract()[index+1])
                   tempPostDate = int(tempPostDate.split()[0])
                   tempPostDate = datetime.today() - timedelta(days=tempPostDate)
                   item["postDate"] = tempPostDate.strftime('%x')
                ### ADD SCRAPE FOR MAINTENANCE FEE
            
            tempPath = '//section[@class="si-ld-details clearfix js-scrollto"]//div[@class="si-ld-details__item clearfix js-masonary-item js-collapsible"]//div//text()'
            for index, x in enumerate(response.xpath(tempPath)):
                if str(x.extract()) == "Subdivision:":
                # If the specific page has a subdivision record it - otherwise it will be blank
                   item["subdivision"] = str(response.xpath(tempPath).extract()[index+1])
    
            tempPath = '//div[@class="si-ld-details__item js-masonary-item js-collapsible"]//div//text()'
            for index, x in enumerate(response.xpath(tempPath)):
                if str(x.extract()) == "Style:":
                    # If the specific page has a style record it - otherwise it will be blank
                    item["style"] = str(response.xpath(tempPath).extract()[index+1])
                if str(x.extract()) == "Year Built:":
                    # If the specific page has a year built record it - otherwise it will be blank
                    item["year"] = str(response.xpath(tempPath).extract()[index+1])
    
            # Capture long text and strip any tabs and line breaks on left and right
            # item["longText"] = str(response.xpath('//div[@class="si-ld-description js-listing-description"]//text()').extract()[0]).lstrip().rstrip()
            # Capture the address - need to update this to include city and postal
            item["address"] = str(response.xpath('//div[@class="si-ld-top js-top-nav"]//h1//text()').extract()[0])
            item["link"] = str(response.xpath('//link[@rel="canonical"]/@href').extract()[0])[31:-1]

            with open(r'C:\Users\Tommy Chu\Dropbox\(3) Python\(2) YYCRealEstate\scrapeMLS2.txt','a+', encoding="utf-8") as file:
                file.write(item["link"] + "/" + '\t' + item["address"] + '\t' + item["mls"]+ '\t' + item["postDate"] + '\t' + item["subdivision"] + '\t' + item["style"] + '\t' + item["year"] + '\n')
                file.close()
            r'''
                    # Open scrapeMLS3 that holds all the comments
                    with open(r'C:\Users\Tommy Chu\Dropbox\(3) Python\(2) YYCRealEstate\scrapeMLS3.txt','a+', encoding="utf-8") as file:
                        if (str(item["link"] + "/") in self.addressList) or self.updateFlag == 1:
                            self.updateFlag = 1
                        else:
                            file.write(item["link"] + "/" + '\t' + item["longText"] + '\n')
                        file.close()
            '''
        except:
            pass