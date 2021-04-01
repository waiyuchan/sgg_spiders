# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:50:18 2020

@author: zmddzf
"""
import scrapy
from scrapy import Request
from weibo_spider.items import WeibospiderItem
import json
from pyquery import PyQuery as pq
import time

class WeiboSpider(scrapy.spiders.Spider):
    name = 'weibo_spider'
    allowed_domains = ['m.weibo.cn']
    handle_httpstatus_list = [403, 404, 418]
    cookies ={'_T_WM': '89973670882',
             'WEIBOCN_FROM': '1110006030',
             'MLOGIN': '1',
             'ALF': '1588779689',
             'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWaiTFpgF7sWpCCBM8HHSp55JpX5K-hUgL.Fo-R1hz7SK50eo-2dJLoIpiCqPxDdc4yd2LEMJ8XIgvVqg7t',
             'SCF': 'Aj8ynMNClId5tGTKnGrmkNXp-4VBt_JE1auEmPjS6HeaSdW_QUhTKLEFB6jqtidHTVWyX0MFWqe9aTo-v_q7-74.',
             'SUB': '_2A25zjyA4DeRhGeNG41AR9S7PyTmIHXVRcEBwrDV6PUJbktANLXXAkW1NSwIY7Q7hfUYiVibTGipE_68JrIQ7Qe-6',
             'SUHB': '0M2FjqVxSEdS7i',
             'SSOLoginState': '1586188393',
             'XSRF-TOKEN': '56923f'}
    # 微博
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
    # 用户
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    start_uids = [
        '1824301624',  # cook
        '7330842801',  # offer bobao
        '7029497065',  # UK offer yaya
    ]

    def start_requests(self):
        for uid in self.start_uids:
            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                          meta={'page': 1, 'uid': uid})
            #yield Request(self.user_url.format(uid=uid), callback=self.parse_user)  
            
    
    def parse_weibos(self, response):

        result = json.loads(response.text)
        if result.get('ok') == 1 and result.get('data').get('cards'):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                # 判断是否存在mblog
                if mblog:
                    weibo_item = WeibospiderItem()
                    weibo_item['id'] = mblog.get('id')  # 微博id
                    weibo_item['idstr'] = mblog.get('idstr')
                    weibo_item['created_at'] = mblog.get('created_at')
                    weibo_item['user'] = response.meta.get('uid') # 用户id
                    print("===============================================================")
                    print(weibo_item)
                    # 检测有没有阅读全文:
                    all_text = mblog.get('text')
                    if '>全文<' in all_text:
                        # 微博全文页面链接
                        all_text_url = 'https://m.weibo.cn/statuses/extend?id=' + mblog.get('id') + "&sudaref=login.sina.com.cn"
                        yield Request(all_text_url, callback=self.parse_all_text, meta={'item': weibo_item}, cookies = self.cookies)

                    else:
                        text = pq(mblog.get('text')).text().replace('\n', '')
                        text = ''.join([x.strip() for x in text])
                        weibo_item['text'] = text
                        yield weibo_item

            # 下一页微博
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos,
                          meta={'uid': uid, 'page': page})

    # 有阅读全文的情况，获取全文
    def parse_all_text(self, response):
        print('=============================================================')
        print('=============================================================')
        print(response.text)
        print('=============================================================')
        print('=============================================================')

        result = json.loads(response.text)
        if result.get('ok') and result.get('data'):
            weibo_item = response.meta['item']
            all_text = result.get('data').get('longTextContent')
            text = pq(all_text).text().replace('\n', '')
            text = ''.join([x.strip() for x in text])
            weibo_item['text'] = text
            print(weibo_item)
            time.sleep(3)


            yield weibo_item
    
    
            
            
    