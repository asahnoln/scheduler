#!/usr/bin/python3.9

from loader import Source
from processor import Processor

#locale.setlocale(locale.LC_ALL, '')
# TODO: Possible bug - I want days in english, what happens if I don't set locale?

process = Processor()
args = process.parse_args()

source = Source(args.db)
people = source.load()

new_people = process.process(people)

if new_people:
    source.save(new_people)
