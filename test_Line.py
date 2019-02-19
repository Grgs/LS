import unittest

from Line import FLine


class FFieldTest(unittest.TestCase):

    def test_static_dot_test(self):
        self.assertEqual(True, FLine._test_dot('.name'))
