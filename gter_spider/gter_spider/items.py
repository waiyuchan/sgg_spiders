# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Applicant(scrapy.Item):
    aid = scrapy.Field()
    TOEFL = scrapy.Field()
    IELTS = scrapy.Field()
    GRE = scrapy.Field()
    sub = scrapy.Field()
    GMAT = scrapy.Field()
    LSAT = scrapy.Field()
    ug_level = scrapy.Field()  # 本科
    ug_major = scrapy.Field()
    ug_gpa = scrapy.Field()
    pg_level = scrapy.Field()  # 研究生
    pg_major = scrapy.Field()
    pg_gpa = scrapy.Field()
    note = scrapy.Field()  # 其他说明
    
class Offer(scrapy.Item):
    aid = scrapy.Field()
    admission_school = scrapy.Field()  # 学校
    admission_major = scrapy.Field()  # 专业
    admission_year = scrapy.Field()  # 入学年份
    admission_type = scrapy.Field()  # 学位类型
    admission_term = scrapy.Field()  # 学期
    apply_result = scrapy.Field()  # 申请结果
    offer_date = scrapy.Field()  # 通知时间
    