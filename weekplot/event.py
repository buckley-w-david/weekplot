from collections import namedtuple
import datetime
from enum import Enum
import typing


class Day(Enum):
    UNKNOWN = -1
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def from_prefix(prefix: str) -> 'Day':
        up = prefix.upper()
        for d in Day:
            if d.name.startswith(up):
                return d
        return Day.UNKNOWN


class Event(typing.NamedTuple):
    name: str
    days: typing.List[Day]
    start: datetime.time
    end: datetime.time
    color: str

    @staticmethod
    def from_dict(d) -> 'Event':
        start = datetime.datetime.strptime(d['start'], '%H:%M').time()
        end = datetime.datetime.strptime(d['end'], '%H:%M').time()
        return Event(
            name=d['name'],
            days=[Day.from_prefix(day) for day in d['days']],
            start=start,
            end=end,
            color=d['color'],
        )
