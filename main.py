#!python3.9

import locale
locale.setlocale(locale.LC_ALL, '')

import json
from datetime import date, time
from calendar import LocaleTextCalendar, Calendar, day_name


for d in enumerate(day_name):
    print(d)

# cal = LocaleTextCalendar()
# 
# today = date.today()
# cal.prmonth(today.year, today.month);
# 
# print('Enter first time: ')
# startTime1 = time.fromisoformat(input())
# 
# print('Enter second time: ')
# startTime2 = time.fromisoformat(input())
# 
# print(f'{startTime1} > {startTime2}: {startTime1 > startTime2}')
# print(f'{startTime1} < {startTime2}: {startTime1 < startTime2}')
# print(f'{startTime1} = {startTime2}: {startTime1 == startTime2}')
