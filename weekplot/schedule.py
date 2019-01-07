import typing
import datetime

from .event import Event, Day
from .errors import WeekplotError

class ScheduleParseError(WeekplotError):
    pass


def _get_day(prefix):
    day = Day.from_prefix(prefix)
    if day is Day.UNKNOWN:
        raise ScheduleParseError("Invalid day: {0}".format(prefix))
    return day

def _parse_events(lines) -> typing.Iterator[Event]:
    index = 0
    name, days, start, end, color = None, None, None, None, None
    for line in lines:
        line = line.rstrip()
        index += 1
        if index == 1:
            name = line
        elif index == 2:
            days = [_get_day(d) for d in line.replace(' ', '').split(',')]
        elif index == 3:
            hours = line.replace(' ', '').split('-')
            start = datetime.datetime.strptime(hours[0], '%H:%M').time()
            end = datetime.datetime.strptime(hours[1], '%H:%M').time()
        elif index == 4:
            color = line
        elif index == 5 and line == '':
            yield Event(
                name=name, 
                days=days, 
                start=start,
                end=end,
                color=color
            )
            index = 0
        else:
            raise ScheduleParseError("Corrupted input file.")


def load_txt(schedule: str) -> typing.Iterator[Event]:
    return _parse_events(schedule.split('\n'))


def load_yaml(schedule: typing.List) -> typing.Iterator[Event]:
    for event in schedule:
        yield Event.from_dict(event)