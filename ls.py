#!/usr/bin/env python3
# import profile
import os
import sys
from typing import *

from FileValue import FValue
from AllLines import AllLines


def _file_lines(_path: str):
    file_lines = AllLines()
    with os.scandir(_path) as osscandir:
        for e in osscandir:
            file_lines.add(FValue(e))
    return file_lines


def main():
    if len(sys.argv) > 1:
        _paths = [os.path.normpath(i) for i in sys.argv[1:]]
        if not all(map(os.path.exists, _paths)):
            print('Error: invalid path(s)')
            sys.exit(1)
        _paths = [i for i in _paths if os.path.isdir(i)]
        if _paths == []:
            print('Error: no path that is a directory')
            sys.exit(1)
    else:
        _paths = ['.']
    for _path in _paths:
        print(os.path.realpath(_path))
        print(_file_lines(_path).get_lines())


if __name__ == "__main__":
    # profile.run("pmain()")
    main()
