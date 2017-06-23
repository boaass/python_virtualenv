# -*- coding:utf-8 -*-
# 1-1 识别后续的字符串: "bat"、"bit"、"but"、"hat"、"hit"、或者"hut".

import re

data = ('bat', 'bit', 'but', 'hat', 'hit', 'hut')

result = []
for d in data:
    m = re.match(r'[bh][aiu]t', d)
    if m is not None:
        result.append(m.group())

for r in result:
    print r

