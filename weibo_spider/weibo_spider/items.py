# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibospiderItem(scrapy.Item):
    id = scrapy.Field()
    idstr = scrapy.Field()
    created_at = scrapy.Field()
    user = scrapy.Field()
    text = scrapy.Field()