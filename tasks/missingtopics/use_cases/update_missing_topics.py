import re
import time
from typing import List, Protocol

from entities.topic_entity import Topic, Article
from repositories.article_repository import ArticleRepository
from repositories.topic_repository import TopicRepository

class UpdateObserver(Protocol):
    def on_topic_start(self, topic: Topic):
        pass
        
    def on_topic_complete(self, topic: Topic):
        pass
        
    def on_topic_error(self, topic: Topic, error: Exception):
        pass

class UpdateMissingTopicsUseCase:
    def __init__(
        self,
        topic_repository: TopicRepository,
        article_repository: ArticleRepository,
        batch_size: int = 50,
        delay_seconds: int = 3
    ):
        self.topic_repository = topic_repository
        self.article_repository = article_repository
        self.batch_size = batch_size
        self.delay_seconds = delay_seconds
        self.observers: List[UpdateObserver] = []
        
    def add_observer(self, observer: UpdateObserver):
        self.observers.append(observer)
        
    def execute(self):
        topics = self.topic_repository.get_all_topics()
        for topic in topics:
            self._process_topic(topic)
            
    def _process_topic(self, topic: Topic):
        try:
            for observer in self.observers:
                observer.on_topic_start(topic)
                
            # Get missing articles for the topic
            articles = self.article_repository.get_missing_articles(topic.name)
            
            # Process articles in batches
            for i in range(0, len(articles), self.batch_size):
                batch = articles[i:i + self.batch_size]
                self._process_article_batch(batch)
                time.sleep(self.delay_seconds)
                
            topic.missing_articles = articles
            self._update_topic_page(topic)
            
            for observer in self.observers:
                observer.on_topic_complete(topic)
                
        except Exception as e:
            for observer in self.observers:
                observer.on_topic_error(topic, e)
    
    def _process_article_batch(self, articles: List[Article]):
        # Filter non-Arabic titles and prepare for English lookup
        valid_titles = []
        for article in articles:
            title = article.title.replace(" ", "_").replace("[[", "").replace("]]", "")
            if not self._has_arabic_chars(title) and len(title) <= 100:
                valid_titles.append(title)
        
        # Get English versions
        en_titles = self.article_repository.get_english_versions(valid_titles)
        
        # Update articles with English versions
        for article in articles:
            title = article.title.replace(" ", "_").replace("[[", "").replace("]]", "")
            if title in en_titles:
                article.en_title = en_titles[title]
    
    def _update_topic_page(self, topic: Topic):
        content = self._generate_page_content(topic)
        self.topic_repository.save_topic_page(topic, content)
    
    def _generate_page_content(self, topic: Topic) -> str:
        table_rows = []
        for i, article in enumerate(topic.missing_articles, 1):
            table_rows.append(f"""|-
            |{i}
            |{article.link_count}
            |{article.format_wiki_link()}
            |{article.format_en_wiki_link()}""")
            
        return f"""<center>
<div style="background: #E5E4E2; padding: 0.5em; font-family: Traditional Arabic; font-size: 130%;  -moz-border-radius: 0.3em; border-radius: 0.3em;">
تعرض هذه الصفحة قائمة وصلات حمراء مطلوبة حسب الموضوع ([[{topic.name}]]).<br/>
</div>
</center>
<center>
<div style="background: #E5E4E2; padding: 0.5em;   -moz-border-radius: 0.3em; border-radius: 0.3em;">
{{| class="wikitable sortable"
!style="background-color:#808080" align="center"|#
!style="background-color:#808080" align="center"|عدد الوصلات
!style="background-color:#808080" align="center"|اسم المقال
!style="background-color:#808080" align="center"|المقالة المقابلة في لغة أخرى
{''.join(table_rows)}
|}}
</div>
</center>"""
    
    @staticmethod
    def _has_arabic_chars(text: str) -> bool:
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')
        return bool(arabic_pattern.search(text)) 