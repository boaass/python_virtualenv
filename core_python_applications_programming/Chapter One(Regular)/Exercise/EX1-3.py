# -*- coding:utf-8 -*-
# 1-3 匹配由单个逗号和单个空白符分割的任何单词和单个字母， 如姓氏的首字母

import re

data = ('Ming, X', 'Z-Hong, X', 'Xiang Li', 'Qianqian, S')

result = []
for d in data:
    m = re.match(r'[A-Za-z-]+,\s[A-Za-z]', d)
    if m is not None:
        result.append(m.group())

for r in result:
    print r