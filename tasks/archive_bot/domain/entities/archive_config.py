"""Domain entity representing a parsed ``{{أرشفة آلية}}`` configuration."""

from dataclasses import dataclass

#: Archive by age (value = days).
AGE_MODE = "قسم"
#: Archive by size (value = kilobytes).
SIZE_MODE = "حجم"


@dataclass(frozen=True)
class ArchiveConfig:
    """Parsed configuration from a ``{{أرشفة آلية}}`` template.

    The template is invoked on Arabic Wikipedia as::

        {{أرشفة آلية|قسم|10|نقاش المستخدم:Example/أرشيف 6}}

    Attributes:
        archive_type: ``قسم`` (archive by age) or ``حجم`` (archive by size).
        value: Days (age mode) or kilobytes (size mode).
        base_prefix: Archive page prefix without the trailing counter,
            e.g. ``نقاش المستخدم:Example/أرشيف``.
        counter: Current archive counter (0 when not specified).
    """

    archive_type: str
    value: int
    base_prefix: str
    counter: int = 0

    @property
    def is_age_mode(self) -> bool:
        """Return True when archiving by age (``قسم``)."""
        return self.archive_type == AGE_MODE

    @property
    def age_hours(self) -> int:
        """Return the age threshold in hours.

        Age mode uses ``value`` days; size mode archives threads that have
        been unchanged for at least one hour.
        """
        return self.value * 24 if self.is_age_mode else 1

    @property
    def size_threshold_bytes(self) -> int:
        """Return the page-size threshold in bytes (size mode only)."""
        return self.value * 1000
