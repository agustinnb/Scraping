# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem



class Elcigarroelectronico3Pipeline:


    def process_item(self, item, spider):
        fp=open("productos.csv","a")
        fp.write(str(item['webpage_id']) + ';' + str(item['url']) + ';' + str(item['name']) + ';' + str(item['price']) + ';' + str(item['image_urls'][0]) + ';' + str(item['image_path']) + '\n')
        return item
        

    

class ElCigarroElectronico3ImagesPipeline(ImagesPipeline):


    def file_path(self, request, response=None, info=None, *, item):
        image_perspective = request.url.split('/')[-1]
        image_filename = item['image_path']

        return image_filename

