# -*- coding:utf-8 -*-
# 匹配街道地址

import re

data = {'3120 De La Cruz Drive', '1180 Bordeaux Drive'}


def match_street_address(address_name):
    m = re.match(r'(\w+ )*\w*', address_name)
    if m is not None:
        return m.group()
    else:
        return None

if __name__ == '__main__':
    for d in data:
        m = match_street_address(d)
        if m is not None:
            print m