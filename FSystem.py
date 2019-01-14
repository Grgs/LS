from FNums import FSize, FTime


class FSystem:

    @staticmethod
    def _split(test, data):
        o_1, o_2 = [], []
        for i in data:
            if test(i):
                o_1.append(i)
            else:
                o_2.append(i)
        return o_1, o_2

    def __init__(self, line_type, current_time):
        self._regular = FLines(self._sort)
        self._other = FLines(self._sort)
        self.current_time = current_time
        self.is_split = False
        self.line_gen = FFileLine if line_type == 'file' else FDirLine

    def __repr__(self):
        return '<{!r}>{!r} \n{!r}'.format(self.current_time, self._regular,
                                          self._other)

    def __str__(self):
        return '\n'.join(map(str, [self._other, self._regular]))

    @staticmethod
    def _test_dot(line):
        return line.name.startswith('.')

    @staticmethod
    def _test_backup(line):
        return line.name.endswith('~')

    @staticmethod
    def _test_underscore(line):
        return line.name.startswith('_')

    @classmethod
    def _test(cls, line):
        pass

    @classmethod
    def _sort(cls, lines):
        return sorted(lines, key=lambda l: l.name, reverse=True)

    def add(self, e, stats):
        line = self.line_gen(e, stats, self.current_time)
        if self._test(line):
            self._regular.add(line)
        else:
            self._other.add(line)

    @property
    def regular(self):
        return self._regular

    @property
    def other(self):
        return self._other


class FFiles(FSystem):

    @classmethod
    def _test(cls, line):
        return not any([cls._test_backup(line), cls._test_dot(line)])

    @classmethod
    def _sort(cls, lines):
        return sorted(lines, key=lambda l: l.size, reverse=True)


class FDirs(FSystem):

    @classmethod
    def _test(cls, line):
        return not any([cls._test_dot(line), cls._test_underscore(line)])

    @classmethod
    def _sort(cls, lines):
        return sorted(lines, key=lambda l: l.name)


class FLine:

    def __init__(self, e):
        self._name = e.name
        self._line = []
        self._stored_str = None
        self._max_name = 8

    def get_str(self, name_max):
        self._stored_str = ' '.join([
            self._name.ljust(name_max, ' '),
            ' '.join([str(f) for f in self._line])
        ])
        return self._stored_str

    def _str(self):
        if self._stored_str is None:
            self._stored_str = ' '.join([
                self._name.ljust(self._max_name, ' '),
                ' '.join([str(f) for f in self._line])
            ])
        return self._stored_str

    def __str__(self):
        if self._stored_str is None:
            return self.get_str(self._max_name)
        return self._str()

    def __len__(self):
        return len(self._line)

    @property
    def max_name(self):
        return self.max_name

    @max_name.setter
    def max_name(self, max_name):
        self._max_name = max_name

    @property
    def name(self):
        return self._name


class FFileLine(FLine):

    def __init__(self, e, stats, current_time):
        super().__init__(e)
        self._line = [
            FSize(stats.st_size),
            FTime(stats.st_atime, current_time),
            FTime(stats.st_mtime, current_time),
        ]

    @property
    def size(self):
        return self._line[0]


class FDirLine(FLine):

    def __init__(self, e, stats, current_time):
        super().__init__(e)
        self._line = [
            FTime(stats.st_mtime, current_time),
        ]


class FLines:

    def __init__(self, sorter):
        self._lines = []
        self._sort = sorter
        self._max_name = 8
        self._max_line = 8
        self._index = 0

    def add(self, line):
        self._lines.append(line)
        if len(line.name) > self._max_name:
            self._max_name = len(line.name)
            # self._max_line = self._max_name + len(line) * 7

    def __str__(self):
        return '\n'.join(
            [l.get_str(self._max_name) for l in self._sort(self._lines)])
            # [str(l) for l in self._sort(self._lines)])

    def get_lines(self):
        return [l.get_str(self._max_name) for l in self._sort(self._lines)]

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, index):
        # return self._lines[index]
        return self._lines[index]

    # def max_line(self):
    #     return self._max_line

    # def empty(self):
    #     return ' ' * self._max_line
