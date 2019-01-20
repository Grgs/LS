import typing as T

from LsNums import FSize, FTime


class FLine:

    @staticmethod
    def _test_dot(name):
        return name.startswith('.')

    @staticmethod
    def _test_tilda(name):
        return name.endswith('~')

    @staticmethod
    def _test_underscore(name):
        return name.startswith('_')

    def __init__(self, e, stats, current_time):
        self.name: str = e.name
        self.stats = stats
        self.current_time = current_time
        self._lnums: T.List[T.Union[FSize, FTime]] = []
        self.max_name = 15
        self.line_len = 0
        self.is_hidden = self._test_dot(self.name)
        self.is_backup = self._test_tilda(self.name)
        self.is_cache = self._test_underscore(self.name)
        self.type = self.is_backup * -100 + self.is_cache * -10 + self.is_hidden * -1
        self.sort_by = None

    def _str(self) -> str:
        return ' '.join([
            self.name.ljust(self.max_name, ' '),
            ' '.join([str(f) for f in self._lnums])
        ])

    def __lt__(self, other):
        if self.type == other.type:
            return self.sort_by < other.sort_by
        return self.type < other.type

    def __le__(self, other):
        if self.type == other.type:
            return self.sort_by <= other.sort_by
        return self.type <= other.type

    def __eq__(self, other):
        if self.type == other.type:
            return self.sort_by == other.sort_by
        return False

    def __ne__(self, other):
        if self.type == other.type:
            return self.sort_by != other.sort_by
        return self.type != other.type

    def __ge__(self, other):
        if self.type == other.type:
            return self.sort_by >= other.sort_by
        return self.type >= other.type

    def __gt__(self, other):
        if self.type == other.type:
            return self.sort_by > other.sort_by
        return self.type > other.type

    def __hash__(self):
        return self._str()

    def __len__(self):
        return self.line_len

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
        self.line_len = 3
        self.sort_by = -1 * self.size

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
        self.line_len = 1
        self.sort_by = self.name

    def __len__(self):
        return 1

    def get_str(self, max_name: int):
        return str.ljust(self.name, max_name, ' ') + str(self._lnums[0])
