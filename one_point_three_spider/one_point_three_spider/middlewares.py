# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

"""
    
class CookiesMiddleware(object):
    
    def process_request(self, request, spider):
        cookie = '_ga=GA1.2.907173391.1584854024; __gads=ID=95425e14432ed1cd:T=1584854878:S=ALNI_MZ7UVh68CZhnRGLZiGXxBV-TofR2g; __cfduid=dbdfba4ff203f8478901eb99c04de96551584861606; PHPSESSID=f9h412m1o7j2huvcsk7ahlfc21; _gid=GA1.2.2131170173.1585401523; 4Oaf_61d6_saltkey=byvcvc37; 4Oaf_61d6_lastvisit=1585397946; 4Oaf_61d6_home_diymode=1; 4Oaf_61d6_atarget=1; 4Oaf_61d6_visitedfid=82; 4Oaf_61d6_auth=00458KoSZb8J66hzI%2B714%2BEwuxvgMCZOVitDAtUoX%2FdSuAAlxHoARvu580ZZKWxeRFtyIKh9G22Z%2BP2bV3G2YUS76nY; 4Oaf_61d6_lastcheckfeed=603729%7C1585413747; 4Oaf_61d6_lip=119.135.207.182%2C1585413747; 4Oaf_61d6_member_login_status=1; 4Oaf_61d6_forum_lastvisit=D_82_1585568822; 4Oaf_61d6_ulastactivity=1585575113%7C0; 4Oaf_61d6_cookie_hash=24c70647c01e756519f8068d522c1a4d; 4Oaf_61d6_viewid=tid_616854; 4Oaf_61d6_noticeTitle=1; 4Oaf_61d6_lastact=1585576344%09forum.php%09misc'
        line = cookie.replace('\r', '').replace(' ', '')
        line = line.split(';')

        cookies = {}
        for i in line:
            key, value = i.split('=', 1)
            cookies[key] = value
        request.headers.setdefault('Cookie', cookies)
"""


class OnePointThreeSpiderMiddleware(object):
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


class OnePointThreeSpiderDownloaderMiddleware(object):
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
        cookie = '_ga=GA1.2.907173391.1584854024; __gads=ID=95425e14432ed1cd:T=1584854878:S=ALNI_MZ7UVh68CZhnRGLZiGXxBV-TofR2g; __cfduid=dbdfba4ff203f8478901eb99c04de96551584861606; PHPSESSID=f9h412m1o7j2huvcsk7ahlfc21; _gid=GA1.2.2131170173.1585401523; 4Oaf_61d6_saltkey=byvcvc37; 4Oaf_61d6_lastvisit=1585397946; 4Oaf_61d6_home_diymode=1; 4Oaf_61d6_atarget=1; 4Oaf_61d6_visitedfid=82; 4Oaf_61d6_auth=00458KoSZb8J66hzI%2B714%2BEwuxvgMCZOVitDAtUoX%2FdSuAAlxHoARvu580ZZKWxeRFtyIKh9G22Z%2BP2bV3G2YUS76nY; 4Oaf_61d6_lastcheckfeed=603729%7C1585413747; 4Oaf_61d6_lip=119.135.207.182%2C1585413747; 4Oaf_61d6_member_login_status=1; 4Oaf_61d6_forum_lastvisit=D_82_1585568822; 4Oaf_61d6_ulastactivity=1585575113%7C0; 4Oaf_61d6_cookie_hash=24c70647c01e756519f8068d522c1a4d; 4Oaf_61d6_viewid=tid_616854; 4Oaf_61d6_noticeTitle=1; 4Oaf_61d6_lastact=1585576344%09forum.php%09misc'
        line = cookie.replace('\r', '').replace(' ', '')
        line = line.split(';')

        cookies = {}
        for i in line:
            key, value = i.split('=', 1)
            cookies[key] = value
        request.headers.setdefault('Cookie', cookies)

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
