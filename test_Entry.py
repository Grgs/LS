import unittest

from Entry import FEntry


class FFieldTest(unittest.TestCase):

    def test_static_dot_test(self):
        self.assertEqual(True, FEntry._test_dot('.name'))
