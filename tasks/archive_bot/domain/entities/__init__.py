"""Domain entities for the archive_bot task."""

from tasks.archive_bot.domain.entities.archive_config import ArchiveConfig
from tasks.archive_bot.domain.entities.archive_result import ArchiveResult
from tasks.archive_bot.domain.entities.section import Section

__all__ = ["ArchiveConfig", "ArchiveResult", "Section"]
