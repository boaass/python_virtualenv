# -*- coding:utf-8 -*-
# 匹配能够表示 Python 整数的字符串集

import re

data = ('11111111111111', '22222222222+2222222', '333333333.33333')


def match_int_type_number(num):
    # 还要根据系统判断 32位或64位最大最小值，此处暂不做处理
    m = re.match(r'[+-]?\d+$', num)
    if m is not None:
        return m.group()
    else:
        return None

if __name__ == '__main__':
    for d in data:
        m = match_int_type_number(d)
        if m is not None:
            print m


