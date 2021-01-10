#!python3.9

import locale
from datetime import date, time
from calendar import LocaleTextCalendar, Calendar, day_name
from parser import Source
from schedule import BusyRange, Schedule
import pprint

locale.setlocale(locale.LC_ALL, '')

#source = Source()
#people = source.load()
#print(people)
#source.save(people)

schedule = Schedule()
schedule.append(BusyRange('09:00', '13:00'))
schedule.append(BusyRange('18:00', '20:00'))

schedule2 = Schedule()
schedule2.append(BusyRange('11:00', '16:00'))
schedule2.append(BusyRange('20:00', '21:00'))
schedule2.append(BusyRange('22:00', '23:00'))

print(schedule)
print(schedule2)
print(schedule.add(schedule2))

print(repr(schedule))

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
