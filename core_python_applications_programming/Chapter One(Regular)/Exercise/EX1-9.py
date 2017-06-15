# -*- coding:utf-8 -*-
# 匹配能够表示 Python 浮点数的字符串集

import re

data = ('245123.4', '532.1232', '424fs4.3235', '44252.4512L')


def match_float_number(num):
    m = re.match(r'[+-]?\d+\.\d+$', num)
    if m is not None:
        return m.group()
    else:
        return None

if __name__ == '__main__':
    for d in data:
        m = match_float_number(d)
        if m is not None:
            print m