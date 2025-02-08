import pytest
from unittest.mock import Mock, patch

from tasks.missingtopics.entities.topic_entity import Topic
from tasks.missingtopics.repositories.topic_repository import WikiTopicRepository

@pytest.fixture
def mock_db_result():
    return [
        {'page_title': b'Science'},
        {'page_title': b'History'}
    ]

@pytest.fixture
def topic_repository():
    return WikiTopicRepository()

class TestWikiTopicRepository:
    @patch('core.utils.wikidb.Database')
    def test_get_all_topics_success(self, MockDatabase, topic_repository, mock_db_result):
        # Arrange
        mock_db = Mock()
        mock_db.result = mock_db_result
        MockDatabase.return_value = mock_db

        # Act
        topics = topic_repository.get_all_topics()

        # Assert
        assert len(topics) == 2
        assert topics[0].name == "Science"
        assert topics[0].page_name == "ويكيبيديا:مقالات مطلوبة حسب الاختصاص/Science"
        assert topics[0].missing_articles == []
        assert topics[1].name == "History"

    @patch('pywikibot.Page')
    def test_save_topic_page_success(self, MockPage, topic_repository):
        # Arrange
        mock_page = Mock()
        MockPage.return_value = mock_page
        topic = Topic(name="Science", page_name="Test Page", missing_articles=[])
        content = "Test content"

        # Act
        topic_repository.save_topic_page(topic, content)

        # Assert
        mock_page.text = content
        mock_page.save.assert_called_once_with("بوت:تحديث مقالات مطلوبة حسب الاختصاص v2.0.0") 