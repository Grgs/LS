import unittest

from Linelist import FLines


class FFieldTest(unittest.TestCase):

    def test_flines_init(self):
        flines = FLines()
        self.assertEqual(0, flines._index)
