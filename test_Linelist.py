import unittest

from Entry import FDirEntry, FFileEntry, FEntry
from Linelist import FLines


class FFieldTest(unittest.TestCase):

    def setUp(self):
        self.fileline = FLines(FFileEntry)
        self.dirline = FLines(FDirEntry)

    def test_fileline_generates_something(self):
        self.assertIsNotNone(self.fileline)

    def test_dirline_generates_something(self):
        self.assertIsNotNone(self.dirline)
