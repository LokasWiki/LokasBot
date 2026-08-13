"""Tests for the keep-vs-archive decision engine."""

import unittest

from tasks.archive_bot.domain.entities.section import Section
from tasks.archive_bot.domain.use_cases.decide_archive import classify


def section(heading, content):
    return Section(heading=heading, content=content,
                   heading_markup=f"== {heading} ==")


class TestClassify(unittest.TestCase):
    """Tests for :func:`classify`."""

    def test_unchanged_section_archived(self):
        current = [section("قديم", "\nنقاش قديم\n")]
        old = [section("قديم", "\nنقاش قديم\n")]
        keep, archive = classify(current, old)
        self.assertEqual(archive, current)
        self.assertEqual(keep, [])

    def test_new_section_kept(self):
        current = [section("قديم", "\nنقاش\n"), section("جديد", "\nنقاش جديد\n")]
        old = [section("قديم", "\nنقاش\n")]
        keep, archive = classify(current, old)
        self.assertEqual(keep, [current[1]])
        self.assertEqual(archive, [current[0]])

    def test_changed_section_kept(self):
        current = [section("قديم", "\nنقاش معدل\n")]
        old = [section("قديم", "\nنقاش\n")]
        keep, archive = classify(current, old)
        self.assertEqual(keep, current)
        self.assertEqual(archive, [])

    def test_do_not_archive_kept(self):
        current = [section("قديم", "\nنقاش {{لا للأرشفة}}\n")]
        old = [section("قديم", "\nنقاش {{لا للأرشفة}}\n")]
        keep, archive = classify(current, old)
        self.assertEqual(keep, current)
        self.assertEqual(archive, [])

    def test_do_not_archive_with_whitespace(self):
        current = [section("قديم", "\nنقاش {{ لا للأرشفة }}\n")]
        old = [section("قديم", "\nنقاش {{ لا للأرشفة }}\n")]
        keep, archive = classify(current, old)
        self.assertEqual(keep, current)
        self.assertEqual(archive, [])

    def test_duplicate_headings_match_positionally(self):
        current = [
            section("أ", "\n1"),
            section("أ", "\n2"),
            section("أ", "\n3"),
        ]
        old = [
            section("أ", "\n1"),
            section("أ", "\n2"),
        ]
        keep, archive = classify(current, old)
        # Third "أ" is new -> kept; first two unchanged -> archived.
        self.assertEqual(archive, current[:2])
        self.assertEqual(keep, current[2:])

    def test_min_threads_left(self):
        current = [
            section("أ", "\n1"),
            section("ب", "\n2"),
            section("ج", "\n3"),
        ]
        old = current[:]  # all unchanged
        keep, archive = classify(current, old, min_threads_left=2)
        # At least 2 threads must remain.
        self.assertEqual(len(keep), 2)
        self.assertEqual(len(archive), 1)

    def test_max_threads_overflow_archived(self):
        current = [
            section("أ", "\n1"),
            section("ب", "\n2"),
            section("ج", "\n3"),
        ]
        old = []  # all new -> all kept initially
        keep, archive = classify(current, old, max_threads=2)
        self.assertEqual(len(keep), 2)
        self.assertEqual(len(archive), 1)
        # Newest threads remain: "ب" and "ج" kept, oldest "أ" archived.
        self.assertEqual(keep, current[1:])
        self.assertEqual(archive, current[:1])


if __name__ == "__main__":
    unittest.main()
