# -*- coding:utf-8 -*-
# 支持使用圆括号或者连接字符连接的区号

import re

data = ('800-555-1212', '555-1212', '(800)555-1212')


def match_phone_number(num):
    m = re.match(r'((?:\d{3}-)|(?:\(\d{3}\)))?\d{3}-\d{4}', num)
    if m is not None:
        print m.group()


if __name__ == '__main__':
    for d in data:
        match_phone_number(d)