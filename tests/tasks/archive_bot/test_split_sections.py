"""Tests for the section splitter."""

import unittest

from tasks.archive_bot.domain.use_cases.split_sections import split_sections


class TestSplitSections(unittest.TestCase):
    """Tests for :func:`split_sections`."""

    def test_split_with_preamble(self):
        text = "Intro\n== Section A ==\nContent A\n== Section B ==\nContent B"
        preamble, sections = split_sections(text)
        self.assertEqual(preamble, "Intro\n")
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].heading, "Section A")
        self.assertEqual(sections[0].content, "\nContent A\n")
        self.assertEqual(sections[1].heading, "Section B")
        self.assertEqual(sections[1].content, "\nContent B")

    def test_no_preamble(self):
        text = "== فقط ==\nBody"
        preamble, sections = split_sections(text)
        self.assertEqual(preamble, "")
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].heading, "فقط")
        self.assertEqual(sections[0].content, "\nBody")

    def test_level_three_headings_ignored(self):
        text = "=== مستوى ثالث ===\nskip me"
        preamble, sections = split_sections(text)
        self.assertEqual(preamble, text)
        self.assertEqual(sections, [])

    def test_no_headings(self):
        text = "Text without headings"
        preamble, sections = split_sections(text)
        self.assertEqual(preamble, text)
        self.assertEqual(sections, [])

    def test_empty_text(self):
        self.assertEqual(split_sections(""), ("", []))

    def test_nested_level_three_is_content(self):
        text = "== a ==\n1\n=== sub ===\nsubbody\n== b ==\n2"
        preamble, sections = split_sections(text)
        self.assertEqual(preamble, "")
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].content, "\n1\n=== sub ===\nsubbody\n")

    def test_heading_without_spaces(self):
        text = "==أرشفة==\nno spaces"
        _, sections = split_sections(text)
        self.assertEqual(sections[0].heading, "أرشفة")
        self.assertEqual(sections[0].heading_markup, "==أرشفة==")

    def test_duplicate_headings(self):
        text = "== a ==\n1\n== a ==\n2\n== a ==\n3\n"
        _, sections = split_sections(text)
        self.assertEqual([s.heading for s in sections], ["a", "a", "a"])
        self.assertEqual(len(sections), 3)

    def test_trailing_text_not_a_heading(self):
        text = "Preamble\n== a == trailing\ncontent\n"
        preamble, sections = split_sections(text)
        self.assertEqual(preamble, text)
        self.assertEqual(sections, [])

    def test_roundtrip_preserves_text(self):
        text = "Intro\n== A ==\nBody A\n== B ==\nBody B"
        preamble, sections = split_sections(text)
        rebuilt = preamble + "".join(s.to_wikitext() for s in sections)
        self.assertEqual(rebuilt, text)

    def test_heading_markup_preserved(self):
        text = "==  عنوان  ==\nBody"
        _, sections = split_sections(text)
        self.assertEqual(sections[0].heading, "عنوان")
        self.assertEqual(sections[0].heading_markup, "==  عنوان  ==")
        self.assertEqual(sections[0].to_wikitext(), text)


if __name__ == "__main__":
    unittest.main()
