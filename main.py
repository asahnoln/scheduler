#!/usr/bin/python3.9

from loader import Source
import locale
import argparse
import datetime
import calendar
import pprint

#locale.setlocale(locale.LC_ALL, '')
# TODO: Possible bug - I want days in english, what happens if I don't set locale?

parser = argparse.ArgumentParser(description='Tool to figure out sum of busy schedules from different people for a week')

parser.add_argument('db', help='Path to a json file with data')
parser.add_argument('-l', '--list', help='Show current list of people in db', action='store_true')

parser.add_argument('-s', '--show', help='Show busy schedule for people', nargs='+', metavar='NAME')

time_group = parser.add_argument_group('time editing')
time_group.add_argument('-p', '--person', help='Add new person or edit an existing one in the db')

for key, day in enumerate(calendar.day_abbr):
    time_group.add_argument(f'--{day.lower()}', help=f'Busy time range for {calendar.day_name[key]}', nargs=2, action='append', metavar=('FROM', 'TO'))

args = parser.parse_args()

source = Source(args.db)
data = source.load()

if args.list:
    pprint.pprint(data)

print(args)
