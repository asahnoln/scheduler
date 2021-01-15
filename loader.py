import json
import sys
from json.decoder import JSONDecodeError

class Source:
    def __init__(self, path: str) -> None:
        self._path = path

    def load(self) -> list[dict]:
        people = []

        # Create the file if does not exist (thus 'append' attribute)
        with open(self._path, 'a+') as fp:
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
        with open(self._path, 'w') as fp:
            json.dump(people, fp)
