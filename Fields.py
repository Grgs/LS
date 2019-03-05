from datetime import datetime as dt

import humanize


class FField:

    def __init__(self, value):
        self.value = value
        self._stored_string = None

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __hash__(self):  #pragma: no cover
        return self.value

    def __str__(self):
        if self._stored_string is None:
            self._stored_string = self._str()
        return self._stored_string

    def _str(self) -> str:
        return str(self.value)

    def finish(self, max_name):
        return self


class FName(FField):

    def __init__(self, value):
        super().__init__(value)
        self.string_val = self.value

    def _str(self) -> str:
        return self.string_val

    def finish(self, max_name):
        self.string_val = str.ljust(self.string_val, max_name, ' ')
        return self


class FSize(FField):

    def _str(self) -> str:
        return '{:>8}'.format(humanize.naturalsize(self.value, gnu=True))


class FTime(FField):

    def __init__(self, value, current_time=dt.now()):
        self.current_time = current_time
        self.value_date = dt.fromtimestamp(value)
        super().__init__(value)

    def _str(self) -> str:
        if self.value_date.year != self.current_time.year:
            return '{:%Y-%m}'.format(self.value_date)
        diffdate = abs(self.current_time - self.value_date)
        if diffdate.days >= 30:
            return '{:%mm-%dd}'.format(self.value_date)
        diffhours = (diffdate.seconds // 3600) % 24
        if diffdate.days != 0:
            return '{0:>2}d {1:>2}h'.format(diffdate.days, diffhours)
        diffminutes = (diffdate.seconds // 60) % 60
        if diffhours != 0:
            return '{0:>2}h {1:>2}m'.format(diffhours, diffminutes)
        diffseconds = diffdate.seconds % 60
        return '{0:>2}m {1:>2}s'.format(diffminutes, diffseconds)
