# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OnePointThreeSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # applicant data
    aid = scrapy.Field()
    link = scrapy.Field()
    ug_level = scrapy.Field()  # 本科学校档次
    ug_school = scrapy.Field()  # 本科学校名称
    ug_major = scrapy.Field()
    ug_gpa = scrapy.Field()
    pg_level = scrapy.Field()  # 研究生学校档次
    pg_school = scrapy.Field()
    pg_major = scrapy.Field()
    pg_gpa = scrapy.Field()
    english_grade = scrapy.Field()  # Toefl or Ielts
    g_grade = scrapy.Field()  # gre or gmat
    note = scrapy.Field()  # 其他说明
    # offer data
    admission_school = scrapy.Field()  # 申请学校
    admission_major = scrapy.Field()  # 申请专业
    admission_year = scrapy.Field()  # 入学年份
    admission_term = scrapy.Field()  # 入学学期
    admission_type = scrapy.Field()  # MS or PhD
    admission_project_name = scrapy.Field()  # 具体项目名称
    apply_result = scrapy.Field()  # 申请结果
    offer_date = scrapy.Field()  # 通知时间

    pass
