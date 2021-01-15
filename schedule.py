from __future__ import annotations
from datetime import time
from typing import Union


class BusyRange:
    '''Data for busy time range.

    from_time - range start
    to_time - range end
    '''
    TimeType = Union[str, time]

    def __init__(self, from_time: TimeType, to_time: TimeType) -> None:
        self.from_time = from_time if isinstance(
            from_time, time) else time.fromisoformat(from_time)
        self.to_time = to_time if isinstance(
            to_time, time) else time.fromisoformat(to_time)

    def __repr__(self) -> str:
        # TODO: Use repr str instead of repr?
        return f'BusyRange({self.from_time!r}, {self.to_time!r})'


class Schedule:
    '''Data for storing and manipulating several busy time ranges.
    '''
    Range = Union[BusyRange, tuple[BusyRange.TimeType, BusyRange.TimeType]]
    RangeList = list[Range]

    def __init__(self, ranges: RangeList = None) -> None:
        if not ranges:
            ranges = []
        self._ranges = self._convert_ranges(ranges)

    def __str__(self) -> str:
        text = ''
        for busy_range in self._ranges:
            text += f'{busy_range.from_time} — {busy_range.to_time}\n'

        return text

    def __repr__(self) -> str:
        return f'Schedule({self._ranges!r})'

    def __add__(self, schedule: Schedule) -> Schedule:
        return self.add(schedule)

    def append(self, busy_range: Range) -> None:
        '''Append busy range to current range list.'''

        if not isinstance(busy_range, BusyRange):
            busy_range = BusyRange(*busy_range)

        self._ranges.append(busy_range)

    def add(self, schedule: Schedule) -> Schedule:
        '''Produce a new schedule by adding another schedule to current schedule.'''

        all_ranges = self._ranges.copy()
        all_ranges.extend(schedule._ranges)
        all_ranges.sort(key=lambda busy_range: busy_range.from_time)

        # Linear search for crossings of time ranges
        new_ranges = []
        new_from_time = None
        for key, busy_range in enumerate(all_ranges):
            if not new_from_time:
                new_from_time = busy_range.from_time

            if key == len(all_ranges) - 1 or busy_range.to_time < all_ranges[key + 1].from_time:
                new_ranges.append(BusyRange(new_from_time, busy_range.to_time))
                new_from_time = None

        return Schedule(new_ranges)

    def _convert_ranges(self, ranges: RangeList) -> list[BusyRange]:
        converted_ranges = []
        for busy_range in ranges:
            if not isinstance(busy_range, BusyRange):
                busy_range = BusyRange(*busy_range)
            converted_ranges.append(busy_range)
        return converted_ranges

