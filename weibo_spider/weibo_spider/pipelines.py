# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
import re

class WeibospiderPipeline(object):
    def __init__(self):
        self.f1 = open("./data/weibo.csv", "w")
        self.writer1 = csv.writer(self.f1)
        self.writer1.writerow(['uid', 'wid', 'date', 'content',])
        
    def filter_emoji(self, data):
        """
        清除表情符号
        :param sentence: 待清洗句子
        :return sent: 清洗后句子
        """
        restr = ''
        co = re.compile(u'[\U00010000-\U0010ffff]')
        sent = co.sub(restr, data)
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        sent = co.sub(restr, sent)
        #co = re.compile(u'[\u0000-\uFFFF]')
        #sent = co.sub(restr, sent)
        co = re.compile(u'[\u2000-\u2FFF]')
        sent = co.sub(restr, sent)
        return sent
    
    def parse_time(self, date):
        if re.match('刚刚', date) or re.match('\d+分钟前', date) or re.match('\d+小时前', date):
            date = time.strftime('%Y-%m-%d')
        if re.match('昨天.*', date):
            date = re.match('昨天(.*)', date).group(1).strip()
            date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date
        return date

    def process_item(self, item, spider):
        data = [item['user'], item['id'], self.parse_time(item['created_at']), self.filter_emoji(item['text'])]
        self.writer1.writerow(data)
        return item
    
    
    def close_spider(self, offer_spider):
        self.f1.close()
