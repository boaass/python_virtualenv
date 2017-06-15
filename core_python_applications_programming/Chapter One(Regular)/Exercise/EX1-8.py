# -*- coding:utf-8 -*-
# 匹配能够表示 Python 长整数的字符串集

import re

data = ('123456789123456789L', '987654321987654321L', '66672L3567', '999999999L999999999L')

def match_long_int_number(num):
    m = re.match(r'[-+]?\d+L$', num)
    if m is not None:
        return m.group()
    else:
        return None

if __name__ == '__main__':
    for d in data:
        m = match_long_int_number(d)
        if m is not None:
            print m