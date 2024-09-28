import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Elcigarroelectronico3Item

class ElcigarroelectronicoSpider(CrawlSpider):

    def parse(self, response, **kwargs):
        pass

    name = 'elcigarroelectronico3'
    allowed_domains = ['elcigarroelectronico.com']
    start_urls = ['https://elcigarroelectronico.com/']

    rules = (
        Rule(LinkExtractor(deny=('/content/','contact', '/brand/', 'autenticacion', 'blog', 'contrasena', '\?back', 'facebook', 'google', '\?q=', '\?order', '\?tag=', '/modules/', 'resultsPerPage=', '.html\?', '/jolisearch\?s=', '/reviews\?')), callback='parse_url', follow=True),
    )

    def parse_url(self, response):
        url = response.url
        print(url)

        if ".html" in url:
            name = response.xpath('//h1/span/text()').get()
            if name: name = name.replace("\n", "")
            price = response.xpath("//span[@class='current-price']/span/text()").get()
            price = str(price).strip()
            image_url = response.xpath("//div[contains(@class, 'easyzoom')]//a//img//@src").extract()
            #print (response.body)
            items = Elcigarroelectronico3Item()
            items['webpage_id']=self.name
            items['url']=url
            items['name']=name
            items['price']=price
            items['image_urls']=image_url
            items['image_path']=self.name+'/'+str(image_url[0]).split('/')[-1]

            yield items
