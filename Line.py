import typing as T

from Fields import FSize, FTime, FName


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
        self._fields = []
        # self._fields = [FName(self.name)]
        self.max_name = 15
        self.line_len = 0
        self.is_hidden = self._test_dot(self.name)
        self.is_backup = self._test_tilda(self.name)
        self.is_cache = self._test_underscore(self.name)
        self.type = self.is_backup * -4 + self.is_cache * -2 + self.is_hidden * -1
        self.sort_by = None

    def _str(self) -> str:
        return ' '.join([
            self.name.ljust(self.max_name, ' '),
            ' '.join([str(f) for f in self._fields])
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
        return self.type == other.type and self.sort_by == other.sort_by

    def __ne__(self, other):
        return self.type != other.type or self.sort_by != other.sort_by

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
            max_name, fillchar=' ') + ' '.join([str(f) for f in self._fields])

    def get_empty(self, max_name: int = None):
        if max_name is None:
            return ' ' * (self.max_name + len(self._fields) * 8)
        return ' ' * (max_name + len(self._fields) * 8)

    @property
    def size(self):
        return self.stats.st_size


class FFileLine(FLine):

    def __init__(self, e, stats, current_time):
        super().__init__(e, stats, current_time)
        self._fields.extend([
            FSize(stats.st_size),
            # FTime(stats.st_atime, current_time),
            FTime(stats.st_mtime, current_time),
        ])
        self.line_len = len(self._fields)
        self.sort_by = -1 * self.size

    def __len__(self):
        return len(self._fields)

    def get_str(self, max_name: int):
        return str.ljust(self.name, max_name, ' ') + ' '.join(
            [str(f) for f in self._fields])


class FDirLine(FLine):

    def __init__(self, e, stats, current_time):
        super().__init__(e, stats, current_time)
        self._fields.extend([
            FTime(stats.st_mtime, current_time),
        ])
        self.line_len = 1
        self.sort_by = self.name

    def __len__(self):
        return 1

    def get_str(self, max_name: int):
        return str.ljust(self.name, max_name, ' ') + str(self._fields[0])
