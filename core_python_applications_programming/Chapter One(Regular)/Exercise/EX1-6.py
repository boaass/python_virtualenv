# -*- coding:utf-8 -*-
# 匹配Web域名

import re

data = ('www://www.yahoo.com/', 'http://www.foothill.edu', 'https://www.baidu.com')


def match_web_domain(domain_name):
    m = re.match(r'^(www|http|https)://[\w+\.]+(edu|org|com|cn|net)/*$', domain_name)
    if m is not None:
        return m.group()
    else:
        return None

if __name__ == '__main__':
    for d in data:
        m = match_web_domain(d)
        if m is not None:
            print m