import scrapy
from scrapy.http import Request
from io import StringIO
from html.parser import HTMLParser

class CallbarSpider(scrapy.Spider):
    name = 'callbar'
    allowed_domains = ['calbar.ca.gov']
    start_urls = ['https://apps.calbar.ca.gov/attorney/LicenseeSearch/QuickSearch?FreeText=AA&SoundsLike=false']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'


    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def parse(self, response):
        
        arrletter=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        for i in range(0,len(arrletter)):
            for p in range(0,len(arrletter)):
                r = Request(url='https://apps.calbar.ca.gov/attorney/LicenseeSearch/QuickSearch?FreeText='+arrletter[i]+arrletter[p]+'&SoundsLike=false',
                            method='GET',
                            callback=self.after_that)

                yield r

    
    def after_that(self,response):
        gName = response.xpath("//tr[@class='rowASRLodd']/td[1]/a/text()").getall()
        gUrl = response.xpath("//tr[@class='rowASRLodd']/td[1]/a/@href").extract()
        gStatus =  response.xpath("//tr[@class='rowASRLodd']/td[2]/node()").getall()  
        gNumber =  response.xpath("//tr[@class='rowASRLodd']/td[3]/text()").getall() 
        gCity =   response.xpath("//tr[@class='rowASRLodd']/td[4]/text()").getall() 
        gAdmDate=   response.xpath("//tr[@class='rowASRLodd']/td[5]/text()").getall()
        for l in range(0,len(gName)):
            print ("Name:" + gName[l])
            print ("Url: https://apps.calbar.ca.gov/attorney/Licensee" + gUrl[l])
            print ("Status:" + self.strip_tags(gStatus[l]).strip())
            print ("Number:" + gNumber[l])
            print ("City: " + gCity[l])
            print ("Admission Date: " + gAdmDate[l])



class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()
