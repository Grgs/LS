import unittest
from datetime import datetime as dt

import Fields


class FFieldTest(unittest.TestCase):

    def setUp(self):
        self.fourty_two = Fields.FField(42)
        self.another_fourty_two = Fields.FField(42)
        self.fourty_one = Fields.FField(41)

    def test_equals_zero(self):
        ffield = Fields.FField(0)
        self.assertEqual(ffield.value, 0)

    def test_equals_correctly(self):
        self.assertTrue(self.fourty_two == self.another_fourty_two)
        self.assertFalse(self.fourty_one == self.fourty_two)

    def test_not_equals_correctly(self):
        self.assertFalse(self.fourty_two != self.another_fourty_two)
        self.assertTrue(self.fourty_one != self.fourty_two)

    def test_lessthan_correctly(self):
        self.assertTrue(self.fourty_one < self.fourty_two)

    def test_morethan_correctly(self):
        self.assertTrue(self.fourty_two > self.fourty_one)

    def test_morethan_equal_correctly(self):
        self.assertTrue(self.fourty_two >= self.fourty_one)
        self.assertTrue(self.fourty_two >= self.another_fourty_two)

    def test_lessthan_equal_correctly(self):
        self.assertTrue(self.fourty_one <= self.fourty_two)
        self.assertTrue(self.fourty_two <= self.another_fourty_two)

    def test_string(self):
        self.assertEqual(str(self.fourty_two), '42')


class FSizeTest(unittest.TestCase):

    def test_equals_zero(self):
        fsize = Fields.FSize(0)
        self.assertRegex(str(fsize), ' *0B')
        # assert str(fsize).endswith(' 0B')

    def test_equals_zero(self):
        fsize = Fields.FSize(1024)
        self.assertRegex(str(fsize), ' *1\.0K')


class FTimeTest(unittest.TestCase):

    def setUp(self):
        self.file_time = 1544143207
        self.plus_one_hour = 1544146807
        self.one_hour_diff = Fields.FTime(self.file_time,
                                          dt.fromtimestamp(self.plus_one_hour))

    def test_has_current_time(self):
        self.assertIsNotNone(self.one_hour_diff.current_time)

    def test_current_time_is_greater_than_file_time(self):
        self.assertGreater(self.one_hour_diff.current_time,
                           self.one_hour_diff.value_date)

    def test_zero_minutes_in_one_hour(self):
        self.assertRegex(str(self.one_hour_diff), r' 0m')

    def test_1_hour_in_one_hour(self):
        self.assertRegex(str(self.one_hour_diff), r'^ *1h ')
