# -*- coding: utf-8 -*-
import scrapy
import requests, cookielib
import sys, codecs
import json

from auth import Logging
from bs4 import BeautifulSoup
from ..items import ZhihuSpiderItem

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

cookie_jar = cookielib.LWPCookieJar('cookies')
try:
    cookie_jar.load(ignore_discard=True)
except Exception as e:
    Logging.error("你还没有登录知乎哦 ...")
    Logging.info("执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")

class AuthorSpider(scrapy.Spider):
    name = "author"
    allowed_domains = ["zhihu.com"]

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        }

        # LWPCookieJar对象转字典类型
        cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)
        return [scrapy.Request(url='https://www.zhihu.com/', headers=headers, cookies=cookie_dict, meta={'dont_redirect': True, 'cookies': cookie_dict}, callback=self.parse_data_to_request)]

    def catch_last_itemid_from_content(self, response):
        Logging.info("catch itemid ... ")

        if response.url.endswith('TopStory2FeedList'):
            parse_data = json.loads(response.body_as_unicode())['msg'][-1]

            bs_data = BeautifulSoup(parse_data, "lxml")
            item_id = bs_data.find_all('div', {'class' : 'undo-dislike-options'})[-1].get('data-item_id')
        else:
            item_id = response.xpath("//div[@class='undo-dislike-options']/@data-item_id").extract()[-1]

        Logging.info("item_id: %s" % item_id)
        return item_id

    def catch_offset_from_content(self, response):
        if response.meta.has_key('offset'):
            offset = int(str(response.meta['offset']))+10
        else:
            offset = 10

        Logging.info("offset = %s" % offset)
        return offset

    def parse_data_to_request(self, response):

        # parse item
        if response.url.endswith('TopStory2FeedList'):
            for parse_data in json.loads(response.body_as_unicode())['msg']:
                parse_data = parse_data.encode('utf-8')

                f = open('parse_data.json', 'a+')
                f.write(parse_data)
                f.close()

                bs_data = BeautifulSoup(parse_data, "lxml")
                authors = bs_data.find_all('a', attrs={'class':'author-link'})

                for author in authors:
                    item = ZhihuSpiderItem()
                    auth_name = author.string

                    f = open('auth_name.text', 'a+')
                    f.write(auth_name.encode('utf-8'))
                    f.write(' ')
                    f.close()

                    item['auth_name'] = auth_name

                    yield item
        else:
            authors = response.xpath("//a[@class='author-link']/text()")
            for author in authors:
                item = ZhihuSpiderItem()
                auth_name = author.extract()

                f = open('auth_name.text','a+')
                f.write(auth_name.encode('utf-8'))
                f.write(' ')
                f.close()

                item['auth_name'] = auth_name

                yield item

        item_id = self.catch_last_itemid_from_content(response)

        offset = offset = self.catch_offset_from_content(response)

        if offset > 10:
            Logging.success("over ... ")
            return
        else:
            # circle request
            form_data = {
                 'params' : '{"offset":%s,"start":%s}' % (offset, item_id),
                 'method' : 'next'
            }

            cookie_dict = response.meta['cookies']
            xsrf = cookie_dict['_xsrf']
            Logging.info("xsrf = %s" % xsrf)

            headers = {
                 'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                 "X-Requested-With": "XMLHttpRequest",
                 "X-Xsrftoken": xsrf
             }
            yield scrapy.FormRequest(url='https://www.zhihu.com/node/TopStory2FeedList', headers=headers, cookies=response.meta['cookies'], formdata=form_data, meta={'dont_redirect': True, 'offset': str(offset), 'cookies': cookie_dict}, callback=self.parse_data_to_request)

