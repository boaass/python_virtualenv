# -*- coding:utf-8 -*-
# 提取完整时间戳


import re

with open('redata.txt', 'r') as f:
    for line_data in f:
        print line_data.split('::')[0]

f.close()