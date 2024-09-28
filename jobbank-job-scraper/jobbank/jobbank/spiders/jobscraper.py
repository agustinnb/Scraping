from asyncio import base_futures
from types import NoneType
import scrapy
import bs4 as bs
import re
from .. import items


class JobscraperSpider(scrapy.Spider):
    name = 'jobscraper'
    allowed_domains = ['jobbank.gc.ca']
    start_urls = ['https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=data+scientist+&locationstring=Canada&sort=M']
    base_url =  'https://www.jobbank.gc.ca'
    
        
    def parse(self, response):
        gbody = response.xpath("//article/a/@href").extract()   
        for i in range(0,len(gbody)):
            jobget = self.base_url + gbody[i]
            
            request = scrapy.Request(url=jobget,callback=self.parse_job)
            yield request

        pass

    def parse_job(self,response):
        item = items.JobbankItem()
        item['link']=response.request.url
        item['title'] = response.xpath("//span[@property='title']/text()").extract_first()
        item['dateposted'] =response.xpath("//span[@property='datePosted']/text()").extract_first()
        item['addresslocality'] = response.xpath("//span[@property='addressLocality']/text()").extract_first()
        item['addressRegion'] = response.xpath("//span[@property='addressRegion']/text()").extract_first()
        if 'for' in response.xpath("//ul[contains(@class, 'job-posting-brief')]//li[2]/text()").extract()[1]:
            if (type(response.xpath("//span[@property='minValue']/text()").extract_first())!=NoneType):
                item['salary'] = response.xpath("//span[@property='minValue']/text()").extract_first()
            if (type(response.xpath("//span[@property='unitText']/text()").extract_first())!=NoneType):
                item['salary'] += ' - ' + response.xpath("//span[@property='unitText']/text()").extract_first()
        else:
            item['salary'] = response.xpath("//ul[contains(@class, 'job-posting-brief')]//li[2]/text()").extract()[1]
        item['startdate'] = response.xpath("//ul[contains(@class, 'job-posting-brief')]//li[3]/span[3]/text()").extract_first()
        item['vacancy'] = response.xpath("//ul[contains(@class, 'job-posting-brief')]//li[4]/span[3]/text()").extract_first()
        yield item