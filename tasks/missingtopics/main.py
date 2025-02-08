import logging

from tasks.missingtopics.observers.logging_observer import LoggingObserver
from tasks.missingtopics.repositories.article_repository import WikiArticleRepository
from tasks.missingtopics.repositories.topic_repository import WikiTopicRepository
from tasks.missingtopics.use_cases.update_missing_topics import UpdateMissingTopicsUseCase

def setup_logging():
    # Clear any existing handlers
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
            
    # Configure logging with a stream handler for console output
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # This ensures output goes to console
        ]
    )
    
    # Set logging level for specific loggers
    logging.getLogger('tasks.missingtopics').setLevel(logging.INFO)
    logging.getLogger('pywikibot').setLevel(logging.WARNING)  # Reduce noise from pywikibot

def main():
    setup_logging()
    
    # Initialize repositories
    topic_repository = WikiTopicRepository()
    article_repository = WikiArticleRepository()
    
    # Create use case
    use_case = UpdateMissingTopicsUseCase(
        topic_repository=topic_repository,
        article_repository=article_repository
    )
    
    # Add observers
    use_case.add_observer(LoggingObserver())
    
    # Execute the use case
    use_case.execute()

if __name__ == "__main__":
    main() 