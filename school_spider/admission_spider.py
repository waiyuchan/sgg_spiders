# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 16:18:31 2020

@author: zmddzf
"""

import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://m.baidu.com/sf?word={}&pd=education_school&openapi=1&dspName=iphone&from_sf=1&resource_id=5200&group={}&ext=%7B%22sf_tab_name%22%3A%22intro%22%7D&title={}&country={}&lid=8669480809547502925&referlid=8669480809547502925&ms=1&frsrcid=5175&frorder=1'

baike_url = 'https://baike.baidu.com/item/{}'

page_dict = {'admission':'47250', 'college': '47251', 'special': '47248'}

school = pd.read_csv('./data/school_list.csv')

headers = {
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
          }


texts = []
for s in school.school:
    
    text = {'name': s}
    
    resp = requests.get(baike_url.format(s), headers=headers)
    html = resp.text
    soup = BeautifulSoup(html, 'html')
    intr = soup.find('div', attrs={'class':"lemma-summary"})
    if intr:
        intr = intr.get_text()
        intr = re.sub("[\\\n\\\xa0]|\\[.*?]", '', intr)
    else:
        intr = ""
    text['title'] = intr
    
    
    resp = requests.get(url.format(s, page_dict['special'], s, '英国'))
    html = resp.text
    soup = BeautifulSoup(html, 'html')
    jsn = json.loads(soup.find_all('script', type="application/json")[1].string)
    print(s)
    
    for i in range(len(jsn['data']['result'])):
        name = jsn['data']['result'][i]['result']['text']
        descrp = ''.join(jsn['data']['result'][i]['result']['description'])
        text[name] = descrp
    
    texts.append(text)
    
dt = pd.DataFrame(texts)
dt.to_csv('./data/院校信息.csv')


    
texts = []
exams = []

for s in school.school:    
    text = {'name': s}
    print(s)
    
    try: 
        resp = requests.get(url.format(s, page_dict['admission'], s, '英国'))
        html = resp.text
        soup = BeautifulSoup(html, 'html')
        jsn = json.loads(soup.find_all('script', type="application/json")[1].string)['data']['result'][1]
    except Exception as e:
        print(e)
    
    try:
        text[jsn['applicationMaterials']['text']] = '。'.join(jsn['applicationMaterials']['description'])
    except Exception as e:
        print(e)
    
    try:
        for i in jsn['examRequirement']['mainExams']:
            i['name'] = s
            exams.append(i)
    except Exception as e:
        print(e)
    
    try:
        for i in list(jsn['priceSpecification'].keys())[:-1]:
            text[jsn['priceSpecification'][i]['text']] = jsn['priceSpecification'][i]['price']
    except Exception as e:
        print(e)
        
    try:
        for i in list(jsn['contactInfo']):
            text[i['text']] = i['content']
    except Exception as e:
        print(e)
        
    texts.append(text)
    
dt = pd.DataFrame(texts)
dt.to_csv('./data/招生信息')
dt1 = pd.DataFrame(exams)
dt1.to_csv('./data/成绩要求.csv')


texts = []
majors = {}
for s in school.school:
    resp = requests.get(url.format(s, page_dict['college'], s, '英国'))
    html = resp.text
    soup = BeautifulSoup(html, 'html')
    script = soup.find_all('script', type="application/json")
    
    text = {'name': s}
    
    for i in script:
        x = json.loads(i.string)
        if 'data' not in x:
            continue
        
        if 'content' in x['data']:
            text[x['data']['text']] = ''.join(list(x['data']['content'][0]['description']))
            
            texts.append(text)
        
        elif 'infor' in x['data']:
            majors[s] = []
            for j in x['data']['infor'][0]['result']:
                majors[s].append(j)
                
                
        else:
            continue
                
dt = pd.DataFrame(texts)
dt.to_csv('./data/院校安排')

with open('./data/专业内容.json', 'w') as f:
    json.dump(majors, f)
            
    
    







