import re
import time
from typing import List

from tasks.missingtopics.entities.topic_entity import Topic, Article
from tasks.missingtopics.repositories.article_repository import ArticleRepository
from tasks.missingtopics.repositories.topic_repository import TopicRepository
from tasks.missingtopics.observers.observer_protocol import UpdateObserver

class UpdateMissingTopicsUseCase:
    def __init__(
        self,
        topic_repository: TopicRepository,
        article_repository: ArticleRepository,
        bot_name: str = "LokasBot",
        batch_size: int = 50,
        delay_seconds: int = 3
    ):
        self.topic_repository = topic_repository
        self.article_repository = article_repository
        self.bot_name = bot_name
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
            batch_number = 1
            for i in range(0, len(articles), self.batch_size):
                batch = articles[i:i + self.batch_size]
                
                for observer in self.observers:
                    observer.on_batch_start(topic, batch_number, len(batch))
                
                initial_en_count = len([a for a in batch if a.has_english_version])
                initial_desc_count = len([a for a in batch if a.description])
                
                self._process_article_batch(batch)
                
                final_en_count = len([a for a in batch if a.has_english_version])
                final_desc_count = len([a for a in batch if a.description])
                
                for observer in self.observers:
                    observer.on_batch_complete(
                        topic,
                        batch_number,
                        len(batch),
                        final_en_count - initial_en_count,
                        final_desc_count - initial_desc_count
                    )
                
                batch_number += 1
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

        # Get Wikidata descriptions for articles with English versions
        articles_with_en = [article for article in articles if article.has_english_version]
        if articles_with_en:
            en_titles = [article.en_title for article in articles_with_en]
            
            for observer in self.observers:
                observer.on_wikidata_lookup(en_titles)
                
            descriptions = self.article_repository.get_wikidata_descriptions(en_titles)
            
            # Update articles with descriptions
            desc_count = 0
            for article in articles_with_en:
                if article.en_title in descriptions:
                    article.description = descriptions[article.en_title]
                    desc_count += 1
                    
            for observer in self.observers:
                observer.on_wikidata_result(desc_count, len(en_titles))
    
    def _update_topic_page(self, topic: Topic):
        content = self._generate_page_content(topic)
        self.topic_repository.save_topic_page(topic, content)
    
    def _generate_page_content(self, topic: Topic) -> str:
        table_rows = []
        for i, article in enumerate(topic.missing_articles, 1):
            table_rows.append(f"""
            |-
            |{i}
            |{article.link_count}
            |{article.format_wiki_link()}
            |{article.format_en_wiki_link()}
            |{article.format_description()}
            
            """)
            
        return f"""<center>
<div style="background: #E5E4E2; padding: 0.5em; font-family: Traditional Arabic; font-size: 130%;  -moz-border-radius: 0.3em; border-radius: 0.3em;">
تعرض هذه الصفحة قائمة وصلات حمراء مطلوبة حسب الموضوع ([[{topic.name}]]).<br/>
'''حَدَّث [[مستخدم:{self.bot_name}|{self.bot_name}]] هذه القائمة في: {{{{نسخ:#time:H:i، j F Y}}}} (ت ع م)'''
</div>
</center>
<center>
<div style="background: #E5E4E2; padding: 0.5em;   -moz-border-radius: 0.3em; border-radius: 0.3em;">
{{| class="wikitable sortable"
!style="background-color:#808080" align="center"|#
!style="background-color:#808080" align="center"|عدد الوصلات
!style="background-color:#808080" align="center"|اسم المقال
!style="background-color:#808080" align="center"|المقالة المقابلة في لغة أخرى
!style="background-color:#808080" align="center"|الوصف من ويكي بيانات
{''.join(table_rows)}
|}}
</div>
</center>"""
    
    @staticmethod
    def _has_arabic_chars(text: str) -> bool:
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')
        return bool(arabic_pattern.search(text)) 