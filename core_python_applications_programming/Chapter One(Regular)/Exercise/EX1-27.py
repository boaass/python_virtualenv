# -*- coding:utf-8 -*-
# 从时间戳中提取月、日和年，然后以"月，日，年"的格式，每一行仅仅迭代一次

import re


with open('redata.txt', 'r') as f:
    patt = re.compile(r'^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1,2}(\d{1,2})\s\d{2}:\d{2}:\d{2}\s(\d{4})')
    for line_data in f:
        m = re.sub(patt, r'\1, \2, \3', line_data)
        if m is not None:
            print m

f.close()