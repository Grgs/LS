import typing as T


class FLine:

    def __init__(self, ent):
      self.ent = ent

    def _str(self) -> str:
        return ' '.join([
            self.name.ljust(self.max_name, ' '),
            ' '.join([str(f) for f in self._fields])
        ])

    def __hash__(self):
        return self._str()

    def __str__(self):
        return self._str()

    def get_str(self, max_name: int) -> str:
        self._fields[self._name_index] = self._fields[0].finish(max_name)
        return ' '.join([str(f) for f in self._fields])

    def __len__(self):
        return self.line_len

    def append_backup_ending(self):
        self.name += '/~'
        self._fields[self._name_index].string_val += '/~'


class FFileLine(FEntry):

    def __init__(self, e, current_time):
        super().__init__(e, current_time)
        self._fields = [
            FName(self.name),
            FSize(self.e.size),
            FTime(self.e.mtime, current_time),
        ]
        self.line_len = len(self.name) + (len(self._fields) - 1) * 8
        self.sort_by = -1 * self.e.size


class FDirLine(FEntry):

    def __init__(self, e, current_time):
        super().__init__(e, current_time)
        self._fields = [
            FName(self.name),
            FTime(self.e.mtime, current_time),
        ]
        self.line_len = len(self.name) + (len(self._fields) - 1) * 8
        self.sort_by = self.name
