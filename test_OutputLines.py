import unittest

from OutputLines import OutputLines


class FFieldTest(unittest.TestCase):

    def setUp(self):
        self.fsys = OutputLines()

    def test_fsystem_init(self):
        self.assertIsNotNone(self.fsys)
