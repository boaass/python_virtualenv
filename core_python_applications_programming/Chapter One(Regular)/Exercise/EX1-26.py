# -*- coding:utf-8 -*-
# 替换每一行的电子邮箱地址

import re


with open('redata.txt', 'r') as f:
    for line_data in f:
        m = re.sub(r'\w+@\w+\.\w+', 'boaass@sina.com', line_data)
        print m

f.close()
