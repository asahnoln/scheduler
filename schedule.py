from __future__ import annotations
from datetime import time
from typing import Union


class BusyRange:
    '''Data for busy time range.

    from_time - range start
    to_time - range end

    >>> BusyRange('09:00', '12:00')
    BusyRange(datetime.time(9, 0), datetime.time(12, 0))
    '''

    Time = Union[str, time]

    def __init__(self, from_time: Time, to_time: Time) -> None:
        self.from_time = from_time if isinstance(
            from_time, time) else time.fromisoformat(from_time)
        self.to_time = to_time if isinstance(
            to_time, time) else time.fromisoformat(to_time)

    def __repr__(self) -> str:
        # TODO: Use repr str instead of repr?
        return f'BusyRange({self.from_time!r}, {self.to_time!r})'


class Schedule:
    '''Data for storing and manipulating several busy time ranges.

    Pass a list of tuples with time ranges:
    >>> Schedule([('09:00', '12:00'), ('14:00', '16:00')])
    Schedule([BusyRange(datetime.time(9, 0), datetime.time(12, 0)), BusyRange(datetime.time(14, 0), datetime.time(16, 0))])

    Summation of schedules results in a new schedule with all ranges:
    >>> Schedule([('09:00', '15:00'), ('14:00', '16:00')]) + Schedule([('18:00', '20:00')])
    Schedule([BusyRange(datetime.time(9, 0), datetime.time(16, 0)), BusyRange(datetime.time(18, 0), datetime.time(20, 0))])

    If time ranges overlap, a new time range created with the lowest and highest time signatures from overlapping ranges (note the second schedule)
    >>> Schedule([('09:00', '15:00'), ('14:00', '16:00')]) + Schedule([('11:00', '17:00')])
    Schedule([BusyRange(datetime.time(9, 0), datetime.time(17, 0))])
    '''

    Range = Union[BusyRange, tuple[BusyRange.Time, BusyRange.Time]]
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
        '''Append busy range to current range list.

        >>> schedule = Schedule([('09:00', '14:00')])
        >>> schedule
        Schedule([BusyRange(datetime.time(9, 0), datetime.time(14, 0))])
        >>> schedule.append(('16:00', '18:00'))
        >>> schedule
        Schedule([BusyRange(datetime.time(9, 0), datetime.time(14, 0)), BusyRange(datetime.time(16, 0), datetime.time(18, 0))])
        '''

        if not isinstance(busy_range, BusyRange):
            busy_range = BusyRange(*busy_range)

        self._ranges.append(busy_range)

    # New method from packing minutes
    def add(self, schedule: Schedule) -> Schedule:
        '''Produce a new schedule by adding another schedule to current schedule.

        Summation of schedules results in a new schedule with all ranges:
        >>> Schedule([('09:00', '15:00'), ('14:00', '16:00')]).add(Schedule([('18:00', '20:00')]))
        Schedule([BusyRange(datetime.time(9, 0), datetime.time(16, 0)), BusyRange(datetime.time(18, 0), datetime.time(20, 0))])

        If time ranges overlap, a new time range created as the mix of overlapping ranges (note the second schedule)
        >>> Schedule([('09:00', '15:00'), ('14:00', '16:00')]).add(Schedule([('11:00', '17:00')]))
        Schedule([BusyRange(datetime.time(9, 0), datetime.time(17, 0))])
        '''

        all_minutes = sorted(
            set(self._get_all_minutes() + schedule._get_all_minutes()))
        new_schedule = Schedule()

        start = None
        end = None
        for h, m in all_minutes:
            if not start:
                start = (h, m)
                continue

            if end and ((m - end[1]) % 60 > 1 or (h - end[0]) > 1):
                new_schedule.append((time(*start), time(*end)))
                start = (h, m)

            end = (h, m)

        if start and end:
            new_schedule.append((time(*start), time(*end)))

        return new_schedule

    def _get_all_minutes(self) -> list[tuple[int, int]]:
        minutes = []
        for busy_range in self._ranges:
            start = [int(x) for x in str(busy_range.from_time).split(':')]
            end = [int(x) for x in str(busy_range.to_time).split(':')]

            for h in range(start[0], end[0] + 1):
                for m in range(0, 60):
                    if h == start[0] and m < start[1]:
                        continue
                    if h == end[0] and m > end[1]:
                        break

                    minutes.append((h, m))
        return minutes

    @staticmethod
    def _convert_ranges(ranges: RangeList) -> list[BusyRange]:
        converted_ranges = []
        for busy_range in ranges:
            if not isinstance(busy_range, BusyRange):
                busy_range = BusyRange(*busy_range)
            converted_ranges.append(busy_range)
        return converted_ranges
