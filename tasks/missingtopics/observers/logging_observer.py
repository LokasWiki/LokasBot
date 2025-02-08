import logging
from entities.topic_entity import Topic
from use_cases.update_missing_topics import UpdateObserver

class LoggingObserver(UpdateObserver):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def on_topic_start(self, topic: Topic):
        self.logger.info(f"Starting to process topic: {topic.name}")
        
    def on_topic_complete(self, topic: Topic):
        self.logger.info(
            f"Completed processing topic: {topic.name}. "
            f"Found {len(topic.missing_articles)} missing articles."
        )
        
    def on_topic_error(self, topic: Topic, error: Exception):
        self.logger.error(
            f"Error processing topic {topic.name}: {str(error)}",
            exc_info=True
        ) 