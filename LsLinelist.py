import typing as T
from itertools import compress

from datetime import datetime as dt

from LsLine import FLine, FFileLine, FDirLine

TLine = T.Type[FLine]
TLineList = T.List[TLine]


class FLines:

    def __init__(self):
        self._lines: T.List = []
        self._line_generator = FLine
        self._current_time = dt.now()
        self._max_name = 15
        self._max_line = 8
        self._index = 0

    def _check_max(self, line):
        local_max = len(line.name) + 1
        if local_max > self._max_name:
            self._max_name = local_max

    def add(self, e, stats):
        line = self._line_generator(e, stats, self._current_time)
        self._lines.append(line)
        self._check_max(line)


    def _append_backup_to_line_name(self, index):
        self._lines[index].name += '/~'
        self._check_max(self._lines[index])

    def mark_backup_line(self, f_in_line):
        for i, fline in enumerate(self._lines, 0):
            if f_in_line.name[:-1] == fline.name:
                self._append_backup_to_line_name(i)
                return True
        return False

    def delete_lines(self, compression_index):
        self._lines = list(compress(self._lines, compression_index))

    def __str__(self) -> str:
        return '\n'.join(self.get_lines())

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, key: int):
        return self._lines[key]

    def __iter__(self):
        return self

    def __next__(self):
        for i in self._lines:
            yield i

    def _set_max_line(self, max_name: int, line_len: int, field_size=8):
        self._max_line = max_name + line_len * field_size

    def complete(self):
        if self._lines != []:
            last_line = self._lines[-1]
            self._set_max_line(last_line.max_name, len(last_line))
            self._lines = sorted(self._lines)

    def get_lines(self) -> T.List[str]:
        return [line.get_str(self._max_name) for line in self._lines]

    def get_raw_lines(self) -> T.List:
        return self._lines

    @property
    def max_name(self):
        return self._max_name

    @max_name.setter
    def max_name(self, max_name: int):
        self._max_name = max_name
        self._max_line = max_name + len(self._lines[0]) * 8

    @property
    def max_line(self):
        return self._max_line

class FileLines(FLines):
    def __init__(self):
        super().__init__()
        self._line_generator = FFileLine

class DirLines(FLines):
    def __init__(self):
        super().__init__()
        self._line_generator = FDirLine
