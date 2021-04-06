from __future__ import annotations
from datetime import time
from typing import Union

__all__ = ['BusyRange', 'Schedule']

TimeTuple = tuple[int, int]
Time = Union[str, time]


def get_time_tuple(t: time) -> TimeTuple:
    '''Convert time object to tuple (int, int)

    >>> get_time_tuple(time(hour=12, minute=30))
    (12, 30)
    '''
    return (t.hour, t.minute)


def convert_str_to_time(t: Time) -> time:
    '''Convert possible string to time object

    >>> convert_str_to_time('09:00')
    datetime.time(9, 0)

    >>> convert_str_to_time(time(hour=9, minute=0))
    datetime.time(9, 0)
    '''
    return t if isinstance(t, time) else time.fromisoformat(t)


class BusyRange:
    '''Data for busy time range.

    from_time - range start
    to_time - range end

    >>> BusyRange('09:00', '12:00')
    BusyRange(datetime.time(9, 0), datetime.time(12, 0))

    >>> BusyRange(time(hour=11, minute=30), time(hour=15, minute=45))
    BusyRange(datetime.time(11, 30), datetime.time(15, 45))
    '''

    def __init__(self, from_time: Time, to_time: Time) -> None:
        self.from_time = convert_str_to_time(from_time)
        self.to_time = to_time if isinstance(
            to_time, time) else time.fromisoformat(to_time)

    def __repr__(self) -> str:
        return f'BusyRange({self.from_time!r}, {self.to_time!r})'

    def get_from_time_tuple(self) -> TimeTuple:
        '''Get starting time in a tuple format (int, int)

        >>> BusyRange('09:00', '12:00').get_from_time_tuple()
        (9, 0)
        '''

        return get_time_tuple(self.from_time)

    def get_to_time_tuple(self) -> TimeTuple:
        '''Get starting time in a tuple format (int, int)

        >>> BusyRange('09:00', '12:00').get_to_time_tuple()
        (12, 0)
        '''

        return get_time_tuple(self.to_time)


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

    Range = Union[BusyRange, tuple[Time, Time]]
    RangeList = list[Range]

    def __init__(self, ranges: RangeList = None) -> None:
        if not ranges:
            ranges = []
        self._ranges = convert_ranges(ranges)

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

    def _get_all_minutes(self) -> list[TimeTuple]:
        minutes = []
        for busy_range in self._ranges:
            start = busy_range.get_from_time_tuple()
            end = busy_range.get_to_time_tuple()

            for h in range(start[0], end[0] + 1):
                for m in range(0, 60):
                    if h == start[0] and m < start[1]:
                        continue
                    if h == end[0] and m > end[1]:
                        break

                    minutes.append((h, m))
        return minutes


def convert_ranges(ranges: Schedule.RangeList) -> list[BusyRange]:
    '''Convert list of possible time tuples to list of Busy Ranges

    >>> convert_ranges([('09:00', '12:00'), ('13:00', '15:00')])
    [BusyRange(datetime.time(9, 0), datetime.time(12, 0)), BusyRange(datetime.time(13, 0), datetime.time(15, 0))]
    '''

    converted_ranges = []
    for busy_range in ranges:
        if not isinstance(busy_range, BusyRange):
            busy_range = BusyRange(*busy_range)
        converted_ranges.append(busy_range)
    return converted_ranges
