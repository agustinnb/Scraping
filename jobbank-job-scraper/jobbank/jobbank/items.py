# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobbankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    dateposted =scrapy.Field()
    addresslocality = scrapy.Field()
    addressRegion = scrapy.Field()
    salary = scrapy.Field()
    startdate = scrapy.Field()
    vacancy = scrapy.Field()
    pass
