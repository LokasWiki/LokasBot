from abc import ABC, abstractmethod
from typing import List

import pywikibot
from core.utils.wikidb import Database
from entities.topic_entity import Topic, Article

class TopicRepository(ABC):
    @abstractmethod
    def get_all_topics(self) -> List[Topic]:
        pass

    @abstractmethod
    def save_topic_page(self, topic: Topic, content: str):
        pass

class WikiTopicRepository(TopicRepository):
    def __init__(self):
        self.site = pywikibot.Site()
        self.db = Database()

    def get_all_topics(self) -> List[Topic]:
        self.db.query = """
        select replace(lt_title,"مقالات_مطلوبة_حسب_الاختصاص/","") as page_title 
        from pagelinks 
        inner join linktarget on linktarget.lt_id = pagelinks.pl_target_id
        where pl_from in (676775)
        and lt_namespace in (4)
        and pl_from_namespace in (4)
        and lt_title not like "%وصلة_حمراء%"
        order by lt_title
        """
        self.db.get_content_from_database()
        
        topics = []
        for row in self.db.result:
            name = str(row['page_title'], "utf-8").replace("_", " ")
            topics.append(Topic(
                name=name,
                page_name=f"ويكيبيديا:مقالات مطلوبة حسب الاختصاص/{name}",
                missing_articles=[]
            ))
        return topics

    def save_topic_page(self, topic: Topic, content: str):
        page = pywikibot.Page(self.site, topic.page_name)
        page.text = content
        page.save("بوت:تحديث مقالات مطلوبة حسب الاختصاص v3.2.0") 