class FValue:

    @staticmethod
    def _test_dot(name):
        return name.startswith('.')

    @staticmethod
    def _test_tilda(name):
        return name.endswith('~')

    @staticmethod
    def _test_underscore(name):
        return name.startswith('_')

    def __init__(self, entry):
        self.name = entry.name
        self._stats = entry.stat()
        self.size = self._stats.st_size
        self.mtime = self._stats.st_mtime
        self.is_file = entry.is_file()
        self.is_hidden = self._test_dot(self.name)
        self.is_backup = self._test_tilda(self.name)
        self.is_cache = self._test_underscore(self.name)
        self.type = self.is_backup * -4 + self.is_cache * -2 + self.is_hidden * -1