from dataclasses import dataclass
from typing import List

@dataclass
class Topic:
    name: str
    page_name: str
    missing_articles: List['Article']

@dataclass
class Article:
    title: str
    link_count: int
    en_title: str = ""

    @property
    def has_english_version(self) -> bool:
        return bool(self.en_title)

    def format_wiki_link(self) -> str:
        return f"{self.title}"

    def format_en_wiki_link(self) -> str:
        return f"[[:en:{self.en_title}]]" if self.has_english_version else "\n" 