# -*- coding:utf-8 -*-
# 从电子邮箱中提取登录名和域名（主域名和高级域名一起提取）

import re

with open('redata.txt', 'r') as f:
    for line_data in f:
        m = re.match(r'.*::(\w{4,8})@(\w+\.\w+)::.*', line_data)
        if m is not None:
            print m.groups()

f.close()