# -*- coding:utf-8 -*-
# 匹配能够表示 Python 复数的字符串集

import re

data = ('4+5j', '6j', '5432+jj', '1+j')


def match_complex_number(num):
    m = re.match(r'(\d+\+)?\d*j$', num)
    if m is not None:
        return m.group()
    else:
        return None


if __name__ == '__main__':
    for d in data:
        m = match_complex_number(d)
        if m is not None:
            print m
