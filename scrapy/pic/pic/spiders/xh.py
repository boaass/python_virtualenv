# -*- coding: utf-8 -*-
import scrapy

from pic.items import PicItem

class XhSpider(scrapy.Spider):
    name = "xh"
    allowed_domains = ["xiaohuar.com"]
    start_urls = ['http://www.xiaohuar.com/hua/']

    url_set = set()

    def parse(self, response):
        if not response.url.startswith("http://www.xiaohuar.com/list-"):
            print '------------------------------'
            print response.xpath("//a/@href").extract()
            urls = response.xpath("//a/@href").extract()
            print urls
            for url in urls:
                if url.startswith("http://www.xiaohuar.com/list-"):
                    if url in XhSpider.url_set:
                        pass
                    else:

                        XhSpider.url_set.add(url)

                        yield self.make_requests_from_url(url)
                else:
                    pass
        else:
            allPics = response.xpath('//div[@class="img"]/a')
            for pic in allPics:
                item = PicItem()
                name = pic.xpath('./img/@alt').extract()[0]
                addr = pic.xpath('./img/@src').extract()[0]
                addr = 'http://www.xiaohuar.com' + addr
                item['name'] = name
                item['addr'] = addr

                yield item

