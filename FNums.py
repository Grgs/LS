from datetime import datetime as dt
from datetime import timedelta
import math


class FNums:

    def __init__(self, value):
        self.value = value

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


class FSize(FNums):

    def __str__(self):
        # modified from https://stackoverflow.com/a/14822210/7022271
        if self.value == 0:
            return '|{size: >6} B'.format(size=0)
        size_name = (" B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(self.value, 1024)))
        size = round(self.value / math.pow(1024, i), 2)
        return '|{size: >6}{size_name}'.format(
            size=size, size_name=size_name[i])
        # return f'{size}{size_name[i]}'
        # return '{size}{size_name[i]}'.format(size=size, size_name=size_name[i])
        # return _convert_size(self.value)


class FTime(FNums):

    def __init__(self, value, current_time=dt.now()):
        self.current_time = current_time
        self.value_date = dt.utcfromtimestamp(value)
        return super().__init__(value)

    def __str__(self):
        if self.value_date.year != self.current_time.year:
            return '{:%Y-%m}'.format(self.value_date)
        if self.value_date.month != self.current_time.month:
            return '{:%m-%d}'.format(self.value_date)
        if self.value_date.day != self.current_time.day:
            diffdate = self.value_date - self.current_time
            return '{0.days} {1:%H}'.format(diffdate, self.value_date)
        diffdate = self.current_time - self.value_date
        return '{0}'.format(diffdate // timedelta(hours=1))