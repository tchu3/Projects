

<!-- OBJECTIVE -->
## OBJECTIVE

OBJECTIVE: Create a scraper for housing prices in Calgary.

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

Leveraging Docker and Scrapy, programmed a number of spiders that crawl through the webpages and collect listing information for unique MLS listings using xPath to scour XML information returned from the website. Data scraped included:

 - MLS #
 - Address
 - Price
 - Link
 - Image
 - No. Bed/Baths
 - Square footage
 - Subdivision
 - Post date
 - House style
 - Year Built

Scrapes are done in two steps, the first spider scrapes preliminary data including a link for additional details. The second spider goes into the MLS listing and gets additional information.

<!-- USAGE EXAMPLES -->
## Usage

1. Launch Docker via (docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 3600 ) in command prompt
2. Data is currently appended to existing csv files

<!-- ROADMAP -->
## Roadmap

- Use a virtual machine to run scrape daily - off local PC
- Push data into SQL database
- Find source and built spider to pull transaction data - compare ask prices with actual transaction prices to evaluate List Price/Sales Price
- Handling of price increases and drops on existing MLS listings, currently only the initial price is captured

<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com

