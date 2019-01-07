#!/usr/bin/env python
import argparse
import sys
import typing

import matplotlib.pyplot as plt
import yaml

from .event import Event, Day
from . import schedule
from . import errors

HOURS_START = 7
HOURS_END = 23
HOURS_TICK_INTERVAL = 2
HOURS_RANGE = range(HOURS_START, HOURS_END + HOURS_TICK_INTERVAL, HOURS_TICK_INTERVAL)
DPI = 100
TITLE = 'Schedule'

DAYS = [d.name for d in Day if d is not Day.UNKNOWN]

DAY_OFFSET = 0.52

def plot_event(ax, event: Event):
    for event_day in event.days:
        day = event_day.value + DAY_OFFSET

        start = event.start.hour + event.start.minute / 60
        end = event.end.hour + event.end.minute / 60

        ax.fill_between([day, day + 0.96], [start, start], [end, end], color=event.color)
        ax.text(day + 0.02, start + 0.02, event.start.strftime("%H:%M"), va='top', fontsize=9)
        ax.text(day + 0.48, (start + end) * 0.503, event.name, ha='center', va='center', fontsize=10)

def draw(event_files: typing.List[str], title: str) -> None:
    fig, ax = plt.subplots(figsize=(18, 9))
    ax.set_title(TITLE, y=1, fontsize=14)

    ax.set_xlim(0.5, len(DAYS) + 0.5)
    ax.set_xticks(range(1, len(DAYS) + 1))
    ax.set_xticklabels(DAYS)
    ax.set_ylim(HOURS_END, HOURS_START)
    ax.set_yticks(HOURS_RANGE)
    ax.set_yticklabels(["{0}:00".format(h) for h in HOURS_RANGE])
    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    for filename in event_files:
        with open(filename, 'r') as fp:
            content = fp.read()

        config = yaml.safe_load(content)
        try:
            if isinstance(config, str):
                events = schedule.load_txt(content)
            elif isinstance(config, list):
                events = schedule.load_yaml(config)
            elif isinstance(config, dict):
                events = schedule.load_yaml([config])
            else:
                print("ERROR: Could not parse input file")

            for e in events:
                plot_event(ax, e)
        except errors.WeekplotError as e:
            print("ERROR:", str(e), file=sys.stderr)


    fig.savefig(title, dpi=DPI)

def main():
    parser = argparse.ArgumentParser(
        description='Visualize your weekly schedule.'
    )

    parser.add_argument('out', type=str, help='Schedule output', default='%s.png' % TITLE)
    parser.add_argument('events', type=str, nargs='+', help='Event files')

    args = parser.parse_args(sys.argv[1:])

    draw(args.events, args.out)

if __name__ == '__main__':
    main()