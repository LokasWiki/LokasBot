"""Tests for the ArchivePage orchestration use case."""

import datetime
import unittest

from tasks.archive_bot.config.config_loader import ArchiveBotConfig
from tasks.archive_bot.domain.repositories.wiki_repository import WikiRepository
from tasks.archive_bot.domain.use_cases.archive_page import ArchivePage


class FakeRepository(WikiRepository):
    """In-memory repository for testing the archive use case."""

    def __init__(self):
        self.pages = {}          # title -> text
        self.revisions = {}      # title -> list[(timestamp, text)] newest first
        self.protected = set()   # sysop-protected titles
        self.fail_saves = set()  # titles whose save() fails
        self.saves = []          # (title, text, summary)

    def get_page_text(self, title):
        return self.pages.get(title, "")

    def page_exists(self, title):
        return title in self.pages

    def save_page(self, title, text, summary):
        if title in self.fail_saves:
            return False
        self.saves.append((title, text, summary))
        self.pages[title] = text
        return True

    def get_old_text(self, title, cutoff):
        for timestamp, text in self.revisions.get(title, []):
            if timestamp <= cutoff:
                return text
        return None

    def is_sysop_protected(self, title):
        return title in self.protected

    def list_archive_counters(self, base_prefix):
        counters = []
        for title in self.pages:
            if title.startswith(base_prefix + " "):
                suffix = title[len(base_prefix):].strip()
                if suffix.isdigit():
                    counters.append(int(suffix))
        return counters

    def get_transcluded_pages(self, template_title, namespace):
        return list(self.pages)


def make_config(**overrides):
    defaults = {
        "site_code": "ar",
        "site_family": "wikipedia",
        "template_name": "أرشفة آلية",
        "template_title": "قالب:أرشفة آلية",
        "namespace": 3,
    }
    defaults.update(overrides)
    return ArchiveBotConfig(**defaults)


class TestArchivePage(unittest.TestCase):
    """Tests for :class:`ArchivePage`."""

    def _age_mode_setup(self):
        repo = FakeRepository()
        page = "نقاش المستخدم:X"
        tpl = "{{أرشفة آلية|قسم|10|نقاش المستخدم:X/أرشيف 1}}"
        old_text = tpl + "\n\n== قديم ==\nنقاش قديم\n"
        new_text = tpl + "\n\n== قديم ==\nنقاش قديم\n\n== جديد ==\nنقاش جديد\n"
        repo.pages[page] = new_text
        now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        repo.revisions[page] = [
            (now - datetime.timedelta(hours=1), new_text),
            (now - datetime.timedelta(days=20), old_text),
        ]
        use_case = ArchivePage(repo, make_config())
        return repo, use_case, page

    def test_age_mode_archives_unchanged_section(self):
        repo, use_case, page = self._age_mode_setup()
        result = use_case.execute(page)

        self.assertEqual(result.status, "archived")
        self.assertEqual(result.archived_count, 1)
        self.assertEqual(result.kept_count, 1)
        self.assertEqual(result.archive_title, "نقاش المستخدم:X/أرشيف 1")

        archive_text = repo.pages["نقاش المستخدم:X/أرشيف 1"]
        self.assertIn("{{تصفح أرشيف|1}}", archive_text)
        self.assertIn("== قديم ==", archive_text)
        self.assertNotIn("== جديد ==", archive_text)

        page_text = repo.pages[page]
        self.assertIn("== جديد ==", page_text)
        self.assertNotIn("== قديم ==", page_text)

    def test_size_mode_below_threshold_skipped(self):
        repo = FakeRepository()
        page = "نقاش المستخدم:X"
        repo.pages[page] = (
            "{{أرشفة آلية|حجم|100|نقاش المستخدم:X/أرشيف 1}}\n"
            "== قديم ==\nنقاش\n"
        )
        use_case = ArchivePage(repo, make_config())
        result = use_case.execute(page)
        self.assertEqual(result.status, "skipped")
        self.assertIn("below threshold", result.reason)
        self.assertEqual(repo.saves, [])

    def test_dry_run_does_not_save(self):
        repo, use_case, page = self._age_mode_setup()
        result = use_case.execute(page, dry_run=True)

        self.assertEqual(result.status, "dry_run")
        self.assertEqual(result.archived_count, 1)
        self.assertEqual(repo.saves, [])
        # Page and archive remain untouched.
        self.assertNotIn("نقاش المستخدم:X/أرشيف 1", repo.pages)

    def test_no_template_skipped(self):
        repo = FakeRepository()
        page = "نقاش المستخدم:X"
        repo.pages[page] = "== قسم ==\nنقاش بلا قالب\n"
        use_case = ArchivePage(repo, make_config())
        result = use_case.execute(page)
        self.assertEqual(result.status, "skipped")
        self.assertIn("no", result.reason)

    def test_rollback_on_page_save_failure(self):
        repo, use_case, page = self._age_mode_setup()
        repo.fail_saves.add(page)

        result = use_case.execute(page)

        self.assertEqual(result.status, "failed")
        self.assertIn("rolled back", result.reason)
        # Archive was first written, then rolled back to empty.
        archive_title = "نقاش المستخدم:X/أرشيف 1"
        self.assertEqual(repo.pages[archive_title], "")

    def test_rollover_to_new_counter_when_archive_full(self):
        repo, use_case, page = self._age_mode_setup()
        # Make the target archive too large to force a new counter.
        repo.pages["نقاش المستخدم:X/أرشيف 1"] = "X" * 50
        use_case.config.max_archive_size = 10
        use_case.config.max_archive_total_size = 20

        result = use_case.execute(page)

        self.assertEqual(result.status, "archived")
        self.assertEqual(result.archive_title, "نقاش المستخدم:X/أرشيف 2")
        self.assertEqual(result.new_counter, 2)
        self.assertIn("{{تصفح أرشيف|2}}",
                      repo.pages["نقاش المستخدم:X/أرشيف 2"])
        # The page template counter was updated to 2.
        self.assertIn("نقاش المستخدم:X/أرشيف 2", repo.pages[page])


if __name__ == "__main__":
    unittest.main()
