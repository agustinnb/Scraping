import scrapy
from urllib.parse import urlencode
from scrapy.utils.response import open_in_browser

class ScraperBankCodesSpider(scrapy.Spider):
    name = 'scraper_bank_codes'
    allowed_domains = ['bank.codes']
    start_urls = ['https://bank.codes/us-routing-number/bank/']

    def start_requests(self):
        urls = ['https://bank.codes/us-routing-number/bank/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_main_page)

    def parse_main_page(self, response):
         main_page = response.request.url
         print(f"main_page:{main_page}")
         banks_urls = response.xpath("//div[@class='post_content']/a/@href").getall()
         for bank_url in banks_urls:
             if bank_url[0:1]=="/":
                 absolute_path = f"https://bank.codes{bank_url}"
                 yield scrapy.Request(absolute_path, callback=self.parse_bank_url)

    def parse_bank_url(self,response):
        bank_url = response.request.url
        print(f"bank_url:{bank_url}")

        routing_numbers_urls = response.xpath("//div[@class='post_content']/table/tbody/tr/td[2]/a/@href").getall()
        for routing_numbers_url in routing_numbers_urls[0:]:
            absolute_path = f"https://bank.codes{routing_numbers_url}"
            yield scrapy.Request(absolute_path, callback=self.scrap_routing_number_url)

    def scrap_routing_number_url(self,response):
        routing_number_url = response.request.url
        print(f"routing_number_url:{routing_number_url}")

        routing_number = response.xpath("//th[text()='Routing Number']/../td/text()").get()
        date_of_revision = response.xpath("//th[text()='Date of Revision']/../td/text()").get()
        bank = response.xpath("//th[text()='Bank']/../td/text()").get()
        address = response.xpath("//th[text()='Address']/../td/text()").get()
        city = response.xpath("//th[text()='City']/../td/text()").get()
        state = response.xpath("//th[text()='State']/../td/text()").get()
        zip = response.xpath("//th[text()='ZIP']/../td/text()").get()
        phone = response.xpath("//th[text()='Phone']/../td/text()").get()

        data = {
            'routing_number': routing_number,
            'date_of_revision': date_of_revision,
            'bank': bank,
            'address': address,
            'city': city,
            'state': state,
            'zip': zip,
            'phone': phone,
        }
        print(data)
        yield data
