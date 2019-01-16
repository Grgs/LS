from FNums import FSize, FTime


class FLine:

    def __init__(self, e):
        self._name = e.name
        self._line = []
        self._stored_str = None
        self._max_name = 8

    def get_str(self, max_name):
        self._max_name = max_name
        self._stored_str = self._str()
        return self._stored_str

    def _str(self):
        return ' '.join([
            self._name.ljust(self._max_name, ' '),
            ' '.join([str(f) for f in self._line])
        ])

    def __str__(self):
        if self._stored_str is None:
            return self.get_str(self._max_name)
        return self._str()

    @property
    def max_name(self):
        return self._max_name

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

    def __len__(self):
        return 3

    @property
    def size(self):
        return self._line[0]


class FDirLine(FLine):

    def __init__(self, e, stats, current_time):
        super().__init__(e)
        self._line = [
            FTime(stats.st_mtime, current_time),
        ]

    def __len__(self):
        return 1


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
            self._max_line = self._max_name + len(line) * 8

    def __str__(self):
        return '\n'.join(
            [l.get_str(self._max_name) for l in self._sort(self._lines)])

    def get_lines(self):
        return [l.get_str(self._max_name) for l in self._sort(self._lines)]

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, index):
        # return self._lines[index]
        return self._lines[index]

    @property
    def max_name(self):
        return self._max_name

    # def max_line(self):
    #     return self._max_line

    # def empty(self):
    #     return ' ' * self._max_line
