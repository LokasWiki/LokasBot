"""Tests for the {{أرشفة آلية}} template parser."""

import unittest

from tasks.archive_bot.domain.entities.archive_config import AGE_MODE, SIZE_MODE
from tasks.archive_bot.domain.use_cases.parse_archive_config import (
    ParseArchiveConfig,
)


class TestParseArchiveConfig(unittest.TestCase):
    """Tests for :class:`ParseArchiveConfig`."""

    def setUp(self):
        self.parser = ParseArchiveConfig()

    def test_age_mode(self):
        config = self.parser.parse(
            "{{أرشفة آلية|قسم|10|نقاش المستخدم:مبتدئ/أرشيف 6}}"
        )
        self.assertIsNotNone(config)
        self.assertEqual(config.archive_type, AGE_MODE)
        self.assertEqual(config.value, 10)
        self.assertEqual(config.base_prefix, "نقاش المستخدم:مبتدئ/أرشيف")
        self.assertEqual(config.counter, 6)
        self.assertTrue(config.is_age_mode)
        self.assertEqual(config.age_hours, 240)

    def test_size_mode(self):
        config = self.parser.parse(
            "{{أرشفة آلية|حجم|70|نقاش المستخدم:Elsayed Taha/أرشيف 2}}"
        )
        self.assertIsNotNone(config)
        self.assertEqual(config.archive_type, SIZE_MODE)
        self.assertEqual(config.value, 70)
        self.assertEqual(config.counter, 2)
        self.assertFalse(config.is_age_mode)
        self.assertEqual(config.age_hours, 1)
        self.assertEqual(config.size_threshold_bytes, 70000)

    def test_legacy_flag_عددي(self):
        config = self.parser.parse(
            "{{أرشفة آلية|قسم|7|عددي|نقاش المستخدم:Nassim-alge/أرشيف 1}}"
        )
        self.assertIsNotNone(config)
        self.assertEqual(config.archive_type, AGE_MODE)
        self.assertEqual(config.value, 7)
        self.assertEqual(config.base_prefix, "نقاش المستخدم:Nassim-alge/أرشيف")
        self.assertEqual(config.counter, 1)

    def test_legacy_flag_عددى(self):
        config = self.parser.parse(
            "{{أرشفة آلية|قسم|7|عددى|نقاش المستخدم:Reiser115/أرشيف 1}}"
        )
        self.assertIsNotNone(config)
        self.assertEqual(config.counter, 1)

    def test_no_counter(self):
        config = self.parser.parse(
            "{{أرشفة آلية|حجم|100|نقاش المستخدم:مواطن تونسي/أرشيف }}"
        )
        self.assertIsNotNone(config)
        self.assertEqual(config.base_prefix, "نقاش المستخدم:مواطن تونسي/أرشيف")
        self.assertEqual(config.counter, 0)

    def test_embedded_in_page_text(self):
        text = (
            "مقدمة\n"
            "{{أرشفة آلية|قسم|15|نقاش المستخدم:Example/أرشيف 3}}\n"
            "== قسم ==\nنقاش\n"
        )
        config = self.parser.parse(text)
        self.assertIsNotNone(config)
        self.assertEqual(config.counter, 3)

    def test_whitespace_tolerance(self):
        config = self.parser.parse(
            "{{ أرشفة آلية | قسم | 10 | نقاش المستخدم:Example/أرشيف 6 }}"
        )
        self.assertIsNotNone(config)
        self.assertEqual(config.archive_type, AGE_MODE)
        self.assertEqual(config.value, 10)
        self.assertEqual(config.base_prefix, "نقاش المستخدم:Example/أرشيف")
        self.assertEqual(config.counter, 6)

    def test_no_template_returns_none(self):
        self.assertIsNone(self.parser.parse("== قسم ==\nنقاش بلا قالب"))

    def test_missing_params_returns_none(self):
        self.assertIsNone(self.parser.parse("{{أرشفة آلية|قسم|10}}"))

    def test_non_integer_value_returns_none(self):
        self.assertIsNone(
            self.parser.parse("{{أرشفة آلية|قسم|عشرة|نقاش المستخدم:X/أرشيف 1}}")
        )


if __name__ == "__main__":
    unittest.main()
