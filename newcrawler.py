import requests
from bs4 import BeautifulSoup
import scrapy, csv
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import requests
from scrapy.crawler import CrawlerProcess
from csv import reader

with open('websites.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	out = list(map(tuple, csv_reader))
	
with open('keywords.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	keywords = list(map(tuple, csv_reader))

class GetInfoSpider(scrapy.Spider):
	name = "WebCrawler"
	start_urls = out
	allowed_domains = ['technet.net', 'bisnow.com', 'washingtonpost.com', 'tysonsreporter.com', ' izjournals.com/atlanta', 'bizjournals.com/houston', 'bizjournals.com', 'ajc.com','chron.com', 'denverpost.com', 'dc.citybizlist.com', 'americaninno.com', 'virginiabusiness.com', 'bloomberg.com', 'federalnewsnetwork.com','forbes.com', 'thehill.com', 'inc.com','washingtontechnology.com', 'technical.ly.com']

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
                follow=True,
                callback="parse"
        )
    ]

	def __init__(self):
		self.infile = "output.csv"

    def wordCount(self, text):
        blacklist = [
	        '[document]',
	        'noscript',
	        'header',
	        'html',
	        'meta',
	        'head', 
	        'input',
	        'script',
        ]
        output = ''
        for t in text:
	        if t.parent.name not in blacklist:
		        output += '{} '.format(t)
        counter = 0
        keyWords = self.get_keywords()
        keywordCount = []
        for i in range(len(keyWords)):
            numOfOccur = output.count(keyWords[i])
            keywordCount.append(numOfOccur)
            counter += numOfOccur
        
        l = -1
        for i in range(len(keywordCount)):
            if keywordCount[i] > l:
                l = i
        keywordCount.append(counter)
        return [l, counter]   

c = CrawlerProcess({
	'USER_AGENT': 'Mozilla/5.0',   
})
c.crawl(GetInfoSpider)
c.start()