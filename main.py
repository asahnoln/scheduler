#!python3.9

import json
from datetime import date, time
from calendar import LocaleTextCalendar, Calendar, day_name
from json.decoder import JSONDecodeError
import locale
import sys

locale.setlocale(locale.LC_ALL, '')


def print_people(people: list):
    print('People in the db.json:')
    for person in people:
        print(person)


def input_people(people: list):
    while True:
        print('Person name? (Enter to skip)', end='')
        name = input()

        if not name:
            break

        people.append({'name': name})


DB_FILE_PATH = './db.json'
people = []

# Create the file if does not exist (thus 'append' attribute)
with open(DB_FILE_PATH, 'a+') as fp:
    try:
        # Append attribute - end of file, return caret
        fp.seek(0)
        people = json.load(fp)
    except JSONDecodeError as exc:
        print(exc)
        print('Format is incorrect. Truncate db file? Y for truncate, n for exit the program. Y/n ', end='')
        answer = input()
        if answer != 'Y':
            sys.exit()

print_people(people)
print()
input_people(people)

print(people)

with open(DB_FILE_PATH, 'w') as fp:
    json.dump(people, fp)

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
