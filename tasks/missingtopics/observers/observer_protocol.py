from typing import List, Protocol

from entities.topic_entity import Topic

class UpdateObserver(Protocol):
    def on_topic_start(self, topic: Topic):
        """Called when starting to process a topic"""
        pass
        
    def on_topic_complete(self, topic: Topic):
        """Called when a topic has been completely processed"""
        pass
        
    def on_topic_error(self, topic: Topic, error: Exception):
        """Called when an error occurs while processing a topic"""
        pass
        
    def on_batch_start(self, topic: Topic, batch_number: int, batch_size: int):
        """Called when starting to process a batch of articles"""
        pass
        
    def on_batch_complete(
        self, 
        topic: Topic, 
        batch_number: int,
        processed: int,
        en_found: int,
        desc_found: int
    ):
        """Called when a batch of articles has been processed"""
        pass
        
    def on_api_request(self, endpoint: str, params: dict):
        """Called before making an API request"""
        pass
        
    def on_api_response(self, endpoint: str, status_code: int, success: bool):
        """Called after receiving an API response"""
        pass
        
    def on_db_query(self, query: str):
        """Called before executing a database query"""
        pass
        
    def on_db_result(self, result_count: int):
        """Called after receiving database query results"""
        pass
        
    def on_wikidata_lookup(self, titles: List[str]):
        """Called before looking up Wikidata descriptions"""
        pass
        
    def on_wikidata_result(self, found: int, total: int):
        """Called after retrieving Wikidata descriptions"""
        pass 