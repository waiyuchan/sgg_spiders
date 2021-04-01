# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from gter_spider.items import Applicant, Offer

class GterspiderPipeline(object):
    def __init__(self):
        # 打开文件写入表头
        self.f1 = open("./data/offer1.csv", "w")
        self.writer1 = csv.writer(self.f1)
        self.writer1.writerow(['aid', '申请学校', '学位', '专业', '申请结果', 
                               '入学年份', '入学学期', '通知时间'])
        
        self.f2 = open("./data/applicants1.csv", "w")
        self.writer2 = csv.writer(self.f2)
        self.writer2.writerow(['aid', 'TOEFL', 'IELTS', 'GRE', 'sub', 'GMAT', 
                               'LSAT', '本科学校档次','本科专业', 
                               '本科成绩和算法、排名', '其他说明','研究生专业', 
                               '研究生成绩和算法、排名',
                               '研究生学校档次'])
        
    def process_item(self, item, offer_spider):
        
        # offer写入
        if isinstance(item, Offer):
            data = [item['aid'], item['admission_school'], item['admission_type'],
                    item['admission_major'], item['apply_result'], item['admission_year'],
                    item['admission_term'], item['offer_date']]
            self.writer1.writerow(data)
        
        # 申请人写入
        if isinstance(item, Applicant):
            data = [item['aid'], item['TOEFL'], item['IELTS'], item['GRE'], item['sub'],
                    item['GMAT'], item['LSAT'], item['ug_level'], item['ug_major'],
                    item['ug_gpa'], item['note'], item['pg_major'], item['pg_gpa'],
                    item['pg_level']]
            self.writer2.writerow(data)
    
    def close_spider(self, offer_spider):#关闭
        self.f1.close()
        self.f2.close()
        
        
        