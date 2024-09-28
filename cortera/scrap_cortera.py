import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from pymsgbox import *


class ScrapCorteraSpider(scrapy.Spider):
    name = 'scrap_cortera_4'
    start_urls = ['https://start.cortera.com/go/dispatcher/signin']

    def parse(self, response):
        print(f"Login Page: {response.request.url}")
        token = response.xpath("//*[@name='_csrf']/@content").get()
        return FormRequest.from_response(
            response,
            formdata={'_csrf': token,
                      'password': 'xpdw9q7r7',
                      'userid': 'heinz.rich@protonmail.com'},
            callback=self.go_to_main_page)

    def go_to_main_page(self, response):
        #alert("stop")
        print(f"Logged in: {response.request.url}")
        #open_in_browser(response)
        yield scrapy.Request("https://start.cortera.com/go/industry", callback=self.go_to_industry_page)

    def go_to_industry_page(self, response):
        #alert("stop")
        print(f"\nIndustry Page: {response.request.url}")
        #open_in_browser(response)

        print("\nIndustries (level 1)")
        print("------------------------------------------")
        urls = response.xpath("//div[@id='listing']/p/a")
        #for i in range(0,len(urls)):
        for i in range(0,1):
            industry = urls[i].xpath("text()").get()
            print(industry)

            url = response.urljoin(urls[i].xpath("@href").get())
            # print(url)
            # print()

            yield scrapy.Request(url=url, callback=self.go_to_subindustry_page)

    def go_to_subindustry_page(self, response):
        print(f"\n             SubIndustry Page: {response.request.url}")
        #open_in_browser(response)
        #alert("stop")

        print("\n             SubIndustries (level 2)")
        print("             ------------------------------------------")
        urls = response.xpath("//div[@id='listing']/p/a")
        #for i in range(0,len(urls)):
        for i in range(0,1):
            subindustry = urls[i].xpath("text()").get()
            print(f"             {subindustry}")

            url = response.urljoin(urls[i].xpath("@href").get())
            # print(f"             {url}")
            # print()

            yield scrapy.Request(url=url, callback=self.go_to_terminal)

    def go_to_terminal(self, response):
        print(f"\n                          Terminal Page: {response.request.url}")
        #open_in_browser(response)
        # alert("stop")

        print("\n                          Terminal Pages (level 3)")
        print("                          ------------------------------------------")
        urls = response.xpath("//div[@id='directory']/form/p/a")
        for i in range(0,len(urls)):
        #for i in range(0,1):
            terminal = urls[i].xpath("text()").get()
            print(f"                          {terminal}")

            url = response.urljoin(urls[i].xpath("@href").get())
            # print(f"                          {url}")
            # print()
        
            yield scrapy.Request(url=url, callback=self.scrap)
        csrf = response.xpath("//form[@name='companiesByIndustryForm']/*[@name='_csrf']/@value").get()
        list_order = 'next'
        page_no = '1'
        highRange = ''
        lowRange = ''
        selectedSicName = response.xpath("//form[@name='companiesByIndustryForm']/*[@name='selectedSicName']/@value").get()
        selectedRangeId = response.xpath("//form[@name='companiesByIndustryForm']/*[@name='selectedRangeId']/@value").get()
        selectedRangeName = response.xpath("//form[@name='companiesByIndustryForm']/*[@name='selectedRangeName']/@value").get()
        yield FormRequest.from_response(
        response,
        formdata={'_csrf': csrf,
        'list_order': list_order,
        'page_no': page_no,
        'high_range': highRange,
        'low_range': lowRange,
        'selectedSicName': selectedSicName,
        'selectedRangeId': selectedRangeId,
        'selectedRangeName': selectedRangeName,
        },
        callback=self.go_to_terminal)


        ############# HERE IS WHERE I HAVE TO GO TO THE NEXT PAGE USING REQUEST OR FORMREQUEST

    def scrap(self,response):
        print(f"                                       Terminal Page Data: {response.request.url}")
        #open_in_browser(response)
        # alert("stop")

        title = response.xpath("//div[@class='companyBasics']/h1/text()").get()
        print(f"                                       title: {title}")

        address = response.xpath("//input[@id='address']/@value").get()
        print(f"                                       address: {address}")

        print()