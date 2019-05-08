import typing as T
from datetime import datetime as dt
from itertools import compress

from FileEntry import FDirEntry, FFileEntry, FEntry


class FLines:

    def __init__(self, LineGenerator):
        self._lines: T.List[FFileEntry, FDirEntry] = []
        self._line_generator = LineGenerator
        self._current_time = dt.now()
        self._max_line = self._max_name = 12
        self._index = 0

    def add(self, e):
        line = self._line_generator(e, self._current_time)
        self._lines.append(line)

    def __str__(self) -> str:
        return '\n'.join(self.get_lines())

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, key: int):
        return self._lines[key]

    def _set_max_line(self):
        self._max_name = max([len(i.name) for i in self._lines])
        self._max_line = self._max_name + 2 * 8 + 1

    def _mark_backup_line(self, f_in_line):
        for index, fline in enumerate(self._lines, 0):
            if f_in_line.name[:-1] == fline.name:
                self._lines[index].append_backup_ending()
                return 0
        return 1

    def _delete_lines(self, compression_index):
        self._lines = list(compress(self._lines, compression_index))

    def delete_tmps_from_list(self):
        lines_to_compress = []
        for fline in self._lines:
            if fline.e.is_backup:
                lines_to_compress.append(self._mark_backup_line(fline))
            else:
                lines_to_compress.append(1)
        self._delete_lines(lines_to_compress)

    def finalize(self):
        if self._lines != []:
            self._set_max_line()
            self._lines = sorted(self._lines)

    def get_empty_line(self) -> str:
        return ' ' * (self._max_line + 2)

    def get_lines(self) -> T.List[str]:
        return [line.get_str(self._max_name) for line in self._lines]

    def get_raw_lines(self) -> T.List:
        return self._lines

    @property
    def max_name(self):
        return self._max_name

    @property
    def max_line(self):
        return self._max_line
