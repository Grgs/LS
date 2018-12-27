#!/usr/bin/env python3
'''display directory files and folders'''
import subprocess
import sys
from itertools import chain, compress, repeat

import regex as re

from guirguis.filter import filter_list

COLOR_STOP = '[0m'


def _map_join(clean_fun, text_list):
    return '\n'.join(map(clean_fun, text_list))


def _regurlar_file_test(line: str) -> bool:
    return line.startswith('-')


def _tmp_file_test(line: str) -> bool:
    return any([line.endswith('~'), line.endswith('~' + COLOR_STOP)])


def _regurlar_dir_test(line: str) -> bool:
    return line.startswith('d')


def _other_file_test(line: str) -> bool:
    return len(line) > 0


def _filter_start(line: str, filter_select):
    return compress(re.split(r'\s+', line, maxsplit=3),
                    chain(filter_select, repeat(1)))


def _clean_dirs(line: str):
    return ' '.join(_filter_start(line, [0, 0, 0, ])) + COLOR_STOP


def _clean_files_in_mnt(line: str) -> str:
    output_0, output_1, output_2 = _filter_start(line, [1, 0, ])
    return '{} {:>6} {}'.format(output_0[1:], output_1,
                                output_2) + COLOR_STOP


def _clean_other_files(line: str) -> str:
    output_0, output_1 = _filter_start(line, [1, 0, 0, ])
    return '{} {}'.format(output_0[0], output_1) + COLOR_STOP


def _clean_files_regular(line: str) -> str:
    output_0, output_1 = _filter_start(line, [0, 0, ])
    return '{:>6} {}'.format(output_0, output_1) + COLOR_STOP


def _clean_files_tmp(line: str) -> str:
    return re.sub(r'\x1b\[0m|\x1b\[01;\d+m', '',
                  _clean_files_regular(line))


def _separate_header_from_text(text: str):
    if not str.startswith(text, 'total '):
        print(text)
        sys.exit()
    head, _, text = text.partition('\n')
    return head, text


def _file_cleaner():
    if subprocess.run(['pwd'], stdout=subprocess.PIPE).stdout.decode(
            'utf-8').startswith('/mnt/'):
        return _clean_files_regular
    return _clean_files_in_mnt


def _get_shell_args():
    shell_args = ['ls', '-gGASh', '--color=always', ]
    shell_args.extend(sys.argv[1:])
    return shell_args


def _get_shell_text(shell_args) -> str:
    return subprocess.run(
        shell_args, stdout=subprocess.PIPE
    ).stdout.decode('utf-8')


# def _remove_start_color(text: str) -> str:
#     return re.sub(repl=r'\g<1>',
#                   pattern=r'\x1b\[0m(\x1b\[01;\d+m)', string=text,
#                   count=1)

FDATA = {
    "regular_files": {"cleaner": _file_cleaner(), "test": _regurlar_file_test, "data": []},
    "tmp_files": {"cleaner": _clean_files_tmp, "test": _tmp_file_test, "data": []},
    "dirs": {"cleaner": _clean_dirs, "test": _regurlar_dir_test, "data": []},
    "other_files": {"cleaner": _clean_other_files, "test": _other_file_test, "data": []},
}


def main():
    '''display directory files and folders'''
    text: str = _get_shell_text(_get_shell_args())
    assert isinstance(text, str), "text must by of type string"
    head, text = _separate_header_from_text(text)
    # text = _remove_start_color(text)
    flist = ["tmp_files", "regular_files", "dirs", "other_files"]
    FDATA["tmp_files"]["data"], FDATA["regular_files"]["data"], FDATA["dirs"]["data"], FDATA["other_files"]["data"], _ = filter_list(
        text.splitlines(), [FDATA[x]["test"] for x in flist])
    for i in flist:
        FDATA[i]["data"] = _map_join(FDATA[i]["cleaner"], FDATA[i]["data"])
    # t_files = _map_join(_file_cleaner(), files)
    # t_tmp_files = _map_join(_clean_files_tmp, temp_files)
    # t_dirs = _map_join(_clean_dirs, FDATA["dirs"]["data"])
    # t_other_files = _map_join(_clean_other_files, other_files)
    f_output_list = ["tmp_files", "dirs", "other_files", "regular_files", ]
    output_list = filter(lambda f: len(f) > 0,
                         [FDATA[x]["data"] for x in f_output_list])
    #  [t_tmp_files, t_dirs, t_other_files, t_files, head])
    print('\n'.join(output_list))
    print(head)


if __name__ == "__main__":
    main()
