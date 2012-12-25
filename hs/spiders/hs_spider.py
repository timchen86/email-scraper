# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.spider import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

import hs.settings as settings

from urlparse import urlparse
import json
import copy
import re
import csv
import datetime 
import pprint 

class HsItem(Item):
    # define the fields for your item here like:
    domain = Field()
    mail = Field()

class HsSpider(BaseSpider):
    name = "hs"
    #allowed_domains = ["www.missingkids.org.tw"]
    start_urls = ["http://www.nssh.ntpc.edu.tw/bin/home.php"]

    i = 0

    def __init__(self):
        dispatcher.connect(self.engine_stopped, signals.engine_stopped)
        pass


    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        urls = hxs.select('//a/@href').extract()

        domain = urlparse(response.url).netloc
        ds = domain.split('.')
        base1 = ds[len(ds)-2]
        base2 = ds[len(ds)-3]

        for u in urls:
            if base1 in u or base2 in u:
                self.i+=1
                if self.i<300:
                    yield Request(u, self.mail_parser)


    def mail_parser(self, response):
        hxs = HtmlXPathSelector(response)
        item = HsItem()
        mailto = hxs.select("//a[@href]").re("mailto:(.*?)[,\"%\?]{1}")
        mail = mailto + hxs.select("//text()").re("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}")
 
        domain = urlparse(response.url).netloc.split('.')
        item['domain'] = '.'.join(domain[(len(domain)-4):])
        item['mail'] = list(set(mail))

        if len(item['mail'])>0:
            return item

        
    def engine_stopped(self):
        with open(settings.RAW_JSON,"rb") as json_file:
            data_raw = json.load(json_file)
               
            data = []

            for dr in data_raw:
                if dr["domain"] not in [s["domain"] for s in data]:
                    data.append(dr)
                else:
                    for d in data:
                        if d["domain"] == dr["domain"]:
                            d["mail"] += dr["mail"]
                        d["mail"] = list(set(d["mail"]))    
                        
            with open(settings.SORTED_JSON, 'wb') as json_file:
                json.dump(data, json_file)
