from calendar import day_name
from datetime import time

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
            from_time = input()

            if not from_time:
                break

            from_time = time.fromisoformat(from_time)

            to_time = ''
            while not to_time:
                print('\tTo? ', end='')
                to_time = input()
                print()

            to_time = time.fromisoformat(to_time)

            schedule.append({'from': str(from_time), 'to': str(to_time)})

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

