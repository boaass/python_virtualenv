# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    auth_name = scrapy.Field()
    icon_url = scrapy.Field()
    overview = scrapy.Field()
    data_itemid = scrapy.Field()
