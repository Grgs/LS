import unittest
import LsLine


class FFieldTest(unittest.TestCase):

    def test_static_dot_test(self):
        self.assertEqual(True, LsLine.FLine._test_dot('.name'))

        # def test_init_line(self):
        #   fline = LsLine.FLine()
