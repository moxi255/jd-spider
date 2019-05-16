# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComputerSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    img_url = scrapy.Field()
    param = scrapy.Field()
