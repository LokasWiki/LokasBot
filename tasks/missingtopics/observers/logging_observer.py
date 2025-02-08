import logging
from typing import List, Dict, Any

from tasks.missingtopics.entities.topic_entity import Topic
from tasks.missingtopics.observers.observer_protocol import UpdateObserver

class LoggingObserver(UpdateObserver):
    def __init__(self):
        self.logger = logging.getLogger('tasks.missingtopics.observer')
        
    def on_topic_start(self, topic: Topic):
        self.logger.info(f"Starting to process topic: {topic.name}")
        
    def on_topic_complete(self, topic: Topic):
        self.logger.info(f"Completed processing topic: {topic.name}")
        self.logger.info(f"Found {len(topic.missing_articles)} missing articles")
        
    def on_topic_error(self, topic: Topic, error: Exception):
        self.logger.error(f"Error processing topic {topic.name}: {str(error)}", exc_info=True)
        
    def on_batch_start(self, topic: Topic, batch_number: int, batch_size: int):
        self.logger.info(f"Starting batch {batch_number} for topic {topic.name} with {batch_size} articles")
        
    def on_batch_complete(
        self,
        topic: Topic,
        batch_number: int,
        batch_size: int,
        new_en_count: int,
        new_desc_count: int
    ):
        self.logger.info(
            f"Completed batch {batch_number} for topic {topic.name}. "
            f"Added {new_en_count} English versions and {new_desc_count} descriptions"
        )
        
    def on_wikidata_lookup(self, en_titles: List[str]):
        self.logger.info(f"Looking up Wikidata descriptions for {len(en_titles)} articles")
        
    def on_wikidata_result(self, found_count: int, total_count: int):
        self.logger.info(f"Found {found_count} descriptions out of {total_count} articles")
        
    def on_api_request(self, host: str, params: Dict[str, Any]):
        self.logger.debug(f"Making API request to {host} with params: {params}")
        
    def on_api_response(self, host: str, status_code: int, success: bool):
        if success:
            self.logger.debug(f"Successful API response from {host} with status {status_code}")
        else:
            self.logger.warning(f"Failed API response from {host} with status {status_code}")
            
    def on_db_query(self, query: str):
        self.logger.debug(f"Executing database query: {query}")
        
    def on_db_result(self, result_count: int):
        self.logger.debug(f"Database query returned {result_count} results") 