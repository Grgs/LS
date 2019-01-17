from datetime import datetime as dt
from datetime import timedelta
import math


class FNums:

    def __init__(self, value):
        self.value = value
        self._stored_string = None

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __hash__(self):
        return self.value

    def __str__(self):
        if self._stored_string is None:
            self._stored_string = self._str()
        return self._stored_string

    def _str(self):
        return str(self.value)


class FSize(FNums):

    def _str(self):
        # modified from https://stackoverflow.com/a/14822210/7022271
        if self.value == 0:
            return '{size: >6}B '.format(size=0)
        size_name = ("B ", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(self.value, 1024)))
        size = round(self.value / math.pow(1024, i), 2)
        return '{size: >6}{size_name}'.format(size=size, size_name=size_name[i])


class FTime(FNums):

    def __init__(self, value, current_time=dt.now()):
        self.current_time = current_time
        self.value_date = dt.utcfromtimestamp(value)
        super().__init__(value)

    def _str_inner(self):
        if self.value_date.year != self.current_time.year:
            return '{:%Y-%m}'.format(self.value_date)
        if self.value_date.month != self.current_time.month:
            return '{:%m-%d}'.format(self.value_date)
        diffdate = self.current_time - self.value_date
        if self.value_date.day != self.current_time.day:
            return '{0:>2}d {1:>2}h'.format(
                abs(diffdate.days), (diffdate - timedelta(days=diffdate.days))
                // timedelta(hours=1))
        if self.value_date.hour < self.current_time.hour:
            return '{0:>2}h {1:>2}m'.format(
                int(diffdate / timedelta(hours=1)),
                diffdate.seconds % (60 * 60) // 60)
        return '{0:>2}m {1:>2}s'.format(diffdate.seconds % (60 * 60) // 60,
                                        diffdate.seconds % 60)

    def _str(self):
        return '{:<8}'.format(self._str_inner())
