import pytest
from unittest.mock import Mock, patch

from tasks.missingtopics.entities.topic_entity import Topic, Article
from tasks.missingtopics.repositories.topic_repository import WikiTopicRepository

@pytest.fixture
def mock_db_result():
    return [
        {'page_title': b'Science'},
        {'page_title': b'History'},
        {'page_title': b'Mathematics'}
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
        assert len(topics) == 3
        assert topics[0].name == "Science"
        assert topics[0].page_name == "ويكيبيديا:مقالات مطلوبة حسب الاختصاص/Science"
        assert topics[0].missing_articles == []
        assert topics[1].name == "History"
        assert topics[2].name == "Mathematics"

    @patch('core.utils.wikidb.Database')
    def test_get_all_topics_empty_result(self, MockDatabase, topic_repository):
        # Arrange
        mock_db = Mock()
        mock_db.result = []
        MockDatabase.return_value = mock_db

        # Act
        topics = topic_repository.get_all_topics()

        # Assert
        assert len(topics) == 0

    @patch('core.utils.wikidb.Database')
    def test_get_all_topics_query_format(self, MockDatabase, topic_repository):
        # Arrange
        mock_db = Mock()
        mock_db.result = []
        MockDatabase.return_value = mock_db

        # Act
        topic_repository.get_all_topics()

        # Assert
        assert "select replace" in mock_db.query.lower()
        assert "from pagelinks" in mock_db.query.lower()
        assert "where pl_from in (676775)" in mock_db.query.lower()

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
        mock_page.save.assert_called_once_with("بوت:تحديث مقالات مطلوبة حسب الاختصاص v3.1.0")

    @patch('pywikibot.Page')
    def test_save_topic_page_with_articles(self, MockPage, topic_repository):
        # Arrange
        mock_page = Mock()
        MockPage.return_value = mock_page
        articles = [
            Article(title="Article 1", link_count=5),
            Article(title="Article 2", link_count=10)
        ]
        topic = Topic(
            name="Science",
            page_name="Test Page",
            missing_articles=articles
        )
        content = "Test content with articles"

        # Act
        topic_repository.save_topic_page(topic, content)

        # Assert
        assert mock_page.text == content
        mock_page.save.assert_called_once()

    @patch('pywikibot.Site')
    def test_site_initialization(self, MockSite, topic_repository):
        # Assert
        MockSite.assert_called_once()

    @patch('pywikibot.Page')
    def test_save_topic_page_error_handling(self, MockPage, topic_repository):
        # Arrange
        mock_page = Mock()
        mock_page.save.side_effect = Exception("Save failed")
        MockPage.return_value = mock_page
        topic = Topic(name="Science", page_name="Test Page", missing_articles=[])
        content = "Test content"

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            topic_repository.save_topic_page(topic, content)
        assert "Save failed" in str(exc_info.value) 