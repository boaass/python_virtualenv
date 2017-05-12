# -*- coding: utf-8 -*-

import json, re
import requests, cookielib
from scrapy.selector import Selector
from zhihu_login import Logging
from bs4 import BeautifulSoup

cookies = cookielib.LWPCookieJar('cookies')
session = requests.session()
session.cookies = cookies
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    Logging.debug(e.message)
    Logging.warning("cookies 加载失败 !!! 请重新运行 'zhihu_login.py'验证登录 !!!")


# 用户
class User(object):
    user_url = None

    def __init__(self, user_url, user_id=None):
        self.user_url = user_url


# 文章
class article(object):

    meta = None
    slug = None
    response = None

    def __init__(self, response):
        self.response = response

        html_content = re.compile(r'hidden\>(.*)\<\/textarea\>').findall(response.body)[-1]
        json_content = json.loads(html_content)

        self.slug = re.compile(r'\/(\d*)$').findall(response.url)[0]
        self.meta = json_content['database']['Post'][self.slug]



        # url = 'https://zhuanlan.zhihu.com%s' % self.meta['links']
        # Logging.debug(url)
        #
        # headers = {}
        # for (key, value) in response.request.headers.items():
        #     headers[key] = value[0]
        #
        # r = session.get(url, headers=headers)
        # Logging.debug('status_code: %s' % r.status_code)
        # if r.status_code == 200:
        #     s = json.loads(r.content)
        #     self.meta = s

    def author(self):
        return self.meta['author']

    def title(self):
        return self.meta['title']

    def content(self):
        all_str = self.meta['content']
        print all_str
        print '======================='

        soup = BeautifulSoup(all_str, 'lxml')
        contents = u''
        for element in soup.find_all('p'):
            if element.strings:
                contents = '\n'.join((contents, element.string))

        img_urls = []
        for element in soup.find_all('img', class_='origin_image zh-lightbox-thumb lazy'):
            img_urls.append(element['data-original'])

        return (contents, img_urls)

    def like_count(self):
        return self.meta['likeCount']

    def topics(self):
        topic_list = []
        for topic in self.meta['topics']:
            topic_list.append(topic['name'])

        return topic_list


class Answer(object):

    response = None
    meta = None

    def __init__(self, response):
        self.response = response

    def author(self):
        l = self.response.selector.xpath('//div[@class="AuthorInfo"]//a[@class="UserLink-link"]/text()').extract()
        if len(l)==0:
            return u'匿名用户'
        else:
            return l[0]

    def content(self):
        contents = ''
        for s in self.response.selector.xpath('//span[@class="RichText CopyrightRichText-richText"]').xpath('string(.)').extract():
            contents = '\n'.join((contents, s))

        img_urls = []
        for s in self.response.selector.xpath('//span[@class="RichText CopyrightRichText-richText"]//img[@class="origin_image zh-lightbox-thumb lazy"]/@data-original').extract():
            img_urls.append(s)

        return (contents, img_urls)



# 专栏
class Column(object):
    column_url = None
    meta = None
    slug = None

    def __init__(self, column_url, slug=None):
        self.column_url = column_url

        if slug == None:
            self.slug = re.compile(r'\/(\d*)$').findall(self.column_url)[0]
        else:
            self.slug = slug
