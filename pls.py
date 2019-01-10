#!/usr/bin/env python3
import os
from itertools import zip_longest
from tabulate import tabulate as tb
from datetime import datetime as dt
from datetime import timedelta
import math

import typing as T


class FSize(object):

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __hash__(self):
        return self.value

    def __str__(self):
        return _convert_size(self.value)


def _split(test, data):
    o1, o2 = [], []
    for i in data:
        if test(i):
            o1.append(i)
        else:
            o2.append(i)
    return o1, o2


def _convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '{}{}'.format(s, size_name[i])


def format_time(t, current_time=dt.now()):
    idate = dt.utcfromtimestamp(t)
    # if idate.year != current_time.year:
    #     return '{:%Y-%m}'.format(idate)
    if idate.month != current_time.month:
        return '{:%m-%d}'.format(idate)
    if idate.day != current_time.day:
        diffdate = idate - current_time
        return '{0.days} {1:%H}'.format(diffdate, idate)
    diffdate = current_time - idate
    return '{0}'.format(diffdate // timedelta(hours=1))
    # return '{0} {1}'.format(idate.day - current_time.hour, current_time.minute - idate.minute)


def generate_line_file(e, stats, current_time=dt.now()):
    return {
        'name': e.name,
        'size': FSize(stats.st_size),
        'access': format_time(stats.st_atime, current_time),
        'modification': format_time(stats.st_mtime, current_time),
    }


def generate_line_dir(e, stats, current_time=dt.now()):
    return {
        'name': e.name,
        'access': format_time(stats.st_atime, current_time),
    }


def zip_file_dirs(line_dict1, line_dict2):
    if len(line_dict1) < len(line_dict2):
        line_dict1, line_dict2 = line_dict2, line_dict1
    output_lines = []
    for f, d in zip_longest(line_dict1, line_dict2, fillvalue={}):
        ol = list(f.values())
        ol.extend(list(d.values()))
        output_lines.append(ol)
    return output_lines


def _sort_files(line_list):
    return sorted(line_list, key=lambda l: l['size'], reverse=True)


def _sort_dirs(line_list):
    return sorted(line_list, key=lambda l: l['name'])


def _test_dot(line):
    return line['name'].startswith('.')


def _test_backup(line):
    return line['name'].endswith('~')


def _test_underscore(line):
    return line['name'].startswith('_')


def _test_files(line):
    return not any([_test_backup(line), _test_dot(line)])


def _test_dirs(line):
    return not any([_test_dot(line), _test_underscore(line)])


DATA = {
    'files': {
        'add': generate_line_file,
        'lines': [],
        'regular': {
            'test': _test_files,
            'lines': [],
            'sort': _sort_files,
        },
        'other': {
            'lines': [],
            'sort': _sort_files,
        },
    },
    'dirs': {
        'add': generate_line_dir,
        'lines': [],
        'regular': {
            'test': _test_dirs,
            'lines': [],
            'sort': _sort_dirs,
        },
        'other': {
            'lines': [],
            'sort': _sort_dirs,
        },
    },
}


def fill_entries(e, stats, current_time=dt.now()):
    if (e.is_file()):
        DATA['files']['lines'].append(DATA['files']['add'](e, stats,
                                                           current_time))
    else:
        DATA['dirs']['lines'].append(DATA['dirs']['add'](e, stats,
                                                         current_time))


def main():
    current_time = dt.now()
    with os.scandir('.') as osscandir:
        for e in osscandir:
            stats = e.stat()
            fill_entries(e, stats, current_time)
    for x in DATA:
        DATA[x]['regular']['lines'], DATA[x]['other']['lines'] = _split(
            DATA[x]['regular']['test'], DATA[x]['lines'])
        DATA[x]['regular']['lines'] = DATA[x]['regular']['sort'](
            DATA[x]['regular']['lines'])

        # DATA[x]['regular']['lines'] = DATA[x]['regular']['sort'](filter(
        #     DATA[x]['regular']['test'], DATA[x]['lines']))
    # LINES['regular_files'] = _sort(filter(_test_files, LINES['regular_files']))

    # LINES['regular_files'] = sorted(
    #     filter(_test_all, LINES['regular_files']),
    #     key=lambda l: l['size'],
    #     reverse=True)
    # LINES['regular_files'] = sorted(
    #     LINES['regular_files'], key=lambda l: l['size'], reverse=True)
    # print(
    #     tb(
    #         zip_file_dirs(DATA['files']['other']['lines'],
    #                       DATA['dirs']['other']['lines'])))
    print(tb(zip_file_dirs(*[DATA[i]['other']['lines'] for i in DATA])))
    print(tb(zip_file_dirs(*[DATA[i]['regular']['lines'] for i in DATA])))


if __name__ == "__main__":
    main()