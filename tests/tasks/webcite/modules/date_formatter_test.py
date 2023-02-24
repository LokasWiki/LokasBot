import unittest
from datetime import datetime

from tasks.webcite.modules.date_formatter import DateFormatter


class TestDateFormatter(unittest.TestCase):
    def setUp(self):
        self.date_formatter = DateFormatter()

    def test_format_timestamp_english(self):
        timestamp = '20220125101500'
        expected_output = '25 January 2022'
        self.assertEqual(self.date_formatter.format_timestamp(timestamp), expected_output)

    def test_format_timestamp_arabic(self):
        timestamp = '20220125101500'
        expected_output = '25 يناير 2022'
        self.date_formatter.language = 'ar'
        self.assertEqual(self.date_formatter.format_timestamp(timestamp), expected_output)

    def test_format_timestamp_invalid_input(self):
        timestamp = '20220x25101500'
        with self.assertRaises(ValueError):
            self.date_formatter.format_timestamp(timestamp)

    def test_format_timestamp_different_language(self):
        timestamp = '20220125101500'
        expected_output = '25 January 2022'
        self.date_formatter.language = 'en'
        self.assertEqual(self.date_formatter.format_timestamp(timestamp), expected_output)

        expected_output = '25 يناير 2022'
        self.date_formatter.language = 'ar'
        self.assertEqual(self.date_formatter.format_timestamp(timestamp), expected_output)

    def test_format_timestamp_same_month(self):
        timestamp = '20220201101500'
        expected_output = '01 February 2022'
        self.assertEqual(self.date_formatter.format_timestamp(timestamp), expected_output)

    def test_format_timestamp_leap_year(self):
        timestamp = '20240229101500'
        expected_output = '29 February 2024'
        self.assertEqual(self.date_formatter.format_timestamp(timestamp), expected_output)

if __name__ == '__main__':
    unittest.main()
