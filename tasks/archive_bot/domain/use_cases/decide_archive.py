"""Classify discussion sections into keep vs archive.

Ports the keep/archive decision logic of the legacy PHP ``doarchive``
function (``script/Lib2.php``).
"""

import re
from typing import Dict, List, Tuple

from tasks.archive_bot.domain.entities.section import Section

#: Template that marks a section as not archivable (``{{لا للأرشفة}}``).
DO_NOT_ARCHIVE_RE = re.compile(r"\{\{\s*لا للأرشفة\s*\}\}")


def _keyed_sections(sections: List[Section]) -> List[Tuple[str, Section]]:
    """Assign a unique key to each section, like the PHP splitter.

    Duplicate headings are disambiguated with a numeric suffix (``X``,
    ``X 2``, ``X 3``, ...) so that the same heading in the old and current
    snapshots maps to the same key.
    """
    keyed: List[Tuple[str, Section]] = []
    seen: Dict[str, int] = {}
    for section in sections:
        base = section.heading.strip()
        count = seen.get(base, 0) + 1
        seen[base] = count
        key = base if count == 1 else f"{base} {count}"
        keyed.append((key, section))
    return keyed


def classify(
    current_sections: List[Section],
    old_sections: List[Section],
    min_threads_left: int = 0,
    max_threads: int = 0,
    max_bytes: int = 0,
) -> Tuple[List[Section], List[Section]]:
    """Split ``current_sections`` into ``(keep, archive)`` lists.

    A section is archived when its content is unchanged compared with the
    ``old_sections`` snapshot (i.e. it has had no activity for the age
    threshold). Sections marked with ``{{لا للأرشفة}}`` or that are new
    are always kept.

    Args:
        current_sections: Sections of the current page text.
        old_sections: Sections of the age-threshold snapshot.
        min_threads_left: Minimum number of threads that must remain.
        max_threads: Maximum number of threads to keep (0 = unlimited).
        max_bytes: Maximum number of bytes to keep (0 = unlimited).

    Returns:
        A tuple ``(keep, archive)`` preserving document order.
    """
    old_index: Dict[str, Section] = dict(_keyed_sections(old_sections))
    keep: List[Section] = []
    archive: List[Section] = []

    for key, section in _keyed_sections(current_sections):
        remaining = len(current_sections) - len(archive)
        if remaining <= min_threads_left:
            keep.append(section)
        elif DO_NOT_ARCHIVE_RE.search(section.content):
            keep.append(section)
        elif key not in old_index:
            keep.append(section)
        elif section.content.strip() == old_index[key].content.strip():
            archive.append(section)
        else:
            keep.append(section)

    if max_threads > 0 or max_bytes > 0:
        keep, archive = _enforce_limits(keep, archive, max_threads, max_bytes)

    return keep, archive


def _enforce_limits(
    keep: List[Section],
    archive: List[Section],
    max_threads: int,
    max_bytes: int,
) -> Tuple[List[Section], List[Section]]:
    """Move the oldest excess kept sections to the archive.

    Iterates from newest to oldest so the newest threads remain on the page.
    """
    count = 0
    total_bytes = 0
    new_keep: List[Section] = []
    overflow: List[Section] = []

    for section in reversed(keep):
        count += 1
        total_bytes += len(section.content.encode("utf-8"))
        if (max_threads > 0 and count > max_threads) or (
            max_bytes > 0 and total_bytes > max_bytes
        ):
            overflow.append(section)
        else:
            new_keep.append(section)

    # Restore document order.
    new_keep.reverse()
    overflow.reverse()
    return new_keep, archive + overflow
