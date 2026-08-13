"""Configuration for the archive_bot task."""

import json
import logging
import os
from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class ArchiveBotConfig:
    """Configuration values for the archive_bot task."""

    site_code: str = "ar"
    site_family: str = "wikipedia"
    #: Template name as it appears in wikitext.
    template_name: str = "أرشفة آلية"
    #: Template page title used for the transclusion lookup.
    template_title: str = "قالب:أرشفة آلية"
    #: Namespace to scan (3 = User talk).
    namespace: int = 3
    #: Minimum number of threads that must remain on the page.
    min_threads_left: int = 0
    #: Maximum number of threads to keep (0 = unlimited).
    max_threads: int = 0
    #: Maximum number of bytes to keep (0 = unlimited).
    max_bytes: int = 0
    #: Archive page byte size above which a new archive is started.
    max_archive_size: int = 100000
    #: Archive page byte size above which a new archive is started (total).
    max_archive_total_size: int = 990000
    #: Maximum number of revisions to walk when locating the old snapshot.
    max_history: int = 5000
    #: Seconds to sleep between processed pages.
    sleep_between_pages: float = 3.0


def load_config(path: Optional[str] = None) -> ArchiveBotConfig:
    """Load configuration from a JSON file if present, else use defaults.

    Args:
        path: Path to a ``settings.json``; defaults to the file next to this
            module.

    Returns:
        An :class:`ArchiveBotConfig` instance.
    """
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "settings.json")

    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
            valid = {field.name for field in fields(ArchiveBotConfig)}
            filtered = {key: value for key, value in data.items() if key in valid}
            return ArchiveBotConfig(**filtered)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            logging.warning("Failed to load %s: %s", path, exc)

    return ArchiveBotConfig()
