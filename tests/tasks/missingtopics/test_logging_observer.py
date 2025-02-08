import pytest
from unittest.mock import Mock, patch
import logging
from io import StringIO

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

@pytest.fixture
def observer():
    return LoggingObserver()

@pytest.fixture
def log_capture():
    # Create a string buffer to capture log output
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Get the logger used by LoggingObserver
    logger = logging.getLogger('tasks.missingtopics.observer')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    yield log_stream
    
    # Cleanup
    logger.removeHandler(handler)
    log_stream.close()

class TestLoggingObserver:
    def test_on_topic_start(self, observer, mock_topic, log_capture):
        # Act
        observer.on_topic_start(mock_topic)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "INFO - Starting to process topic: Science" in log_output

    def test_on_topic_complete(self, observer, mock_topic, log_capture):
        # Act
        observer.on_topic_complete(mock_topic)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "INFO - Completed processing topic: Science" in log_output
        assert "INFO - Found 2 missing articles" in log_output

    def test_on_topic_error(self, observer, mock_topic, log_capture):
        # Act
        error = Exception("Test error")
        observer.on_topic_error(mock_topic, error)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "ERROR - Error processing topic Science: Test error" in log_output

    def test_on_batch_start(self, observer, mock_topic, log_capture):
        # Act
        observer.on_batch_start(mock_topic, 1, 50)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "INFO - Starting batch 1 for topic Science with 50 articles" in log_output

    def test_on_batch_complete(self, observer, mock_topic, log_capture):
        # Act
        observer.on_batch_complete(mock_topic, 1, 50, 25, 20)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "INFO - Completed batch 1 for topic Science" in log_output
        assert "Added 25 English versions and 20 descriptions" in log_output

    def test_on_wikidata_lookup(self, observer, log_capture):
        # Act
        observer.on_wikidata_lookup(["Article1", "Article2"])
        
        # Assert
        log_output = log_capture.getvalue()
        assert "INFO - Looking up Wikidata descriptions for 2 articles" in log_output

    def test_on_wikidata_result(self, observer, log_capture):
        # Act
        observer.on_wikidata_result(15, 20)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "INFO - Found 15 descriptions out of 20 articles" in log_output

    def test_on_api_request(self, observer, log_capture):
        # Act
        observer.on_api_request("api.example.com", {"param": "value"})
        
        # Assert
        log_output = log_capture.getvalue()
        assert "DEBUG - Making API request to api.example.com" in log_output

    def test_on_api_response_success(self, observer, log_capture):
        # Act
        observer.on_api_response("api.example.com", 200, True)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "DEBUG - Successful API response from api.example.com with status 200" in log_output

    def test_on_api_response_failure(self, observer, log_capture):
        # Act
        observer.on_api_response("api.example.com", 404, False)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "WARNING - Failed API response from api.example.com with status 404" in log_output

    def test_on_db_query(self, observer, log_capture):
        # Act
        observer.on_db_query("SELECT * FROM table")
        
        # Assert
        log_output = log_capture.getvalue()
        assert "DEBUG - Executing database query: SELECT * FROM table" in log_output

    def test_on_db_result(self, observer, log_capture):
        # Act
        observer.on_db_result(100)
        
        # Assert
        log_output = log_capture.getvalue()
        assert "DEBUG - Database query returned 100 results" in log_output 