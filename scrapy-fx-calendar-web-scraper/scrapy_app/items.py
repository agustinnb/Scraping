# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # django_model = ScrapyItem	
    unique_id=scrapy.Field()
    ticker = scrapy.Field()
    symbol = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    importance = scrapy.Field()
    previous = scrapy.Field()
    forecast = scrapy.Field()
    country = scrapy.Field()
    actual = scrapy.Field()
    alldayevent = scrapy.Field()
    currency = scrapy.Field()
    reference = scrapy.Field()
    revised = scrapy.Field()
    #economicMeaning = []
    lastupdate = scrapy.Field()
