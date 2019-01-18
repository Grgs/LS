import typing as T
from itertools import compress

from LsNums import FSize, FTime


class FLine:

    def __init__(self, e, stats, current_time):
        self.name: str = e.name
        self.stats = stats
        self.current_time = current_time
        self._lnums: T.List[T.Union[FSize, FTime]] = []
        self.max_name = 15
        self._line_len = 0

    def _str(self) -> str:
        return ' '.join([
            self.name.ljust(self.max_name, ' '),
            ' '.join([str(f) for f in self._lnums])
        ])

    def __len__(self):
        return self._line_len

    def __str__(self):
        return self._str()

    def get_str(self, max_name: int):
        return self.name.ljust(
            max_name, fillchar=' ') + ' '.join([str(f) for f in self._lnums])

    def get_empty(self, max_name: int = None):
        if max_name is None:
            return ' ' * (self.max_name + len(self._lnums) * 8)
        return ' ' * (max_name + len(self._lnums) * 8)

    @property
    def size(self):
        return self.stats.st_size


class FFileLine(FLine):

    def __init__(self, e, stats, current_time):
        super().__init__(e, stats, current_time)
        self._lnums = [
            FSize(stats.st_size),
            FTime(stats.st_atime, current_time),
            FTime(stats.st_mtime, current_time),
        ]
        self._line_len = 3

    def __len__(self):
        return 3

    def get_str(self, max_name: int):
        return str.ljust(self.name, max_name, ' ') + ' '.join(
            [str(f) for f in self._lnums])


class FDirLine(FLine):

    def __init__(self, e, stats, current_time):
        super().__init__(e, stats, current_time)
        self._lnums = [
            FTime(stats.st_mtime, current_time),
        ]
        self._line_len = 1

    def __len__(self):
        return 1

    def get_str(self, max_name: int):
        return str.ljust(self.name, max_name, ' ') + str(self._lnums[0])


TLine = T.Type[FLine]
TLineList = T.List[TLine]


class FLines:

    def __init__(self, sorter: T.Callable[[TLineList], TLineList]):
        self._lines: T.List = []
        self._sort = sorter
        self._max_name = 15
        self._max_line = 8
        self._index = 0

    def _check_max(self, line):
        local_max = len(line.name) + 1
        if local_max > self._max_name:
            self._max_name = local_max

    def add(self, line: TLine):
        self._lines.append(line)
        self._check_max(line)

    def get_line(self, index) -> str:
        return self._lines[index].get_str(self._max_name)

    def _append_backup_to_line_name(self, index):
        self._lines[index].name += '/~'
        self._check_max(self._lines[index])

    def find_and_mark_backup_line(self, f_in_line):
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
            self._lines = self._sort(self._lines)

    def get_lines(self) -> T.List[str]:
        return [line.get_str(self._max_name) for line in self._lines]

    def get_raw_lines(self) -> T.List[str]:
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
