import unittest

from Line import FDirLine, FFileLine, FLine
from Linelist import FLines


class FFieldTest(unittest.TestCase):

    def setUp(self):
        self.fileline = FLines(FFileLine)
        self.dirline = FLines(FDirLine)

    def test_fileline_generates_something(self):
        self.assertIsNotNone(self.fileline)

    def test_dirline_generates_something(self):
        self.assertIsNotNone(self.dirline)
