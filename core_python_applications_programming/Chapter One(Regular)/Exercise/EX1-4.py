# -*- coding:utf-8 -*-
# 1-4 匹配所有有效Python标识符的集合（英文/数字/下划线）

import re

data = ('data', '0python', 'regular_', '__regular_test')
result = []

for d in data:
    m = re.match(r'\b[a-zA-Z_](\w|_)*\b', d)
    if m is not None:
        result.append(m.group())

for r in result:
    print r