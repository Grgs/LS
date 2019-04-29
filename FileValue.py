class FValue:

    def __init__(self, entry):
        self.name = entry.name
        self._stats = entry.stat()
        self.size = self._stats.st_size
        self.mtime = self._stats.st_mtime
        self.is_file = entry.is_file()
        self.is_hidden = self.name.startswith('.')
        self.is_backup = self.name.endswith('~')
        self.is_cache = self.name.startswith('_')
        self.type = self.is_backup * -4 + self.is_cache * -2 + self.is_hidden * -1