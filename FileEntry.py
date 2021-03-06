import typing as T

from FileValue import FValue
from FileField import FName, FSize, FTime, FSpace


class FEntry:

    def __init__(self, e, current_time):
        self.e = e
        self.name = self.e.name
        self.current_time = current_time
        self._fields = []
        self._name_index = 0
        self._space_index = 1
        self.max_name = 12
        self.line_len = 0
        self.type = self.e.type
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

    def __str__(self):
        return self._str()

    def get_str(self, max_name: int) -> str:
        self._fields[self._space_index] = self._fields[
            self._space_index].finish(max_name)
        return ' '.join([str(f) for f in self._fields])

    def __len__(self):
        return self.line_len

    def append_backup_ending(self):
        self.name += '/~'
        self._fields[self._name_index].stored_string += '/~'
        self._fields[self._space_index].value += 2

    def name_entry(self):
        return FName(self.name)

    def space_entry(self):
        return FSpace(self.name)

    def size_entry(self):
        return FSize(self.e.size)

    def time_entry(self):
        return FTime(self.e.mtime, self.current_time)


class FFileEntry(FEntry):

    def __init__(self, e, current_time):
        super().__init__(e, current_time)
        self._fields = [
            self.name_entry(),
            self.space_entry(),
            self.size_entry(),
            self.time_entry(),
        ]
        self.sort_by = -1 * self.e.size


class FDirEntry(FEntry):

    def __init__(self, e, current_time):
        super().__init__(e, current_time)
        self._fields = [
            self.name_entry(),
            self.space_entry(),
            self.time_entry(),
        ]
        self.sort_by = self.name
