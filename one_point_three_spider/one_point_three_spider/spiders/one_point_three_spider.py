from scrapy.spiders import *
from one_point_three_spider.items import OnePointThreeSpiderItem
from bs4 import BeautifulSoup
import re
import urllib


class OnePointThreeSpider(Spider):
    name = "one_point_three_spiders"
    allowed_domains = ["1point3acres.com"]
    start_url = "http://www.1point3acres.com/bbs/forum-82-1.html"
    base_url = "https://www.1point3acres.com/bbs/"
    # base_url = "https://www.1point3acres.com/bbs/"

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
              # 'Accept-Encoding': 'gzip, deflate, br',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    # 原始cookie
    Cookie = '_ga=GA1.2.907173391.1584854024; __gads=ID=95425e14432ed1cd:T=1584854878:S=ALNI_MZ7UVh68CZhnRGLZiGXxBV-TofR2g; __cfduid=dbdfba4ff203f8478901eb99c04de96551584861606; PHPSESSID=f9h412m1o7j2huvcsk7ahlfc21; _gid=GA1.2.2131170173.1585401523; 4Oaf_61d6_saltkey=pD1q2QWD; 4Oaf_61d6_lastvisit=1585654644; 4Oaf_61d6_atarget=1; 4Oaf_61d6_visitedfid=82; 4Oaf_61d6_auth=d8fdsSP8V%2FqK1JRQPduCnpE4oX0dJ8%2FrxcWIrn0rez%2F%2FVZ50D%2BCCeQcxC%2B512j%2BPYSKDn6Iq2SNicnVyg03ppvf3IhI; 4Oaf_61d6_lastcheckfeed=603729%7C1585658251; 4Oaf_61d6_lip=113.74.230.191%2C1585658251; 4Oaf_61d6_member_login_status=1; 4Oaf_61d6_cookie_hash=a39b21fc13dcdeaf745df91a60fccf6e; 4Oaf_61d6_home_diymode=1; 4Oaf_61d6_nofavfid=1; 4Oaf_61d6_forum_lastvisit=D_82_1585677863; 4Oaf_61d6_ulastactivity=1585677863%7C0; 4Oaf_61d6_viewid=tid_619279; 4Oaf_61d6_lastact=1585678207%09forum.php%09misc'
    # 字典形式
    cookie = {'_ga': 'GA1.2.907173391.1584854024', '__gads': 'ID=95425e14432ed1cd:T=1584854878:S=ALNI_MZ7UVh68CZhnRGLZiGXxBV-TofR2g', '__cfduid': 'dbdfba4ff203f8478901eb99c04de96551584861606', 'PHPSESSID': 'f9h412m1o7j2huvcsk7ahlfc21', '_gid': 'GA1.2.2131170173.1585401523', '_gat': '1', '4Oaf_61d6_saltkey': 'pD1q2QWD', '4Oaf_61d6_lastvisit': '1585654644', '4Oaf_61d6_atarget': '1', '4Oaf_61d6_visitedfid': '82', '4Oaf_61d6_sendmail': '1', '4Oaf_61d6_ulastactivity': '1585658251%7C0', '4Oaf_61d6_auth': 'd8fdsSP8V%2FqK1JRQPduCnpE4oX0dJ8%2FrxcWIrn0rez%2F%2FVZ50D%2BCCeQcxC%2B512j%2BPYSKDn6Iq2SNicnVyg03ppvf3IhI', '4Oaf_61d6_lastcheckfeed': '603729%7C1585658251', '4Oaf_61d6_checkfollow': '1', '4Oaf_61d6_lip': '113.74.230.191%2C1585658251', '4Oaf_61d6_member_login_status': '1', '4Oaf_61d6_forum_lastvisit': 'D_82_1585658253', '4Oaf_61d6_lastact': '1585658255%09home.php%09spacecp', '4Oaf_61d6_checkpm': '1'}

    def get_next_url(self, oldurl):
        u = oldurl.split('-')
        page_number = int(u[2].split('.')[0])
        new_number = page_number+1
        if new_number <= 1000:
            next_url = u[0] + "-" + u[1] + "-" + str(new_number) + ".html"
            return str(next_url)
        else:
            return

    def start_requests(self):
        yield Request(self.start_url)

    def request_page(self, start_url):
        url = start_url
        while url is not None:
            yield Request(url, self.parse)
            url = self.get_next_page(url)

    # 解析二级页面，获取具体录取信息
    def parse_detail(self, response):
        offer = {}
        ajax_url = '&inajax=1&ajaxtarget='  # 用于构建ajax请求url
        html = response.body.decode(encoding='gbk', errors='ignore')
        # iCookie = response.request.headers.getlist('Cookie')
        item = response.meta['item']
        referer = str(item['link']).replace('&page=2>2</a>', '')
        # 构造请求头
        headers = self.headers
        headers['Referer'] = referer
        headers['Cookie'] = self.Cookie

        # 读网页信息
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.findAll('table', attrs={'summary': '分类信息'})
        for i in table:
            for tr in i.findAll('tr'):
                th = tr.find('th').text.strip().replace('\n', '').replace('\r', '')
                td = tr.find('td').text.strip().replace('\n', '').replace('\r', '')
                offer[th.strip()] = td.strip()

                if(tr.find('td').children is not None):
                    for i in tr.find('td').children:

                        if(re.search(r'id="\S*"', str(i)) is not None):
                            id = re.search(r'id="\S*"', str(i)).group().replace('id="', '').replace('"', '')
                            link = re.search(r'forum.php(\S*)\'', str(i)).group().replace('amp;', '').replace('\'', '')
                            url = self.base_url + link + ajax_url + id
                            req = urllib.request.Request(url=url, headers=headers)
                            res = urllib.request.urlopen(req)
                            xml = res.read().decode(encoding='gbk', errors='ignore')
                            if(re.search('CDATA\[\S*\]', xml) is not None):
                                data = re.search('CDATA\[\S*\]', xml).group().replace('CDATA[', '').replace(']]', '')
                                offer[th.strip()] = data.strip()

                            # print(url)
        # item赋值
        item['admission_year'] = offer.get('申入学年度:')
        item['admission_term'] = offer.get('入学学期:')
        item['admission_major'] = offer.get('专业:')
        item['admission_project_name'] = offer.get('具体项目名称:')
        item['admission_type'] = offer.get('学位:')
        item['apply_result'] = offer.get('申请结果:')
        item['admission_school'] = offer.get('学校名称:')
        item['offer_date'] = offer.get('通知时间:')
        item['ug_level'] = offer.get('本科学校档次:')
        item['ug_school'] = offer.get('本科学校名称:')
        item['ug_major'] = offer.get('本科专业:')
        item['ug_gpa'] = offer.get('本科成绩和算法，排名:')
        item['pg_level'] = offer.get('研究生学校档次:')
        item['pg_school'] = offer.get('研究生学校名称:')
        item['pg_major'] = offer.get('研究生专业:')
        item['pg_gpa'] = offer.get('研究生成绩和算法，排名:')
        item['english_grade'] = offer.get('T单项和总分:')
        item['g_grade'] = offer.get('G单项和总分:')
        item['note'] = offer.get('背景的其他说明（如牛推等）:')
        for key, value in item.items():
            if(value is None):
                item[key] = ''

        if(item['admission_year'] !=''):
            yield item


    # 解析一级页面，获取二级页面链接
    def parse(self, response):
        item = OnePointThreeSpiderItem()

        html = response.body.decode(encoding='gbk', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.findAll('tbody', attrs={'id': re.compile(r"normalthread(\S*)")})
        # 获取子页面链接以及id号
        for i in tbody:
            th = i.findAll('th')
            for j in th:
                links = j.findAll('a', attrs={'href': re.compile(r"forum.php\?mod=viewthread&tid(\S*)")})
                for k in links:
                    link = str(k).replace('amp;', '')
                    link = re.search(r"forum.php\?mod=viewthread&tid(\S*)", link).group()
                    tid = re.search(r"tid=\d{6,}", link).group().replace('tid=', '')
                    url = self.base_url + link
                    url = url.replace('"', '')
                    item['aid'] = tid
                    item['link'] = url

                    yield Request(url=url, cookies=self.cookie, callback=self.parse_detail, meta={'item': item})
                    # print(tid)

        next_url = self.get_next_url(response.url)
        if next_url is not None:
            yield Request(next_url, callback=self.parse)
