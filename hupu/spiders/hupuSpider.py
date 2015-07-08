#hupuSpider.py

import scrapy
from scrapy import log
from hupu.items import HupuItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class hupuSpider(CrawlSpider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    start_urls = ["http://bbs.hupu.com/bxj",
                  "http://bbs.hupu.com/13145086.html"]
    rules = (
        Rule(LinkExtractor(allow = (r'http://bbs.hupu.com/.*\.php', ))),
        Rule(LinkExtractor(allow = (r'http://bbs.hupu.com/\d*\.html', )), callback = 'parse_item'),
        )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        item = HupuItem()
        
        item['title'] = response.xpath('//head/title/text()').extract()
        
        #spans = response.xpath('//span')
        #for s in spans.xpath('.//span'):
            #print s.extract()
        sel = response.xpath('//span[@author]/@author').extract()
        
        item['url'] = response._get_url()
        
        if sel:
            item['author'] = sel
        else:
            item['author'] = 'somebody'
            
        cons = response.xpath("//div[@class = 'subhead']")
        co = ''
        for c1 in cons.xpath('../p/text()'):
            co += c1.extract()
        for c2 in cons.xpath('../b/text()'):
            co += c2.extract()
        for c3 in cons.xpath('../div/text()'):
            co += c3.extract()
        for c4 in cons.xpath('../text()'):
            co += c4.extract()
        item['content'] = co;

        hh = u''
        hl = response.xpath('//div[@id = "readfloor"]')
        #//*[@id="192432"]/div[2]/table/tbody/tr/td/text()
        #//*[@id="134552"]/div[2]/table/tbody/tr/td/text()[1]
        #//*[@id="134552"]/div[2]/table/tbody/tr/td/text()[2]
        for h in hl.xpath('div'):
            #print h.xpath('div[@class = "floor_box"]/table[@class = "case"]/tr/td/text()').extract()
            for h0 in h.xpath('div[@class = "floor_box"]/table[@class = "case"]/tr/td/text()').extract():
                hh += h0
        item['light'] = hh
            
        yield item

    def parse_details(self, response):
        item = response.meta.get('item', None)
        if item:
            # populate more `item` fields
            return item
        else:
            self.log('No item received for %s' % response.url,
                     level=log.WARNING)
