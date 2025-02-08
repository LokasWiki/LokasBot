import pytest
from unittest.mock import Mock, patch

from tasks.missingtopics.entities.topic_entity import Article
from tasks.missingtopics.repositories.article_repository import WikiArticleRepository, MissingTopicsConfig

@pytest.fixture
def mock_response():
    return """
    {| class="wikitable sortable"
    |-
    ! Title !! Count
    |-
    | 10 || [[Test Article 1]]
    |-
    | 5 || [[Test Article 2]]
    |}
    """

@pytest.fixture
def mock_db_result():
    return [
        {'p_title': b'Test_Article_1'},
        {'p_title': b'Another_Article'}
    ]

@pytest.fixture
def article_repository():
    config = MissingTopicsConfig(
        base_url="https://test.toolforge.org",
        language="test",
        project="wikipedia"
    )
    return WikiArticleRepository(config=config)

class TestWikiArticleRepository:
    @patch('requests.get')
    def test_get_missing_articles_success(self, mock_get, article_repository, mock_response):
        # Arrange
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_response

        # Act
        articles = article_repository.get_missing_articles("test_topic")

        # Assert
        assert len(articles) == 2
        assert articles[0].title == "[[Test Article 1]]"
        assert articles[0].link_count == 10
        assert articles[1].title == "[[Test Article 2]]"
        assert articles[1].link_count == 5

    @patch('requests.get')
    def test_get_missing_articles_api_error(self, mock_get, article_repository):
        # Arrange
        mock_get.return_value.status_code = 404

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            article_repository.get_missing_articles("test_topic")
        assert "Failed to fetch data for topic test_topic" in str(exc_info.value)

    @patch('core.utils.wikidb.Database')
    def test_get_english_versions_success(self, MockDatabase, article_repository, mock_db_result):
        # Arrange
        mock_db = Mock()
        mock_db.result = mock_db_result
        MockDatabase.return_value = mock_db

        titles = ["Test_Article_1", "Test_Article_2"]

        # Act
        result = article_repository.get_english_versions(titles)

        # Assert
        assert "Test_Article_1" in result
        assert result["Test_Article_1"] == "Test_Article_1"
        assert "Test_Article_2" not in result

    def test_get_english_versions_empty_titles(self, article_repository):
        # Act
        result = article_repository.get_english_versions([])

        # Assert
        assert result == {} 