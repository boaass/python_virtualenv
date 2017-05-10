# -*- coding: utf-8 -*-
import scrapy
import cookielib
import requests
from ..items import ZhihuItem
from scrapy.selector import Selector
from zhihu_login import Logging

cookies = cookielib.LWPCookieJar('cookies')
try:
    cookies.load(ignore_discard=True)
except Exception as e:
    Logging.debug(e.message)
    Logging.warning("cookies 加载失败 !!! 请重新运行 'zhihu_login.py'验证登录 !!!")


class ZhihuMainSpider(scrapy.Spider):
    name = "zhihu_main"
    allowed_domains = ["zhihu.com"]

    def start_requests(self):
        url = "https://www.zhihu.com/collection/43268381"
        cookies_dict = requests.utils.dict_from_cookiejar(cookies)
        return [scrapy.Request(url, cookies=cookies_dict)]

    def parse(self, response):

        page_urls = response.selector.xpath('//div[@class="zm-invite-pager"]/span/a/@href').extract()
        page_count = 0
        for url_extention in page_urls:
            page_count = max(page_count, int(url_extention.split('?page=')[-1]))
            url = ''.join((response.url, url_extention))
            Logging.debug('=====================')
            Logging.info(url)
        Logging.info('page_count: %d' % page_count)

        base_url = 'https://www.zhihu.com'
        urls = response.selector.xpath('//a[@class="toggle-expand"]/@href').extract()
        for url in urls:
            if not url.startswith('https://'):
                # 过滤专栏
                url = ''.join((base_url, url))
            Logging.info(url)