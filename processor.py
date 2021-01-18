import argparse
import calendar
import pprint
from typing import Union
from schedule import Schedule


class Processor:

    def __init__(self) -> None:
        self._days = tuple([d.lower() for d in calendar.day_abbr])
        self._people = []

    def parse_args(self) -> argparse.Namespace:
        '''Parse script arguments'''

        parser = argparse.ArgumentParser(
            description='Tool to figure out sum of busy schedules from different people for a week')

        parser.add_argument('db', help='Path to a json file with data')
        parser.add_argument(
            '-l', '--list', help='Show current list of people in db', action='store_true')
        parser.add_argument(
            '-v', '--verbose', help='Verbosity for some of the output commands', action='count', default=0)

        parser.add_argument(
            '-s', '--show', help='Show busy schedule for people', nargs='+', metavar='NAME')

        exclusive_group = parser.add_mutually_exclusive_group()

        exclusive_group.add_argument(
            '-d', '--delete', help='Delete a person from db')
        exclusive_group.add_argument(
            '-p', '--person', help='Add new person or edit an existing one in the db')

        time_group = parser.add_argument_group('time editing')
        for key, day in enumerate(self._days):
            time_group.add_argument(
                f'--{day}', help=f'Busy time range for {calendar.day_name[key]}', nargs=2, action='append', metavar=('FROM', 'TO'))

        self._args = parser.parse_args()

        return self._args

    def process(self, people: list) -> Union[list, None]:
        '''Process script arguments'''

        self._people = people

        commands = ['list', 'show', 'delete', 'add']

        for c in commands:
            people = getattr(self, f'_{c}')()
            if isinstance(people, list):
                return people

    def _list(self) -> None:
        '''Show DB'''

        if self._args.list:
            if self._args.verbose >= 1:
                pprint.pprint(self._people)
            elif self._args.verbose == 0:
                [print(person['name']) for person in self._people]

    def _delete(self) -> Union[list, None]:
        '''Delete person from DB'''

        if self._args.delete:
            for key, person in enumerate(self._people):
                if person['name'] == self._args.delete:
                    del self._people[key]
                    print('Deleted')
                    return self._people
            else:
                print('Not found')

    def _add(self) -> Union[list, None]:
        '''Add new person or edit existing'''

        if self._args.person:
            new_person = {'name': self._args.person, 'schedule': {}}
            for key, day in enumerate(self._days):
                try:
                    new_person['schedule'][key] = getattr(self._args, day)
                except AttributeError:
                    continue

            for key, person in enumerate(self._people):
                if person['name'] == new_person['name']:
                    self._people[key] = new_person
                    break
            else:
                self._people.append(new_person)

            print('Saved!')
            pprint.pprint(self._people)
            return self._people

    def _show(self) -> None:
        '''Show schedule'''

        if self._args.show:
            for key, day in enumerate(self._days):
                mix_schedule = Schedule()
                for person in self._people:
                    if person['name'] not in self._args.show:
                        continue

                    try:
                        ranges = person['schedule'][str(key)]
                        if ranges:
                            schedule = Schedule(ranges)
                            mix_schedule += schedule
                    except KeyError:
                        print(f'No schedule for {day} of {person["name"]}')

                print(f'{day}\n{mix_schedule}')
