"""Tests for the ArchiveConfig entity."""

import unittest

from tasks.archive_bot.domain.entities.archive_config import (
    AGE_MODE,
    SIZE_MODE,
    ArchiveConfig,
)


class TestArchiveConfig(unittest.TestCase):
    """Tests for :class:`ArchiveConfig`."""

    def test_age_mode_hours(self):
        config = ArchiveConfig(archive_type=AGE_MODE, value=10,
                               base_prefix="نقاش المستخدم:X/أرشيف", counter=1)
        self.assertTrue(config.is_age_mode)
        self.assertEqual(config.age_hours, 240)
        self.assertEqual(config.size_threshold_bytes, 10000)

    def test_size_mode_hours(self):
        config = ArchiveConfig(archive_type=SIZE_MODE, value=70,
                               base_prefix="نقاش المستخدم:X/أرشيف", counter=1)
        self.assertFalse(config.is_age_mode)
        self.assertEqual(config.age_hours, 1)
        self.assertEqual(config.size_threshold_bytes, 70000)


if __name__ == "__main__":
    unittest.main()
