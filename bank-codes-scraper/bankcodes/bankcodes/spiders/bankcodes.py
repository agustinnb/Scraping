import scrapy


class BankcodesSpider(scrapy.Spider):
    name = 'bankcodes'
    allowed_domains = ['bank.codes']
    start_urls = ['https://bank.codes/us-routing-number/bank/']
    
    def parse(self, response):
        print(response.request.headers.get("User-Agent"))
        print(response.body)
        
        routing_numbers_urls = response.xpath("//div[@class='post_content']/a/@href").getall()
        print(routing_numbers_urls)
        pass
