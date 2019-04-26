import unittest

from AllLines import AllLines


class FFieldTest(unittest.TestCase):

    def setUp(self):
        self.fsys = AllLines()

    def test_AllLines_init(self):
        self.assertIsNotNone(self.fsys)
