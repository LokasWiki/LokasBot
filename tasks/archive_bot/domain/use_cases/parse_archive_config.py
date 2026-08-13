"""Parse the ``{{أرشفة آلية}}`` configuration template.

Uses :mod:`wikitextparser` (the project's standard wikitext parsing library)
instead of the fragile ``explode``/regex parsing used by the legacy PHP bot.
"""

import re
from typing import Optional, Tuple

import wikitextparser as wtp

from tasks.archive_bot.domain.entities.archive_config import ArchiveConfig

#: Template name as it appears in wikitext.
TEMPLATE_NAME = "أرشفة آلية"

#: Legacy flag sometimes inserted between the value and the prefix.
LEGACY_FLAGS = {"عددي", "عددى"}

#: Matches the trailing archive counter inside the prefix argument.
_COUNTER_RE = re.compile(r"(\d+)\s*$")


def _normalize(name: str) -> str:
    """Normalize a template name for comparison."""
    return name.strip().replace("_", " ").lower()


class ParseArchiveConfig:
    """Parse an :class:`ArchiveConfig` from page wikitext."""

    def __init__(self, template_name: str = TEMPLATE_NAME):
        self.template_name = _normalize(template_name)

    def parse(self, text: str) -> Optional[ArchiveConfig]:
        """Return the first archive config found in ``text`` or ``None``."""
        if not text:
            return None

        for template in wtp.parse(text).templates:
            if _normalize(template.name) != self.template_name:
                continue
            config = self._parse_template(template)
            if config is not None:
                return config
        return None

    def _parse_template(self, template) -> Optional[ArchiveConfig]:
        """Parse a single ``{{أرشفة آلية}}`` template object."""
        # Collect positional arguments, dropping the legacy 'عددي'/'عددى' flag.
        values = []
        for argument in template.arguments:
            if not argument.positional:
                continue
            value = argument.value.strip()
            if value in LEGACY_FLAGS:
                continue
            values.append(value)

        if len(values) < 3:
            return None

        archive_type = values[0]
        try:
            value = int(values[1])
        except ValueError:
            return None

        base_prefix, counter = self._split_counter(values[2])
        return ArchiveConfig(
            archive_type=archive_type,
            value=value,
            base_prefix=base_prefix,
            counter=counter,
        )

    @staticmethod
    def _split_counter(raw_prefix: str) -> Tuple[str, int]:
        """Split the prefix argument into ``(base_prefix, counter)``.

        The prefix carries the current archive counter as trailing digits,
        e.g. ``نقاش المستخدم:Example/أرشيف 6`` → counter ``6``.
        """
        match = _COUNTER_RE.search(raw_prefix)
        if match:
            return raw_prefix[: match.start()].rstrip(), int(match.group(1))
        return raw_prefix.rstrip(), 0
