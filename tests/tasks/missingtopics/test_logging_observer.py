import pytest
from unittest.mock import Mock, patch
import logging

from tasks.missingtopics.entities.topic_entity import Topic, Article
from tasks.missingtopics.observers.logging_observer import LoggingObserver

@pytest.fixture
def mock_topic():
    return Topic(
        name="Science",
        page_name="Wikipedia:Science",
        missing_articles=[
            Article(title="Article 1", link_count=5),
            Article(title="Article 2", link_count=10)
        ]
    )

class TestLoggingObserver:
    @patch('logging.Logger.info')
    def test_on_topic_start(self, mock_info):
        # Arrange
        observer = LoggingObserver()
        topic = Topic(name="Science", page_name="Test", missing_articles=[])

        # Act
        observer.on_topic_start(topic)

        # Assert
        mock_info.assert_called_once_with("Starting to process topic: Science")

    @patch('logging.Logger.info')
    def test_on_topic_complete(self, mock_info, mock_topic):
        # Arrange
        observer = LoggingObserver()

        # Act
        observer.on_topic_complete(mock_topic)

        # Assert
        mock_info.assert_called_once_with(
            "Completed processing topic: Science. Found 2 missing articles."
        )

    @patch('logging.Logger.error')
    def test_on_topic_error(self, mock_error):
        # Arrange
        observer = LoggingObserver()
        topic = Topic(name="Science", page_name="Test", missing_articles=[])
        error = Exception("Test error")

        # Act
        observer.on_topic_error(topic, error)

        # Assert
        mock_error.assert_called_once_with(
            "Error processing topic Science: Test error",
            exc_info=True
        )

    def test_observer_integration(self):
        # Arrange
        observer = LoggingObserver()
        topic = Topic(name="Science", page_name="Test", missing_articles=[])
        
        # Configure logging to use a StringIO object
        import io
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        observer.logger.addHandler(handler)
        observer.logger.setLevel(logging.INFO)

        # Act
        observer.on_topic_start(topic)
        observer.on_topic_complete(topic)
        observer.on_topic_error(topic, Exception("Test error"))

        # Assert
        log_output = log_stream.getvalue()
        assert "Starting to process topic: Science" in log_output
        assert "Completed processing topic: Science" in log_output
        assert "Error processing topic Science: Test error" in log_output 