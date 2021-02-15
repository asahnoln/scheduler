import argparse
import calendar
import pprint
from typing import Union
from schedule import Schedule


class Processor:

    def __init__(self) -> None:
        self._days = [d.lower() for d in calendar.day_abbr]
        self._people = []

    def parse_args(self) -> argparse.Namespace:
        '''Parse script arguments'''

        parser = argparse.ArgumentParser(
            description='Tool to figure out sum of busy schedules from different people for a week')
        parser.add_argument('db', help='Path to a json file with data')

        self._subparsers = parser.add_subparsers()
        self._add_subparser_list()
        self._add_subparser_show()
        self._add_subparser_delete()
        self._add_subparser_add()

        self._args = parser.parse_args()

        return self._args

    def process(self, people: list) -> Union[list, None]:
        '''Process script arguments'''

        self._people = people
        return self._args.func()

    def _add_subparser_list(self):
        parser_list = self._subparsers.add_parser('list',
                                                  help='Show current list of people in db')
        parser_list.add_argument(
            '-v', '--verbose', help='Verbosity for some of the output commands', action='count', default=0)
        parser_list.set_defaults(func=self._list)

    def _add_subparser_show(self):
        parser_show = self._subparsers.add_parser('show',
                                                  help='Show busy schedule for people')
        parser_show.add_argument(
            'person', help='Show busy schedule for people', nargs='+')
        parser_show.set_defaults(func=self._show)

    def _add_subparser_delete(self):
        parser_delete = self._subparsers.add_parser('delete',
                                                    help='Delete a person from db')
        parser_delete.add_argument(
            'person', help='Person to delete')
        parser_delete.set_defaults(func=self._delete)

    def _add_subparser_add(self):
        parser_add = self._subparsers.add_parser('add',
                                                 help='Add new person or edit an existing one in the db')
        parser_add.add_argument(
            'person', help='Person to add')
        parser_add.set_defaults(func=self._add)

        for key, day in enumerate(self._days):
            parser_add.add_argument(
                f'--{day}', help=f'Busy time range for {calendar.day_name[key]}', nargs=2, action='append', metavar=('FROM', 'TO'))

    def _list(self) -> None:
        '''Show DB'''

        if self._args.verbose >= 1:
            pprint.pprint(self._people)
        elif self._args.verbose == 0:
            [print(person['name']) for person in self._people]

    def _delete(self) -> Union[list, None]:
        '''Delete person from DB'''

        for key, person in enumerate(self._people):
            if person['name'] == self._args.delete:
                del self._people[key]
                print('Deleted')
                return self._people
        else:
            print('Not found')

    def _add(self) -> Union[list, None]:
        '''Add new person or edit existing'''

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

        for key, day in enumerate(self._days):
            mix_schedule = Schedule()
            for name in self._args.person:
                try:
                    person = next(p for p in self._people if p['name'] == name)
                except StopIteration:
                    print(f'Person {name} not found!')
                    break

                try:
                    ranges = person['schedule'][str(key)]
                    if ranges:
                        schedule = Schedule(ranges)
                        mix_schedule += schedule
                except KeyError:
                    print(f'No schedule for {day} of {person["name"]}')

            print(f'{day}\n{mix_schedule}')
