# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.spider import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

import hs.settings as settings

import copy
import re
import csv
import datetime 

class HsItem(Item):
    # define the fields for your item here like:
    mail = Field()
    mailto = Field()
    link = Field()

class HsSpider(BaseSpider):
    name = "hs"
    #allowed_domains = ["www.missingkids.org.tw"]
    start_urls = ["http://www.nssh.ntpc.edu.tw/bin/home.php"]

    def __init__(self):
        #dispatcher.connect(self.engine_stopped, signals.engine_stopped)
        pass


    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        urls = hxs.select('//a/@href').extract()

        for u in urls:
            yield Request(u, self.mail_parser)


    def mail_parser(self, response):
        hxs = HtmlXPathSelector(response)
        item = HsItem()
        mailto = hxs.select("//a[@href]").re("mailto:(.*?)[,\"%\?]{1}")
        mail = mailto + hxs.select("//text()").re("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}")
        
        item['mail'] = list(set(mail))
        
        if len(item['mail'])>0:
            return item
