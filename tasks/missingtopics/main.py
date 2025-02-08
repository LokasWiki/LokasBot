import logging

from observers.logging_observer import LoggingObserver
from repositories.article_repository import WikiArticleRepository
from repositories.topic_repository import WikiTopicRepository
from use_cases.update_missing_topics import UpdateMissingTopicsUseCase

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

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