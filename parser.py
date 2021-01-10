from calendar import day_name
from datetime import time
import json
from json.decoder import JSONDecodeError
import sys


class Processor:

    def __init__(self, people=[]) -> None:
        self.people = people

    def print_people(self):
        print('People in the db.json:')
        for person in self.people:
            print(person)

    def input_times(self, schedule: list):
        while True:
            print('\tFrom? (Enter to skip) ', end='')
            fromTime = input()

            if not fromTime:
                break

            fromTime = time.fromisoformat(fromTime)

            toTime = ''
            while not toTime:
                print('\tTo? ', end='')
                toTime = input()
                print()

            toTime = time.fromisoformat(toTime)

            schedule.append({'from': str(fromTime), 'to': str(toTime)})

    def input_schedule(self, person: dict):
        schedule = {}
        for (key, day) in enumerate(day_name):
            print(f'\tSchedule of {person["name"]} for {day}:')
            schedule[key] = []
            self.input_times(schedule[key])
        person['schedule'] = schedule

    def input_people(self, people: list):
        while True:
            print('Person name? (Enter to skip) ', end='')
            name = input()

            if not name:
                break

            person = {'name': name}
            self.input_schedule(person)

            people.append(person)


class Source:
    DB_FILE_PATH = './db.json'

    def load(self) -> list:
        people = []

        # Create the file if does not exist (thus 'append' attribute)
        with open(self.DB_FILE_PATH, 'a+') as fp:
            try:
                # Append attribute - end of file, return caret
                fp.seek(0)
                people = json.load(fp)
            except JSONDecodeError as exc:
                print(exc)
                print(
                    'Format is incorrect. Truncate db file? Y for truncate, n for exit the program. Y/n ', end='')
                answer = input()
                if answer != 'Y':
                    sys.exit()

        return people

    def save(self, people: list):
        with open(self.DB_FILE_PATH, 'w') as fp:
            json.dump(people, fp)
