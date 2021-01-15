#!python3.9

import locale
from schedule import BusyRange, Schedule

# To check repr 
import datetime

locale.setlocale(locale.LC_ALL, '')

# Append ranges
schedule = Schedule()
schedule.append(BusyRange('09:00', '13:00'))
schedule.append(('18:00', '20:00'))

# Create with ranges and append (check mix of methods)
schedule2 = Schedule([
    BusyRange('11:00', '16:00'),
    ('20:00', '21:00'),
    ])
schedule2.append(('22:00', '23:00'))

# Check __str__
print(schedule)
print(schedule2)

# Use method
print(schedule.add(schedule2))

# Use overloaded operator
print(schedule + schedule2)

# Check __repr__
print(repr(schedule))

schedule_mix = eval(repr(schedule + schedule2))
print(schedule_mix)
