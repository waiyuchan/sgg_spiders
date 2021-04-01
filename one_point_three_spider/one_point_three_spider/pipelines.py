# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from one_point_three_spider.items import OnePointThreeSpiderItem


class OnePointThreeSpiderPipeline(object):
    def __init__(self):
        self.file_offer = open('./data/offer.csv', 'w')
        self.writer1 = csv.writer(self.file_offer)
        self.writer1.writerow(['aid', '申请学校', '学位', '专业', '具体项目名称', '申请结果',
                               '入学年份', '入学学期', '通知时间'])

        self.file_applicants = open('./data/applicants.csv', 'w')
        self.writer2 = csv.writer(self.file_applicants)
        self.writer2.writerow(['aid', 'TOEFL or IELTS', 'GRE or GMAT',
                               '本科学校档次', '本科学校名称', '本科专业',
                               '本科成绩和算法、排名', '研究生学校档次', '研究生学校名称',
                               '研究生专业', '研究生成绩和算法、排名',
                               '其他说明'])

    def process_item(self, item, spider):
        item_db = item
        offer_data = [item_db['aid'], item_db['admission_school'], item_db['admission_type'],
                      item_db['admission_major'], item_db['admission_project_name'],
                      item_db['apply_result'], item_db['admission_year'],
                      item_db['admission_term'], item_db['offer_date']]
        applicants_data = [item_db['aid'], item_db['english_grade'], item_db['g_grade'],
                           item_db['ug_level'], item_db['ug_school'], item_db['ug_major'],
                           item_db['ug_gpa'], item_db['pg_level'], item_db['pg_school'],
                           item_db['pg_major'], item_db['pg_gpa'], item_db['note']]

        self.writer1.writerow(offer_data)
        self.writer2.writerow(applicants_data)
        self.file_offer.flush()
        self.file_applicants.flush()

        return item

    def close_spider(self, spider):
        self.file_offer.close()
        self.file_applicants.close()
