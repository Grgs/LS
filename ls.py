#!/usr/bin/env python3
"""display directory files and folders"""
import subprocess
import sys
from itertools import chain, compress, repeat
from typing import List

import regex as re

from guirguis.filter import filter_dict

COLOR_STOP = "[0m"


def _combine_cleaned(clean_fun, text_list):
    return map(clean_fun, text_list)


def _map_join(clean_fun, text_list):
    return "\n".join(map(clean_fun, text_list))


def _regurlar_file_test(line: str) -> bool:
    return line.startswith("-")


def _tmp_file_test(line: str) -> bool:
    return any([line.endswith("~"), line.endswith("~" + COLOR_STOP)])


def _regurlar_dir_test(line: str) -> bool:
    return line.startswith("d")


def _other_file_test(line: str) -> bool:
    return len(line) > 0


def _split_start(line: str) -> List[str]:
    return re.split(r"\s+", line, maxsplit=3)


def _compress_start(chuncks: List[str], filter_select: List[int]):
    return compress(chuncks, chain(filter_select, repeat(1)))


def _split_compress_start(line: str, filter_select: List[int]):
    return _compress_start(_split_start(line), filter_select)


def _clean_dirs(line: str) -> str:
    return _split_start(line)[-1] + COLOR_STOP


def _clean_regular_files(line: str) -> str:
    return "{} {:>6} {}".format(*_split_compress_start(line, [1, 0]))[1:] + COLOR_STOP


def _clean_other_files(line: str) -> str:
    output_0, output_1 = _split_compress_start(line, [1, 0, 0])
    return "{} {}".format(output_0[0], output_1) + COLOR_STOP


def _clean_mnt_files(line: str) -> str:
    return "{:>6} {}".format(*_split_compress_start(line, [0, 0])) + COLOR_STOP


def _clean_files_tmp(line: str) -> str:
    return re.sub(r"\x1b\[0m|\x1b\[01;\d+m", "", _clean_mnt_files(line))


def _separate_header_from_text(text: str):
    if not str.startswith(text, "total "):
        print(text)
        sys.exit()
    head, _, text = text.partition("\n")
    return head, text


def _file_cleaner():
    if (
        subprocess.run(["pwd"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .startswith("/mnt/")
    ):
        return _clean_mnt_files
    return _clean_regular_files


def _get_shell_args():
    shell_args = ["ls", "-gGASh", "--color=always"]
    shell_args.extend(sys.argv[1:])
    return shell_args


def _get_shell_text(shell_args) -> str:
    return subprocess.run(shell_args, stdout=subprocess.PIPE).stdout.decode("utf-8")


def _set_max_len(fdata):
    for k, f in fdata.items():
        fdata[k]["max_len"] = max(f["data"], key=len)


def _is_hidden(text: str):
    return bool(re.search(r"\s(\x1b\[\d+;\d+m)?\.", text, flags=re.V1))


def _sort_dot(lines):
    return sorted(lines, key=_is_hidden, reverse=True)


FDATA = {
    "regular_files": {
        "cleaner": _file_cleaner(),
        "test": _regurlar_file_test,
        "data": [],
        "max_len": -1,
    },
    "tmp_files": {
        "cleaner": _clean_files_tmp,
        "test": _tmp_file_test,
        "data": [],
        "max_len": -1,
    },
    "dirs": {
        "cleaner": _clean_dirs,
        "test": _regurlar_dir_test,
        "data": [],
        "max_len": -1,
    },
    "other_files": {
        "cleaner": _clean_other_files,
        "test": _other_file_test,
        "data": [],
        "max_len": -1,
    },
}

LINE_FILTER_ORDER = ["tmp_files", "regular_files", "dirs"]
LINE_FILTER_ORDER_FALLBACK = "other_files"
LINE_OUTPUT_ORDER = ["tmp_files", "dirs", "other_files", "regular_files"]


def main():
    """display directory files and folders"""
    text: str = _get_shell_text(_get_shell_args())
    assert isinstance(text, str), "text must by of type string"
    head, text = _separate_header_from_text(text)
    filter_dict(text.splitlines(), FDATA, LINE_FILTER_ORDER, LINE_FILTER_ORDER_FALLBACK)
    for fname, fval in FDATA.items():
        FDATA[fname]["data"] = _sort_dot(
            _combine_cleaned(fval["cleaner"], fval["data"])
        )
        # FDATA[fname]["data"] =   sorted()      FDATA[fname]["data"]
        # FDATA[fname]["max_len"] = max(map(len, FDATA[fname]["data"]), default=0)
        # sorted(FDATA[x]["data"], key=lambda s: " ." in s, reverse=True)
    output_list = chain(*[FDATA[x]["data"] for x in LINE_OUTPUT_ORDER])
    # output_list = chain(*[_sort_dot(FDATA[x]["data"]) for x in LINE_OUTPUT_ORDER])
    print("\n".join(output_list))
    print(head)


if __name__ == "__main__":
    main()
