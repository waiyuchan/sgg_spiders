# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from weibo_spider.settings import USER_AGENT_LIST
import random
import urllib.request
import urllib
import re
import time
import requests
#from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

#class CookiesMiddleware(object):
#    """
#    每次请求都随机从账号池中选择一个账号去访问
#    """
"""    def process_request(self, request, spider):
        cookies ={'SINAGLOBAL': '923182067266.7612.1519890485298',
                     'wb_view_log_6919976524': '1368*9122',
                     'Ugrow-G0': 'd52660735d1ea4ed313e0beb68c05fc5',
                     'login_sid_t': '9c1aebef95898e8b5d1677aa75c19c00',
                     'cross_origin_proto': 'SSL',
                     'TC-V5-G0': 'eb26629f4af10d42f0485dca5a8e5e20',
                     '_s_tentry': 'login.sina.com.cn',
                     'UOR': ',,login.sina.com.cn',
                     'wb_view_log': '1368*9122',
                     'Apache': '7226527777167.757.1586184712940',
                     'ULV': '1586184712947:75:4:3:7226527777167.757.1586184712940:1586170607039',
                     'un': '17754928746',
                     'wb_view_log_5882050325': '1368*9122',
                     'TC-Page-G0': '62b98c0fc3e291bc0c7511933c1b13ad|1586187666|1586187629',
                     'webim_unReadCount': '%7B%22time%22%3A1586187669490%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D',
                     'WBStorage': '42212210b087ca50|undefined',
                     'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWaiTFpgF7sWpCCBM8HHSp55JpX5K2hUgL.Fo-R1hz7SK50eo-2dJLoIpiCqPxDdc4yd2LEMJ8XIgvVqg7t',
                     'ALF': '1617723689',
                     'SSOLoginState': '1586187689',
                     'SCF': 'Aj8ynMNClId5tGTKnGrmkNXp-4VBt_JE1auEmPjS6HeaNJLh6SoL69HFRph9KuSQK9dCmYjx6uf6Jx4nbgHT1EA.',
                     'SUB': '_2A25zjz35DeRhGeNG41AR9S7PyTmIHXVQ_SgxrDV8PUNbmtAKLRL3kW9NSwIY7SMvKgvQ5b96HfT3jOjmlx1_LVh7',
                     'SUHB': '0M2FjqVxSEdSFA'}
        request.cookies = cookies"""


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



class MyproxiesSpiderMiddleware(object):
       
      def process_request(self, request, spider):
          pp = ProxyPool()
          ip = pp.select_proxy('https','C:/Users/zmddzf/Desktop/学习/科研/申公公/Spiders/ip_proxy_pool/ip_proxy_pool.txt')
          request.meta["proxy"] = ip['ip'] + ':' + ip['port']



class RandomUserAgentDownloaderMiddleware(object):
    # Randomly choice UA and add to request before download
    def process_request(self, request, spider):
        # Randomly choice a UA
        user_agent = random.choice(USER_AGENT_LIST)
        # Add UA into request
        request.headers['User-Agent'] = user_agent


class WeibospiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeibospiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
