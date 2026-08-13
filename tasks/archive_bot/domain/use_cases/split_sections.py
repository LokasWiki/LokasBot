"""Split wikitext into a preamble and level-N sections.

This is a faithful but cleaner port of the legacy PHP ``splitintosections``
helper (``script/Lib2.php`` of the archived PHP bot).
"""

import re
from typing import List, Tuple

from tasks.archive_bot.domain.entities.section import Section


def split_sections(text: str, level: int = 2) -> Tuple[str, List[Section]]:
    """Split ``text`` into a preamble and a list of level-``level`` sections.

    A heading line must start with exactly ``level`` ``=`` characters (not
    followed by another ``=``) and end with exactly ``level`` ``=`` characters
    (not preceded by another ``=``), e.g. ``== عنوان ==`` for ``level == 2``.
    Everything before the first heading is returned as the preamble; each
    heading plus its trailing content (up to the next heading or EOF) becomes
    a :class:`Section`.

    Args:
        text: The wikitext to split.
        level: The heading level to split on (default 2).

    Returns:
        A tuple ``(preamble, sections)``.
    """
    if not text:
        return "", []

    marker = "=" * level
    # A heading occupies a full line: exactly `level` '=' at the start (not
    # followed by '='), any text, then exactly `level` '=' at the end (not
    # preceded by '='), optionally followed by trailing spaces/tabs.
    pattern = re.compile(
        rf"^{re.escape(marker)}(?!=)(?P<head>.*?)(?<!=){re.escape(marker)}"
        r"[ \t]*(?=\n|$)",
        re.MULTILINE,
    )

    matches = list(pattern.finditer(text))
    if not matches:
        return text, []

    preamble = text[: matches[0].start()]
    sections: List[Section] = []

    for index, match in enumerate(matches):
        heading = match.group("head").strip()
        heading_markup = match.group(0).rstrip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(
            Section(heading=heading, content=text[start:end],
                    heading_markup=heading_markup)
        )

    return preamble, sections
