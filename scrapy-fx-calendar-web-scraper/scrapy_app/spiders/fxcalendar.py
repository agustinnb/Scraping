import scrapy
import json
from .. import items

class FxcalendarSpider(scrapy.Spider):
    name = 'fxcalendar'
    allowed_domains = ['www.dailyfx.com']
    start_urls = ['https://www.dailyfx.com/economic-calendar']

    def parse(self, response):
        res = response.body
        resutf= res.decode('utf-8')
        splitres=resutf.split('dataProvider,')
        lastsplit=splitres[1].split(');\nDfxSocialShareFactory.create()')
        lastsplit2=lastsplit[0].split(',\n{')
        json_data = json.loads(lastsplit2[0])
        
        for i in range(0,len(json_data)):           
            item = items.ScrapyAppItem()
            item['unique_id']=json_data[i]['id']
            item['ticker']=json_data[i]['ticker']
            item['symbol']=json_data[i]['symbol']
            item['date']=json_data[i]['date']
            item['title']=json_data[i]['title']
            item['description']=json_data[i]['description']
            item['importance']=json_data[i]['importance']
            item['previous']=json_data[i]['previous']
            item['forecast']=json_data[i]['forecast']
            item['country']=json_data[i]['country']
            item['actual']=json_data[i]['actual']
            item['alldayevent']=json_data[i]['allDayEvent']
            item['currency']=json_data[i]['currency']
            item['reference']=json_data[i]['reference']
            item['revised']=json_data[i]['revised']
            item['lastupdate']=json_data[i]['lastUpdate']
            yield item
        
        