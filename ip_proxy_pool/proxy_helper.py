# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:04:41 2020

@author: zmddzf
"""

import urllib.request
import urllib
import re
import time
import random
import requests

class ProxyPool:
    """
    创建ip代理池
    """
    
    def __get_proxy(self, page_num):
        """
        爬取免费的IP代理
        """
        ip_title=[]
        ip_tables = []
        for i in range(1,int(page_num)):
            url='http://www.xicidaili.com/nt/'+str(i)
            headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64)"}
            request=urllib.request.Request(url=url,headers=headers)
            response=urllib.request.urlopen(request)
            content=response.read().decode('utf-8')
            pattern=re.compile('<td>(\d.*?|HTTP|HTTPS)</td>')
            ip_page=re.findall(pattern,str(content))
            ip_title.extend(ip_page)
            time.sleep(random.choice(range(1,3)))
        for i in range(0,len(ip_title),5):
            ip_tables.append({'ip':ip_title[i+2].lower() + '://' + ip_title[i], 'port':ip_title[i+1]})
        return ip_tables
    
    def check_proxy(self,ip_dict):
        """
        检查代理是否可用
        """
        ip_proxy = {ip_dict['ip'].split('//')[0][:-1]: ip_dict['ip'] + ':' + ip_dict['port']}
        print(ip_proxy)
        requests.adapters.DEFAULT_RETRIES = 3
        try:
            requests.get("http://icanhazip.com/",proxies=ip_proxy,timeout=6)
            return True, ip_proxy
        except:
            return False, ip_proxy
    
    def save_proxy(self, page_num, path):
        """
        存储ip代理
        """
        ip_tables = self.__get_proxy(page_num)
        with open(path, 'w') as f:
            for ip_dict in ip_tables:
                state, ip = self.check_proxy(ip_dict)
                print(state)
                if state:
                    f.writelines(str(ip_dict) + '\n')
        
    def select_proxy(self, ptype, path):
        """
        获取一个可用的proxy
        """
        ip_tables = []
        with open(path, 'r') as f:
            for line in f:
                ip_dict = eval(line)
                if ptype == ip_dict['ip'].split(':')[0]:
                    ip_tables.append(eval(line))
        while True:
            ip_proxy = random.choice(ip_tables)
            state, _ = self.check_proxy(ip_proxy)
            print(state)
            if state:
                return ip_proxy
        
        
        
        
        
        




