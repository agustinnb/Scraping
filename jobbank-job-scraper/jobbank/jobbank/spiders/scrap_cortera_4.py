import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from pymsgbox import *
from twisted.internet import defer
import re
import time


class ScrapCorteraSpider(scrapy.Spider):
    name = 'scrap_cortera_4'
    allowed_domains = ['cortera.com']
    start_urls = ['https://start.cortera.com/go/dispatcher/signin']
    waitingVar=0    
    TotalUrls=0
    OriginalUrl=''
    page_no=''
    SubIndustryIndex=0
    SubIndustryOriginalUrl=''
    IndustryIndex=0


    def parse(self, response):
        print(f"Login Page: {response.request.url}")
        token = response.xpath("//*[@name='_csrf']/@content").get()
        return FormRequest.from_response(
            response,
            formdata={'_csrf': token,
                      'password': 'xpdw9q7r7',
                      'userid': 'heinz.rich@protonmail.com',
                      'remember-user': 'Y'},
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
        # for i in range(0,1):
        industry = urls[self.IndustryIndex].xpath("text()").get()
        print(industry)

        url = response.urljoin(urls[self.IndustryIndex].xpath("@href").get())
            # print(url)
            # print()
        self.IndustryIndex=self.IndustryIndex+1
        if (self.IndustryIndex<len(urls)): # Si no llegué a la última industria
            yield scrapy.Request(url=url, callback=self.go_to_subindustry_page)
        else:
            print("Termine!")
        
    def go_to_subindustry_page(self, response):
        print(f"\n             SubIndustry Page: {response.request.url}")
        #open_in_browser(response)
        #alert("stop")
        self.SubIndustryOriginalUrl=response.request.url

        print("\n             SubIndustries (level 2)")
        print("             ------------------------------------------")
        urls = response.xpath("//div[@id='listing']/p/a")
        #for i in range(0,len(urls)):
        
        #for i in range(0,1):
        subindustry = urls[self.SubIndustryIndex].xpath("text()").get()
        print(f"             {subindustry}")

        url = response.urljoin(urls[self.SubIndustryIndex].xpath("@href").get()) # Agarro de a una industria en vez de todas juntas
            # print(f"             {url}")
            # print()
        self.SubIndustryIndex=self.SubIndustryIndex+1 # Sumo en 1, la próxima vez que entro a este request, va a ir a la siguiente industria

        if (self.SubIndustryIndex<len(urls)): # Si no estoy por la última subindustria
            yield scrapy.Request(url=url, callback=self.go_to_terminal)
        else:  # Si ya pasé la última subindustria 
            self.SubIndustryIndex=0 # reseteo subindustryindex
            yield scrapy.Request("https://start.cortera.com/go/industry", callback=self.go_to_industry_page) # Vuelvo a requestear la página de las industrias

    def go_to_terminal(self, response):
        
        # Define do_next_page
        self.OriginalUrl=response.request.url

        
        urls = response.xpath("//div[@id='directory']/form/p/a")
        self.TotalUrls=len(urls)

        # Leer primero lo que hace la función scrap
        if (self.TotalUrls==self.waitingVar):
            if (response.xpath("//*[contains(text(), 'More Businesses')]").getall()): # Me fijo si contiene la palabra "more Businessses" 
                csrf = response.xpath("//form[@name='companiesByIndustryForm']//*[@name='_csrf']/@value").get()
                list_order = 'next'
                highRange = ''
                lowRange = ''
                selectedSicName = response.xpath("//form[@name='companiesByIndustryForm']//*[@name='selectedSicName']/@value").get()
                selectedRangeId = response.xpath("//form[@name='companiesByIndustryForm']//*[@name='selectedRangeId']/@value").get()
                selectedRangeName = response.xpath("//form[@name='companiesByIndustryForm']//*[@name='selectedRangeName']/@value").get()
                scripttext= str(response.xpath("//*[contains(text(), 'document.companiesByIndustryForm.list_order.value')]").getall())
                if self.page_no == '':
                    self.page_no = str(re.findall(r'document.companiesByIndustryForm.page_no.value = (.*?);',scripttext,re.IGNORECASE)).replace('[','').replace(']','').replace('\\','').replace('"','').replace('\'','')
                else:
                    self.page_no = str(int(self.page_no)+1)
                request= FormRequest.from_response(
                response,
                formname='companiesByIndustryForm',
                formdata={'_csrf': csrf,
                'list_order': list_order,
                'page_no': self.page_no,
                'high_range': highRange,
                'low_range': lowRange,
                'selectedSicName': selectedSicName,
                'selectedRangeId': selectedRangeId,
                'selectedRangeName': selectedRangeName,
                },
                url=response.request.url,
                callback=self.go_to_terminal,priority=0)      
                self.waitingVar=0 # vuelvo a poner waitingVar en 0
                yield request
                return # Una vez que ejecute esto, mato esta function, porque ya la estoy llamando de nuevo en el callback (O sea, esta ejecución solo sirvió para cambiar la página)
            else:
                # SI NO HAY BOTON SIGUIENTE
                self.page_no='' # Reseteo page_no
                yield scrapy.Request(url=self.SubIndustryOriginalUrl, callback=self.go_to_subindustry_page)
                return

        print(f"\n                          Terminal Page: {response.request.url}")
        #open_in_browser(response)
        # alert("stop")
        print("\n                          Terminal Pages (level 3)")
        print("                          ------------------------------------------")




        for i in range(0,len(urls)):
        #for i in range(0,1):
            terminal = urls[i].xpath("text()").get()
            print(f"                          {terminal}")

            url = response.urljoin(urls[i].xpath("@href").get())
            # print(f"                          {url}")
            # print()
            yield scrapy.Request(url=url, callback=self.scrap,priority=1) # Hago el YIELD dentro del FOR
        
        
        
        


    def scrap(self,response):
        print(f"                                       Terminal Page Data: {response.request.url}")
        #open_in_browser(response)
        # alert("stop")

        title = response.xpath("//div[@class='companyBasics']/h1/text()").get()
        print(f"                                       title: {title}")

        address = response.xpath("//input[@id='address']/@value").get()
        print(f"                                       address: {address}")
        self.waitingVar=self.waitingVar+1 # Voy sumando la variable waitingVar 1 (Esto porque si no lo hago así, hace el yield antes de terminar de scrapear la página)
        if (self.waitingVar==self.TotalUrls): # Cuando llego al último elemento de la página
            yield scrapy.Request(url=self.OriginalUrl, callback=self.go_to_terminal) # Vuelvo a Scrapear, pero esto se va a topar con el if de arriba de todo       
        
    

    

    