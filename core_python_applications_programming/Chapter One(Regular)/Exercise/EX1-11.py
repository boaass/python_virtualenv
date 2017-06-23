# -*- coding:utf-8 -*-
# 匹配电子邮件地址

import re

data = ('boaass@sina.com', 'boaass@qq.com', '476532462@qq.com')


def match_email(email):
    m = re.match(r'\w+@\w+\.\w+', email)
    if m is not None:
        return m.group()
    else:
        return None


if __name__ == '__main__':
    for d in data:
        m = match_email(d)
        if m is not None:
            print m
