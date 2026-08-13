"""Use case orchestrating the archiving of a single discussion page.

This ports the legacy PHP ``doarchive`` function (``script/Lib2.php``) into
the project's clean-architecture style.
"""

import datetime
import logging
import re
from typing import List, Tuple

import wikitextparser as wtp

from tasks.archive_bot.config.config_loader import ArchiveBotConfig
from tasks.archive_bot.domain.entities.archive_config import ArchiveConfig
from tasks.archive_bot.domain.entities.archive_result import ArchiveResult
from tasks.archive_bot.domain.entities.section import Section
from tasks.archive_bot.domain.repositories.wiki_repository import WikiRepository
from tasks.archive_bot.domain.use_cases.decide_archive import classify
from tasks.archive_bot.domain.use_cases.parse_archive_config import (
    ParseArchiveConfig,
)
from tasks.archive_bot.domain.use_cases.split_sections import split_sections


class ArchivePage:
    """Orchestrate the archiving of one discussion page."""

    def __init__(self, wiki_repository: WikiRepository,
                 config: ArchiveBotConfig):
        self.repository = wiki_repository
        self.config = config
        self.parser = ParseArchiveConfig(config.template_name)
        self.logger = logging.getLogger(__name__)

    def execute(self, page_title: str, dry_run: bool = False) -> ArchiveResult:
        """Archive old threads from ``page_title``.

        Args:
            page_title: The talk page to process.
            dry_run: When True, compute everything but do not save.

        Returns:
            An :class:`ArchiveResult` describing the outcome.
        """
        result = ArchiveResult(page_title=page_title)

        text = self.repository.get_page_text(page_title)
        if not text.strip():
            result.reason = "empty or missing page"
            return result

        config = self.parser.parse(text)
        if config is None:
            result.reason = f"no {self.config.template_name} template"
            return result

        # Size mode: only archive once the page exceeds the threshold.
        if not config.is_age_mode:
            page_size = len(text.encode("utf-8"))
            if page_size < config.size_threshold_bytes:
                result.reason = (
                    f"page size {page_size} below threshold "
                    f"{config.size_threshold_bytes}"
                )
                return result

        preamble, current_sections = self._split(text)
        if not current_sections:
            result.reason = "no level-2 sections"
            return result

        cutoff = (
            datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            - datetime.timedelta(hours=config.age_hours)
        )
        old_text = self.repository.get_old_text(page_title, cutoff)
        if old_text is None:
            result.reason = "no revision older than the age threshold"
            return result

        _, old_sections = self._split(old_text)
        keep, archive = classify(
            current_sections,
            old_sections,
            min_threads_left=self.config.min_threads_left,
            max_threads=self.config.max_threads,
            max_bytes=self.config.max_bytes,
        )
        if not archive:
            result.reason = "no sections to archive"
            return result

        counter, archive_title = self._resolve_archive_title(config)
        existing_archive = self.repository.get_page_text(archive_title)
        archive_text = self._assemble_archive_text(existing_archive, counter, archive)

        # If the target archive is too large, roll over to a fresh one.
        if existing_archive.strip() and (
            len(existing_archive.encode("utf-8")) >= self.config.max_archive_size
            or len(archive_text.encode("utf-8")) >= self.config.max_archive_total_size
        ):
            counter += 1
            archive_title = f"{config.base_prefix} {counter}"
            existing_archive = self.repository.get_page_text(archive_title)
            archive_text = self._assemble_archive_text(existing_archive, counter,
                                                       archive)

        new_page_text = self._build_page_text(preamble, keep, counter)

        result.archived_count = len(archive)
        result.kept_count = len(keep)
        result.archive_title = archive_title
        result.new_counter = counter
        result.new_page_text = new_page_text
        result.new_archive_text = archive_text

        if dry_run:
            result.status = "dry_run"
            return result

        archive_summary = self._archive_summary(page_title, archive_title, len(archive))
        page_summary = self._page_summary(page_title, archive_title, len(archive))

        if not self.repository.save_page(archive_title, archive_text, archive_summary):
            result.status = "failed"
            result.reason = "failed to save archive page"
            return result

        if not self.repository.save_page(page_title, new_page_text, page_summary):
            # Roll back the archive edit to keep the two pages consistent.
            rollback_summary = (
                f"الغاء أرشفة {self._count_label(len(archive))} من "
                f"[[{archive_title}]]. (Archive failed)"
            )
            self.repository.save_page(archive_title, existing_archive,
                                      rollback_summary)
            result.status = "failed"
            result.reason = "failed to save page; archive rolled back"
            return result

        result.status = "archived"
        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _split(text: str) -> Tuple[str, List[Section]]:
        return split_sections(text, level=2)

    def _resolve_archive_title(self, config: ArchiveConfig) -> Tuple[int, str]:
        """Return ``(counter, archive_title)`` for the current archive."""
        counters = self.repository.list_archive_counters(config.base_prefix)
        max_existing = max(counters) if counters else 0
        counter = config.counter if config.counter > 0 else (max_existing or 1)
        return counter, f"{config.base_prefix} {counter}"

    def _assemble_archive_text(self, existing: str, counter: int,
                               sections: List[Section]) -> str:
        body = "".join(section.to_wikitext() for section in sections)
        if existing.strip():
            return existing.rstrip() + "\n" + body
        return self._archive_header(counter) + body

    def _archive_header(self, counter: int) -> str:
        return (
            f"{{{{تصفح أرشيف|{counter}}}}}\n"
            "{{تمت الأرشفة}}\n"
            "{{أرشيف صفحة رئيسية}}\n"
        )

    def _build_page_text(self, preamble: str, keep: List[Section],
                         counter: int) -> str:
        body = "".join(section.to_wikitext() for section in keep)
        return self._update_template_counter(preamble + body, counter)

    def _update_template_counter(self, text: str, counter: int) -> str:
        """Rewrite the trailing archive counter inside the config template."""
        parsed = wtp.parse(text)
        replacements = []
        for template in parsed.templates:
            if self._normalize(template.name) != self._normalize(
                    self.config.template_name):
                continue
            new_raw = self._rewrite_counter(template.string, counter)
            replacements.append((template.span[0], template.span[1], new_raw))

        for start, end, new_raw in reversed(replacements):
            text = text[:start] + new_raw + text[end:]
        return text

    @staticmethod
    def _normalize(name: str) -> str:
        return name.strip().replace("_", " ").lower()

    @staticmethod
    def _rewrite_counter(raw_template: str, counter: int) -> str:
        """Replace the trailing counter inside a raw template string."""
        match = re.search(r"(\d+)\s*\}\}\s*$", raw_template)
        if match:
            return (raw_template[: match.start(1)] + str(counter)
                    + raw_template[match.end(1):])
        # No counter present: insert one before the closing braces.
        return re.sub(r"(\s*)(\}\}\s*)$",
                      lambda found: f" {counter}{found.group(2)}", raw_template)

    @staticmethod
    def _count_label(count: int) -> str:
        """Return the Arabic plural label used in edit summaries."""
        if count == 1:
            return "نقاش واحد"
        if count == 2:
            return "نقاشان"
        if 2 < count <= 10:
            return f"{count} نقاشات"
        return f"{count} نقاش"

    def _archive_summary(self, page_title: str, archive_title: str,
                         count: int) -> str:
        return f"أرشفة {self._count_label(count)} من [[{page_title}]]"

    def _page_summary(self, page_title: str, archive_title: str,
                      count: int) -> str:
        return f"أرشفة {self._count_label(count)} إلى [[{archive_title}]]"
