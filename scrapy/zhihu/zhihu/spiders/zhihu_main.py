# -*- coding: utf-8 -*-
import scrapy
import cookielib
import requests

from scrapy.selector import Selector
from ..items import ZhihuItem
from zhihu_login import Logging
from zhihu import article

cookies = cookielib.LWPCookieJar('cookies')
try:
    cookies.load(ignore_discard=True)
except Exception as e:
    Logging.debug(e.message)
    Logging.warning("cookies 加载失败 !!! 请重新运行 'zhihu_login.py'验证登录 !!!")


class ZhihuMainSpider(scrapy.Spider):
    name = "zhihu_main"
    allowed_domains = ["zhihu.com"]

    def __init__(self):
        self.parse_article_count = 0
        self.pase_column_count = 0

    def start_requests(self):
        url = "https://www.zhihu.com/collection/43268381"
        cookies_dict = requests.utils.dict_from_cookiejar(cookies)
        return [scrapy.Request(url, cookies=cookies_dict, meta={'cookies':cookies_dict}, callback=self.parse_page_number)]


    def parse_page_number(self, response):
        # 获取页数
        page_urls = response.selector.xpath('//div[@class="zm-invite-pager"]/span/a/@href').extract()
        page_count = 0
        for url_extention in page_urls:
            page_count = max(page_count, int(url_extention.split('?page=')[-1]))
            url = ''.join((response.url, url_extention))
            Logging.info(url)
        Logging.info('page_count: %d' % page_count)

        page_count = 1
        for index in xrange(1, page_count+1):
            url = response.url + '?page=%d' % index
            yield scrapy.Request(url, cookies=response.meta['cookies'], meta=response.meta, callback=self.parse_request_url)

    def parse_request_url(self, response):

        base_url = 'https://www.zhihu.com'
        urls = response.selector.xpath('//a[@class="toggle-expand"]/@href').extract()
        for url in urls:
            if not url.startswith('https://'):
                # 普通文章
                url = ''.join((base_url, url))
                yield scrapy.Request(url, cookies=response.meta['cookies'], meta=response.meta, callback=self.parse_article)
            else:
                # 专栏
                yield scrapy.Request(url, cookies=response.meta['cookies'], meta=response.meta, callback=self.pase_column)
            # Logging.info(url)

    def parse_article(self, response):
        self.parse_article_count += 1
        # Logging.info('======================%d' % self.parse_article_count)
        # Logging.info(response.url)
        return


    def pase_column(self, response):
        self.pase_column_count += 1
        Logging.info('++++++++++++++++++++++%d' % self.pase_column_count)


        Logging.info('author: %s' % article(response).author())
        Logging.info('title: %s' % article(response).title())

        return