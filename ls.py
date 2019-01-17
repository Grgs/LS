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
    # section_seperator = ('-' * os.get_terminal_size().columns)
    # str_seperator = ('\n' + '-' * 60 + '\n')
    # print(
    #     str_seperator.join(
    #         filter(lambda x: x != '',
    #                map(str, [
    #                    dirs.backup,
    #                    files.backup,
    #                    dirs.other,
    #                    dirs.regular,
    #                    files.other,
    #                    files.regular,
    #                ]))))

    # singles, doubles, last_singles = _pack_entries(
    #         map(lambda x: x.get_lines(), files.output()),
    #         map(lambda x: x.get_lines(), dirs.output()))
    # print('\n'.join(map(str, singles)))
    # print(section_seperator)
    # for i in doubles:
    #     print(' '.join(map(str, i)))

    # print('\n'.join(map(str, last_singles)))

    print('\n'.join(
        list([
            ' | '.join(l) for l in zip_longest(
                chain.from_iterable(
                    map(lambda x: x.get_lines(), files.output())),
                chain.from_iterable(
                    map(lambda x: x.get_lines(), dirs.output())),
                fillvalue=' ' * 50)
        ])))

    # print('\n'.join(
    #     map(_entry_join,
    #         zip_longest(
    #             chain(*map(lambda x: x.get_lines(), [
    #                 files.backup,
    #                 files.other,
    #                 files.regular,
    #             ])),
    #             chain(*map(lambda x: x.get_lines(), [
    #                 dirs.backup,
    #                 dirs.other,
    #                 dirs.regular,
    #             ]))))))

    # print('\n'.join(
    #     map(_entry_join,
    #         zip_longest(files.other.get_lines(), dirs.regular.get_lines()))))


if __name__ == "__main__":
    # profile.run("main()")
    main()
