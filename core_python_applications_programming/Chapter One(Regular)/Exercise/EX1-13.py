# -*- coding:utf-8 -*-
# 从 type(value) 返回的字符串中提取类型

import re


def method():
    return None

data = (str(type(0)), str(type(1.1)), str(type('haha')), str(type(method)))


def match_type(type_str):
    m = re.match(r'^<type\s\'(\w+)\'>$', type_str)
    if m is not None:
        return m.group(1)
    else:
        return None


if __name__ == '__main__':
    for d in data:
        m = match_type(d)
        if m is not None:
            print m