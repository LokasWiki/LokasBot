import pytest
from unittest.mock import Mock, patch

from tasks.missingtopics.entities.topic_entity import Article
from tasks.missingtopics.repositories.article_repository import (
    WikiArticleRepository,
    MissingTopicsConfig,
    DatabaseConfig
)

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
def mock_wikidata_response():
    return {
        "query": {
            "pages": {
                "123": {
                    "title": "Test Article 1",
                    "pageprops": {
                        "wikibase_item": "Q123"
                    }
                }
            }
        }
    }

@pytest.fixture
def mock_wikidata_entities_response():
    return {
        "entities": {
            "Q123": {
                "descriptions": {
                    "en": {
                        "value": "Test description"
                    }
                }
            }
        }
    }

@pytest.fixture
def default_config():
    return MissingTopicsConfig(
        base_url="https://test.toolforge.org",
        language="test",
        project="wikipedia"
    )

@pytest.fixture
def default_db_config():
    return DatabaseConfig(
        host="test.host",
        db_name="test_wiki",
        db_port=3306,
        charset='utf8mb4'
    )

@pytest.fixture
def article_repository(default_config, default_db_config):
    return WikiArticleRepository(
        config=default_config,
        db_config=default_db_config
    )

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

    @patch('pymysql.connect')
    def test_get_english_versions_success(self, mock_connect, article_repository, mock_db_result):
        # Arrange
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = mock_db_result
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

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

    def test_custom_database_config(self, default_config):
        # Arrange
        custom_db_config = DatabaseConfig(
            host="custom.host",
            db_name="custom_wiki",
            db_port=3307,
            charset='latin1'
        )

        # Act
        repo = WikiArticleRepository(
            config=default_config,
            db_config=custom_db_config
        )

        # Assert
        assert repo.db_config.host == "custom.host"
        assert repo.db_config.db_name == "custom_wiki"
        assert repo.db_config.db_port == 3307
        assert repo.db_config.charset == 'latin1'

    @patch('pymysql.connect')
    def test_database_connection_parameters(self, mock_connect, default_config, default_db_config):
        # Arrange
        repo = WikiArticleRepository(
            config=default_config,
            db_config=default_db_config
        )

        # Act
        db = repo._get_db_connection()

        # Assert
        mock_connect.assert_called_once_with(
            host=default_db_config.host,
            read_default_file=default_db_config.read_default_file,
            db=default_db_config.db_name,
            charset=default_db_config.charset,
            port=default_db_config.db_port,
            cursorclass=pytest.approx(type(Mock()))
        )

    @patch('requests.get')
    def test_get_wikidata_descriptions_success(
        self,
        mock_get,
        article_repository,
        mock_wikidata_response,
        mock_wikidata_entities_response
    ):
        # Arrange
        mock_get.side_effect = [
            Mock(
                status_code=200,
                json=lambda: mock_wikidata_response
            ),
            Mock(
                status_code=200,
                json=lambda: mock_wikidata_entities_response
            )
        ]

        # Act
        descriptions = article_repository.get_wikidata_descriptions(["Test Article 1"])

        # Assert
        assert "Test Article 1" in descriptions
        assert descriptions["Test Article 1"] == "Test description"
        assert len(mock_get.call_args_list) == 2  # Two API calls made

    @patch('requests.get')
    def test_get_wikidata_descriptions_empty_titles(self, mock_get, article_repository):
        # Act
        descriptions = article_repository.get_wikidata_descriptions([])

        # Assert
        assert descriptions == {}
        mock_get.assert_not_called()

    @patch('requests.get')
    def test_get_wikidata_descriptions_api_error(self, mock_get, article_repository):
        # Arrange
        mock_get.return_value = Mock(status_code=404)

        # Act
        descriptions = article_repository.get_wikidata_descriptions(["Test Article"])

        # Assert
        assert descriptions == {}

    @patch('requests.get')
    def test_get_wikidata_descriptions_batch_processing(
        self,
        mock_get,
        article_repository,
        mock_wikidata_response,
        mock_wikidata_entities_response
    ):
        # Arrange
        titles = [f"Article {i}" for i in range(100)]  # Create 100 titles
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: mock_wikidata_response),
            Mock(status_code=200, json=lambda: mock_wikidata_entities_response)
        ] * 2  # Repeat for each batch

        # Act
        article_repository.get_wikidata_descriptions(titles)

        # Assert
        # Should make API calls in batches of 50
        assert len(mock_get.call_args_list) == 4  # 2 calls per batch * 2 batches 