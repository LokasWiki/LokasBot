from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional
from urllib.parse import urlencode

import pymysql
import requests
import wikitextparser as wtp
from pywikibot import config as _config
from pymysql.converters import escape_string

from core.utils.wikidb import Database
from entities.topic_entity import Article

@dataclass
class MissingTopicsConfig:
    """Configuration for missing topics API"""
    base_url: str = "https://missingtopics.toolforge.org/"
    language: str = "ar"
    project: str = "wikipedia"
    depth: int = 1
    wikimode: int = 1
    nosingles: int = 1
    limitnum: int = 1

class ArticleRepository(ABC):
    @abstractmethod
    def get_missing_articles(self, topic_name: str) -> List[Article]:
        pass

    @abstractmethod
    def get_english_versions(self, titles: List[str]) -> Dict[str, str]:
        pass

class WikiArticleRepository(ArticleRepository):
    def __init__(self, config: Optional[MissingTopicsConfig] = None):
        self.config = config or MissingTopicsConfig()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def get_missing_articles(self, topic_name: str) -> List[Article]:
        """
        Fetches missing articles for a given topic from the MissingTopics API.
        
        Args:
            topic_name: The topic to fetch missing articles for
            
        Returns:
            List of Article entities
            
        Raises:
            Exception: If the API request fails
        """
        response = self._fetch_missing_topics_data(topic_name)
        return self._parse_missing_topics_response(response)

    def get_english_versions(self, titles: List[str]) -> Dict[str, str]:
        """
        Fetches English versions of articles from Wikipedia database.
        
        Args:
            titles: List of article titles to look up
            
        Returns:
            Dictionary mapping article titles to their English versions
        """
        if not titles:
            return {}
            
        with self._get_enwiki_db_connection() as en_db:
            return self._query_english_titles(en_db, titles)

    def _fetch_missing_topics_data(self, topic_name: str) -> str:
        """Makes HTTP request to MissingTopics API"""
        params = {
            "language": self.config.language,
            "project": self.config.project,
            "article": "",
            "category": topic_name,
            "depth": self.config.depth,
            "wikimode": self.config.wikimode,
            "nosingles": self.config.nosingles,
            "limitnum": self.config.limitnum,
            "doit": "Run"
        }
        
        url = f"{self.config.base_url}?{urlencode(params)}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data for topic {topic_name}")
            
        return response.text

    def _parse_missing_topics_response(self, response_text: str) -> List[Article]:
        """Parses API response into Article entities"""
        parsed = wtp.parse(response_text)
        data = parsed.tables[0].data()[1:1001]
        
        return [
            Article(
                title=row[1],
                link_count=int(row[0])
            )
            for row in data
        ]

    def _get_enwiki_db_connection(self) -> Database:
        """Creates connection to English Wikipedia database"""
        en_db = Database()
        en_db.connection = pymysql.connect(
            host=_config.db_hostname_format.format("arwiki"),
            read_default_file=_config.db_connect_file,
            db=_config.db_name_format.format("arwiki"),
            charset='utf8mb4',
            port=_config.db_port,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return en_db

    def _query_english_titles(self, db: Database, titles: List[str]) -> Dict[str, str]:
        """Queries database for English article titles"""
        escaped_titles = [escape_string(title) for title in titles]
        titles_string = ','.join(["'" + title + "'" for title in escaped_titles])
        
        db.query = f"""
        SELECT page.page_title as 'p_title' 
        FROM page 
        WHERE page.page_title IN ({titles_string}) 
        AND page.page_namespace = 0
        """
        db.get_content_from_database()
        
        return {
            title: str(row['p_title'], 'utf-8')
            for row in db.result
            for title in titles
            if str(row['p_title'], 'utf-8') == title
        } 