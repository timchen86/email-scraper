# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.spider import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

import em.settings as settings

from urlparse import urlparse
import json
import copy
import re
import csv
import datetime 
import pprint 

class EmItem(Item):
    # define the fields for your item here like:
    domain = Field()
    mail = Field()

class EmSpider(BaseSpider):
    name = "em"
    #allowed_domains = [""]
    start_urls = []

    try:
        with open(settings.SITE_LIST, "rb") as site_file:
            for l in site_file:
                if "http://" not in l:
                    start_urls.append("http://"+l.rstrip())
                else:
                    start_urls.append(l.rstrip())
    except: 
        log.msg("error: %s not exists" % settings.SITE_LIST, level=log.ERROR)
        raise

    log.msg("start_urls: %s" % start_urls, level=log.INFO)

    def __init__(self):
        dispatcher.connect(self.engine_stopped, signals.engine_stopped)


    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        urls = hxs.select('//a/@href').extract()

        domain = urlparse(response.url).netloc
        ds = domain.split('.')
        base1 = ds[-4]
        base2 = ds[-3]

        # make sure the parsed url is the domain related.
        for u in urls:
            if base1 in u or base2 in u:
                yield Request(u, self.mail_parser)


    def mail_parser(self, response):
        hxs = HtmlXPathSelector(response)
        item = EmItem()
        mailrex = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
        mailto = hxs.select("//a[@href]").re("mailto:(%s)" % mailrex)
        mail = mailto + hxs.select("//text()").re(mailrex)
 
        domain = urlparse(response.url).netloc.split('.')
        item['domain'] = '.'.join(domain[-4:])
        item['mail'] = list(set(mail))

        if len(item['mail'])>0:
            return item

        
    def engine_stopped(self):
        try:
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
                try:                             
                    with open(settings.SORTED_JSON, 'wb') as json_file:
                        json.dump(data, json_file)
                except:
                    log.msg("error: open %s" % settings.SORTED_JSON, level=log.ERROR)
                    raise
                                    
        except:
            log.msg("error: open %s" % settings.RAW_JSON, level=log.ERROR)
            raise
