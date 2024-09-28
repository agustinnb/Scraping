# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from tkinter import image_names
import scrapy


class Elcigarroelectronico3Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    webpage_id = scrapy.Field()
    url= scrapy.Field()
    name= scrapy.Field()
    price=scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()
    image_path=scrapy.Field()
    pass

