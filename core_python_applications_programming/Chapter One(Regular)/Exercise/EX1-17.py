# -*- coding:utf-8 -*-
# 判断'gendata.py'中，一周每一天出现的次数


week_count = dict(Mon=0, Tue=0, Wed=0, Thu=0, Fri=0, Sat=0, Sun=0)

with open('redata.txt', 'r') as f:
    for line in f:
        for week in week_count:
            week_count[week] += line.split().count(week)

f.close()

for week in week_count:
    print('count of %s is %d' % (week, week_count[week]))
