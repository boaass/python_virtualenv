# -*- coding:utf-8 -*-
# 提取'redata.txt'中的邮箱地址


with open('redata.txt', 'r') as f:
    for line_data in f:
        print line_data.split('::')[1]
