# -*- coding: utf-8 -*-

import json, re
import requests, cookielib
from scrapy.selector import Selector
from zhihu_login import Logging

cookies = cookielib.LWPCookieJar('cookies')
session = requests.session()
session.cookies = cookies
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    Logging.debug(e.message)
    Logging.warning("cookies 加载失败 !!! 请重新运行 'zhihu_login.py'验证登录 !!!")

class article(object):

    meta = None
    post_id = ''

    def __init__(self, response):
        self.meta = response.body
        # post_id = re.compile(r'\{\"(\d*)\"\:').findall(self.meta)[0]
        post_id = re.compile(r'\/(\d*)$').findall(response.url)[0]
        url = 'https://zhuanlan.zhihu.com/api/posts/%s' % post_id + '/contributed'
        Logging.debug(url)

        headers = {}
        for (key, value) in response.request.headers.items():
            headers[key] = value[0]

        r = session.get(url, headers=headers)
        Logging.debug('status_code: %s' % r.status_code)
        if r.status_code == 200:
            s = json.loads(r.content)
            self.meta = s

    def author(self):
        return self.meta[0]['targetPost']['author']['name'].encode('utf-8')

    def title(self):
        return self.meta[0]['targetPost']['title'].encode('utf-8')