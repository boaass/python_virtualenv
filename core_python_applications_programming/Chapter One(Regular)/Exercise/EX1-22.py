# -*- coding:utf-8 -*-
# 提取时间戳中的年份


with open('redata.txt', 'r') as f:
    for line_data in f:
        time = line_data.split('::')[0]
        print time.split(' ')[-1]

f.close()