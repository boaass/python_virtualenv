# -*- coding:utf-8 -*-
# 为'gendata.py'更新代码，是数据直接输出到redata.txt而不是屏幕。


from random import randrange, choice
from string import ascii_lowercase as lc
from sys import maxint
from time import ctime

tlds = ('com', 'edu', 'net', 'org', 'gov')
f = open('redata.txt', 'w+')

for i in xrange(randrange(5, 11)):
    dtint = randrange(2**32)
    dtstr = ctime(dtint)
    llen = randrange(4, 8)
    login = ''.join(choice(lc) for j in range(llen))
    dlen = randrange(llen, 13)
    dom = ''.join(choice(lc) for j in xrange(dlen))
    f.write('%s::%s@%s.%s::%d-%d-%d\n' % (dtstr, login, dom, choice(tlds), dtint, llen, dlen))
f.close()



