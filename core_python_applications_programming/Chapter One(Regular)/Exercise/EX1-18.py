# -*- coding:utf-8 -*-
# 判断'redata.txt'是否有数据损坏


import re

with open('redata.txt', 'r') as f:
    for line_data in f:
        m = re.match(
            r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}\s\d{2}\:\d{2}\:\d{2}\s\w+',
            line_data)
        if m is not None:
            print 'data integrity!'
        else:
            print 'data corruption!'
