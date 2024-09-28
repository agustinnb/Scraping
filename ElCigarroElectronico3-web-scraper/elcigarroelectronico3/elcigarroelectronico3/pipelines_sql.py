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
import hashlib
from os.path import splitext
import os
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline

class Elcigarroelectronico3Pipeline:
    createtable=False
        
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='prueba1234',
            database='price_comparer_db'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS price_comparer_tb""")
        self.curr.execute("""create table price_comparer_tb(
                        id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        webpage_id varchar(100),
                        url varchar(300),
                        name varchar(100),
                        price varchar(10), /* ESTA HABRIA QUE CAMBIARLA POR UN FLOAT; PERO HABRIA QUE SCRAPEAR UN FLOAT */
                        image_url varchar(500),
                        image_path varchar(100)
                        )""")


    def process_item(self, item, spider):
        if self.createtable==False:
                self.create_connection()
                self.create_table()
                self.createtable=True
        self.store_db(item)
        
        #print(item)
        #fp=open("productos.csv","a")
        #fp.write(str(item['webpage_id']) + ';' + str(item['url']) + ';' + str(item['name']) + ';' + str(item['price']) + ';' + str(item['image_url']) + ';' + str(item['image_path']) + '\n')
        #self.download_image(item)
        return item
        

        


    def store_db(self, item):
        self.curr.execute("""insert into price_comparer_tb(webpage_id,url,name,price,image_url,image_path) values (%s, %s, %s, %s, %s, %s)""", (
            item['webpage_id'],
            item['url'],
            item['name'],
            item['price'],
            item['image_urls'][0],
            item['image_path']
        ))
        self.conn.commit()
    

    #def get_media_requests(self, item, info):       
    #    adapter = ItemAdapter(item)
    #    for file_url in adapter['file_urls']:
    #        yield scrapy.Request(file_url)

    #def item_completed(self, results, item, info):
    #    image_paths = [x['path'] for ok, x in results if ok]
    #    if not image_paths:
    #        raise DropItem("Item contains no images")
    #    item['image_paths'] = image_paths
    #    return item

    def file_path(self, request, response=None, info=None, *, item=None):
        print (os.path.basename(urlparse(request.url).path))
        return 'files/' + os.path.basename(urlparse(request.url).path)


class ElCigarroElectronico3ImagesPipeline(ImagesPipeline):


    def file_path(self, request, response=None, info=None, *, item):
        image_perspective = request.url.split('/')[-1]
        image_filename = item['image_path']

        return image_filename

