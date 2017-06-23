# -*- coding:utf-8 -*-
# 1-2 匹配由单个空格分隔的任意单词对， 也就是姓和名

import re

data = ('Xiao Ming', 'Xiao Z-Hong', 'Li Xiang', 'Song Qianqian', 'WangQiuYang', '-Wu -Ge')

result = []
for d in data:
    m = re.match(r'[A-Za-z-]+\s[A-Za-z-]+', d)
    if m is not None:
        result.append(m.group())

for r in result:
    print r

