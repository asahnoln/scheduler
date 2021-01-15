#!/usr/bin/python3.9

from loader import Source
import locale
import argparse
import datetime
import calendar
import pprint

#locale.setlocale(locale.LC_ALL, '')
# TODO: Possible bug - I want days in english, what happens if I don't set locale?

days = tuple([d.lower() for d in calendar.day_abbr])

parser = argparse.ArgumentParser(description='Tool to figure out sum of busy schedules from different people for a week')

parser.add_argument('db', help='Path to a json file with data')
parser.add_argument('-l', '--list', help='Show current list of people in db', action='store_true')

parser.add_argument('-s', '--show', help='Show busy schedule for people', nargs='+', metavar='NAME')

exclusive_group = parser.add_mutually_exclusive_group()

exclusive_group.add_argument('-d', '--delete', help='Delete a person from db')
exclusive_group.add_argument('-p', '--person', help='Add new person or edit an existing one in the db')

time_group = parser.add_argument_group('time editing')
for key, day in enumerate(days):
    time_group.add_argument(f'--{day}', help=f'Busy time range for {calendar.day_name[key]}', nargs=2, action='append', metavar=('FROM', 'TO'))

args = parser.parse_args()

source = Source(args.db)
people = source.load()

if args.list:
    pprint.pprint(people)

if args.delete:
    for key, person in enumerate(people):
        if person['name'] == args.delete:
            del people[key]
            source.save(people)
            print('Deleted!')
            break
    else:
        print('Not found')


if args.person:
    new_person = {'name': args.person, 'schedule': {}}
    for key, day in enumerate(days):
        try:
            new_person['schedule'][key] = getattr(args, day)
        except AttributeError:
            continue

    for key, person in enumerate(people):
        if person['name'] == new_person['name']:
            people[key] = new_person
            break
    else:
        people.append(new_person)


    source.save(people)
    pprint.pprint(people)
    print('Saved!')


