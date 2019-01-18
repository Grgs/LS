#!/usr/bin/env python3
# import profile
import os
import sys
from itertools import zip_longest, chain, islice
from datetime import datetime as dt

from tabulate import tabulate

from FSystem import FDirs, FFiles


def _tabulate_splitline(lines):
    return tabulate(lines, headers="keys", tablefmt='presto').splitlines()


def _zip_tabulate(files, dirs, part: str):
    return tabulate(
        zip_longest(*map(
            _tabulate_splitline,
            [getattr(files, part), getattr(dirs, part)])))


def _fill_empty(line):
    if line is None:
        return ''
    return str(line)


def _entry_join(line):
    return ' | '.join(map(_fill_empty, line))


def _pack_entries(file_lists, dir_lists):
    dir_lists = list(filter(lambda l: l != [], dir_lists))
    file_lists = list(filter(lambda l: l != [], file_lists))
    f_list = list(chain(*file_lists))
    d_index, d_list = 0, []
    for i in dir_lists:
        if len(f_list) > (len(d_list) + len(i)):
            d_list.extend(i)
        else:
            break
        d_index += 1
    singles = chain(*dir_lists[d_index:])
    doubles = zip(f_list, d_list)
    if len(f_list) != len(d_list):
        last_singles = islice(f_list, len(d_list), None)
    else:
        last_singles = []
    return singles, doubles, last_singles


def get_entries(_path: str):
    current_time = dt.now()
    files = FFiles('file', current_time)
    dirs = FDirs('dir', current_time)
    with os.scandir(_path) as osscandir:
        for e in osscandir:
            if e.is_file():
                files.add(e, e.stat())
            else:
                dirs.add(e, e.stat())
    files.complete()
    dirs.complete()
    return files, dirs


def main():
    if len(sys.argv) > 1:
        _path = sys.argv[1]
    else:
        _path = '.'
    files, dirs = get_entries(_path)

    if os.get_terminal_size().columns < 78:
        section_seperator = '\n' + '-' * (
            os.get_terminal_size().columns - 1) + '\n'
        output = dirs.output()
        output.extend(files.output())
        text = section_seperator.join(
            map(lambda x: '\n'.join(x.get_lines()), filter(lambda x: x,
                                                           output)))
    else:
        text = '\n'.join(
            list([
                '{0:<52}|{1}'.format(*l) for l in zip_longest(
                    chain.from_iterable(
                        map(lambda x: x.get_lines(), files.output())),
                    chain.from_iterable(
                        map(lambda x: x.get_lines(), dirs.output())),
                    fillvalue=' ')
            ]))

    print(text)


if __name__ == "__main__":
    # profile.run("main()")
    main()
