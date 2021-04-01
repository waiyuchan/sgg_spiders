# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:06:15 2020

@author: zmddzf
"""

import scrapy
from gter_spider.items import Applicant, Offer
from bs4 import BeautifulSoup
import re


class OfferSpider(scrapy.spiders.Spider):
    name = "offer_spider"
    start_urls = ["http://www.gter.net/offer_{}.html".format(i) for i in range(4,40020)]
    
    
    def parse(self, response):
        
        # 定义申请人与offer两个item类
        applicants = Applicant()
        offers = Offer()
        
        # bs4解析网页
        html = response.body.decode('gbk')
        soup = BeautifulSoup(html, 'html.parser')
        
        # 找出目标表格
        tables = soup.findAll('table',attrs={'summary':re.compile('offer.*?')}) + soup.findAll('table',attrs={'summary':'offer 3'}) + soup.findAll('table', attrs={'summary':'个人情况'})
        
        # 是否找到？
        if len(tables) > 1:
            aid = response.url.split("/")[-1].split("-")[1]
            applicant = {'aid:':None, 'TOEFL:':None, 'IELTS:':None, 'GRE:':None,
                         'sub:':None, 'GMAT:':None, 'LSAT:':None, '本科学校档次:':None,
                         '本科专业:':None, '本科成绩和算法、排名:':None, '其他说明:':None,
                         '研究生专业:':None, '研究生成绩和算法、排名:':None,'研究生学校档次:':None}
            applicant['aid:'] = aid
            
            for tr in tables[-1].findAll('tr'):
                th = tr.find('th').text.strip().replace('\n','').replace('\r','')
                td = tr.find('td').text.strip().replace('\n','').replace('\r','')
                applicant[th.strip()] = td.strip()
            
            applicants['aid'] = applicant['aid:']
            applicants['TOEFL'] = applicant['TOEFL:']
            applicants['IELTS'] = applicant['IELTS:']
            applicants['GRE'] = applicant['GRE:']
            applicants['sub'] = applicant['sub:']
            applicants['GMAT'] = applicant['GMAT:']
            applicants['LSAT'] = applicant['LSAT:']
            applicants['ug_level'] = applicant['本科学校档次:']
            applicants['ug_major'] = applicant['本科专业:']
            applicants['ug_gpa'] = applicant['本科成绩和算法、排名:']
            applicants['pg_level'] = applicant['研究生学校档次:']
            applicants['pg_major'] = applicant['研究生专业:']
            applicants['pg_gpa'] = applicant['研究生成绩和算法、排名:']
            applicants['note'] = applicant['其他说明:']
            
            yield applicants
            
                
            print("==========================================================")
            print(applicant)
            
            for table in tables[:-1]:
                offer = {}
                offer['aid:'] = aid
                for tr in table.findAll('tr'):
                    th = tr.find('th').text.strip().replace('\n','').replace('\r','')
                    td = tr.find('td').text.strip().replace('\n','').replace('\r','')
                    offer[th.strip()] = td.strip()
                offers['aid'] = offer['aid:']
                offers['admission_school'] = offer['申请学校:']
                offers['admission_type'] = offer['学位:']
                offers['admission_major'] = offer['专业:'], 
                offers['apply_result'] = offer['申请结果:']
                offers['admission_year'] = offer['入学年份:']
                offers['admission_term'] = offer['入学学期:']
                offers['offer_date'] = offer['通知时间:']
                yield offers


        

        

