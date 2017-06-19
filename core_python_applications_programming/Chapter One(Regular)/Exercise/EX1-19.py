# -*- coding:utf-8 -*-
# 提取完整时间戳


import re

with open('redata.txt', 'r') as f:
    for line_data in f:
        m = re.match(
            r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1,2}\d{1,2}\s\d{2}\:\d{2}\:\d{2}\s\d+\d{4}',
            line_data)
        if m is not None:
            print m.group()