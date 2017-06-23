# -*- coding:utf-8 -*-
# 处理信用卡号码

import re


data = ('1111-1111-1111-1111', '2222-222222-22222', '3f44-5f43g2-33333', '555555555345346', '8882384928412352')


def match_credit_card(num):
    str_no_symbol = num.replace('-', '')
    m = re.match(r'\d{15,16}', str_no_symbol)
    if m is not None:
        if len(str_no_symbol) == 15:
            return '%s-%s-%s' % (str_no_symbol[0:4], str_no_symbol[4:10], str_no_symbol[10:15])
        elif len(str_no_symbol) == 16:
            return '%s-%s-%s-%s' % (str_no_symbol[0:4], str_no_symbol[4:8], str_no_symbol[8:12], str_no_symbol[12:16])
    return None


if __name__ == '__main__':
    for d in data:
        m = match_credit_card(d)
        if m is not None:
            print m