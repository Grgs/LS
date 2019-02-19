import unittest
from System import FSystem


class FFieldTest(unittest.TestCase):

    def setUp(self):
        self.fsys = FSystem()

    def test_fsystem_init(self):
        self.assertIsNotNone(self.fsys)
