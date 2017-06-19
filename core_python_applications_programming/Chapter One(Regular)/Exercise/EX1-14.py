# -*- coding:utf-8 -*-
# 处理日期，表示10/11/12月份

import re

data = ('10', '11', '12')


def match_month(month):
    m = re.match(r'1[0-2]', month)
    if m is not None:
        return m.group()
    else:
        return None


if __name__ == '__main__':
    for d in data:
        m = match_month(d)
        if m is not None:
            print m