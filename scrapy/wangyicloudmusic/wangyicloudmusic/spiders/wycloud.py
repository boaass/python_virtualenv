# -*- coding: utf-8 -*-
import scrapy
import base64
import json


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crypto.Cipher import AES


first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

class WycloudSpider(CrawlSpider):
    name = 'wycloud'
    allowed_domains = ['music.163.com']
    # start_urls = ['http://music.163.com/#/user/home?id=50075694']

    rules = (
        Rule(LinkExtractor(allow=('/song?id=\d+')), callback='parse_item', process_links='process_links', follow=True),
    )
    # print 'params: %s' % get_params()
    # print 'encSecKey: %s' % get_encSecKey()

    def start_requests(self):
        return [scrapy.FormRequest("http://music.163.com/weapi/user/playlist?csrf_token=",
                                   formdata={'params': 'R/tP8kyAGyzKBFmmpEmxRCW7eAyGhxzCyHa8glo3JJc6VOeFxOLQPQTFsrO4ZUEvJUf3W3PAQB1Uc6zrSN9zO5eHRIJJb+G1/l1KNzJ7BnCYBguHqBtvRt+r48k20fa9TVkbsNW0jgtLtAqxwjvyhGfIAZVPbTr5QnZyn/wK77TnjYpQ2CwZl6FskaOwreqE',
                                                                                             'encSecKey': '0dbe4bd5d6ea4e4174e4e516ed1815ede752b1e5c545b1c0aa05a1d70eb1d483e0d26f0980f01ed8ea4502f9c790ecaa5273b5be96110de3db769226e0e6482c910fdbcda5a7b958f93208be67af0f2a503b4bc3fa1e0af0a309fd8dc54990e6b52d37a4555b816b747ca643c11301a8b6c997366c7aabe3ef0c2747882b47a7'},
                                   callback=self.parse_playlist)]

    def parse_playlist(self, response):
        # print '================url: %s' % response.url
        # print 'status: %d' % response.status
        # print 'body: %s' % response.body

        json_data = json.loads(response.body)

        for music_info in json_data['playlist']:
            name = music_info['name']
            id = music_info['id']
            url = 'http://music.163.com/playlist?id=%s' % id
            # print url + '   ' + name.encode('utf-8')
            yield self.make_requests_from_url(url)


    def parse_item(self, response):
        print '========================'
        print response.body
        i = {}



        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
