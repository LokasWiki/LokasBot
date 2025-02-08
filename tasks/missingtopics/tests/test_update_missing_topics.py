import pytest
from unittest.mock import Mock, patch, call

from entities.topic_entity import Topic, Article
from use_cases.update_missing_topics import UpdateMissingTopicsUseCase

@pytest.fixture
def mock_topic():
    return Topic(
        name="Science",
        page_name="Wikipedia:Missing Articles/Science",
        missing_articles=[]
    )

@pytest.fixture
def mock_articles():
    return [
        Article(title="[[Article 1]]", link_count=10),
        Article(title="[[Article 2]]", link_count=5)
    ]

@pytest.fixture
def mock_observer():
    return Mock()

@pytest.fixture
def use_case(mock_observer):
    topic_repo = Mock()
    article_repo = Mock()
    use_case = UpdateMissingTopicsUseCase(
        topic_repository=topic_repo,
        article_repository=article_repo,
        batch_size=1,
        delay_seconds=0
    )
    use_case.add_observer(mock_observer)
    return use_case

class TestUpdateMissingTopicsUseCase:
    def test_execute_success(self, use_case, mock_topic, mock_articles):
        # Arrange
        use_case.topic_repository.get_all_topics.return_value = [mock_topic]
        use_case.article_repository.get_missing_articles.return_value = mock_articles
        use_case.article_repository.get_english_versions.return_value = {"Article_1": "Article_1"}

        # Act
        use_case.execute()

        # Assert
        use_case.topic_repository.get_all_topics.assert_called_once()
        use_case.article_repository.get_missing_articles.assert_called_once_with("Science")
        assert len(mock_topic.missing_articles) == 2
        use_case.observers[0].on_topic_start.assert_called_once_with(mock_topic)
        use_case.observers[0].on_topic_complete.assert_called_once_with(mock_topic)

    def test_execute_with_error(self, use_case, mock_topic):
        # Arrange
        use_case.topic_repository.get_all_topics.return_value = [mock_topic]
        use_case.article_repository.get_missing_articles.side_effect = Exception("API Error")

        # Act
        use_case.execute()

        # Assert
        use_case.observers[0].on_topic_start.assert_called_once_with(mock_topic)
        use_case.observers[0].on_topic_error.assert_called_once()
        args = use_case.observers[0].on_topic_error.call_args[0]
        assert args[0] == mock_topic
        assert isinstance(args[1], Exception)
        assert str(args[1]) == "API Error"

    def test_process_article_batch(self, use_case, mock_articles):
        # Arrange
        use_case.article_repository.get_english_versions.return_value = {
            "Article_1": "English_Article_1"
        }

        # Act
        use_case._process_article_batch(mock_articles)

        # Assert
        assert mock_articles[0].en_title == "English_Article_1"
        assert mock_articles[1].en_title == ""

    def test_generate_page_content(self, use_case, mock_topic, mock_articles):
        # Arrange
        mock_topic.missing_articles = mock_articles
        mock_articles[0].en_title = "English_Article_1"

        # Act
        content = use_case._generate_page_content(mock_topic)

        # Assert
        assert "[[Article 1]]" in content
        assert "[[Article 2]]" in content
        assert "[[:en:English_Article_1]]" in content
        assert "class=\"wikitable sortable\"" in content 