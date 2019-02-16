import unittest
from ls import LsNums


class FFieldTest(unittest.TestCase):

    def setUp(self):
        self.fourty_two = LsNums.FField(42)
        self.another_fourty_two = LsNums.FField(42)
        self.fourty_one = LsNums.FField(41)

    def test_equals_zero(self):
        ffield = LsNums.FField(0)
        self.assertEqual(ffield.value, 0)

    def test_equals_correctly(self):
        self.assertTrue(self.fourty_two == self.another_fourty_two)
        self.assertFalse(self.fourty_one == self.fourty_two)

    def test_not_equals_correctly(self):
        self.assertFalse(self.fourty_two != self.another_fourty_two)
        self.assertTrue(self.fourty_one != self.fourty_two)

    def test_lessthan_correctly(self):
        self.assertTrue(self.fourty_one < self.fourty_two)

    def test_string(self):
        self.assertEqual(str(self.fourty_two), '42')


class FSizeTest(unittest.TestCase):

    def test_equals_zero(self):
        fsize = LsNums.FSize(0)
        self.assertEqual(fsize.value, 0)
