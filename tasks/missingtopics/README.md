# Missing Topics Task

A clean architecture implementation of a system that identifies and updates Wikipedia pages listing missing articles by topic/specialty in Arabic Wikipedia. The task identifies articles that exist in English Wikipedia but are missing in Arabic Wikipedia, organized by different specialties or topics.

## 🏗️ Architecture

The project follows Clean Architecture principles and is organized into the following layers:

### 1. Entities
- `Topic`: Core business object representing a topic with its missing articles
- `Article`: Represents a missing article with its properties (title, link count, English version)

### 2. Use Cases
- `UpdateMissingTopicsUseCase`: Contains the business logic for updating missing topics pages
- Implements batch processing and rate limiting
- Uses observer pattern for progress monitoring

### 3. Repositories
- `ArticleRepository`: Abstract interface for article operations
  - `WikiArticleRepository`: Concrete implementation for fetching missing articles
- `TopicRepository`: Abstract interface for topic operations
  - `WikiTopicRepository`: Concrete implementation using Pywikibot

### 4. Observers
- `UpdateObserver`: Protocol for monitoring the update process
- `LoggingObserver`: Provides detailed logging of the update process

## 🎨 Design Patterns

The project implements several design patterns to achieve flexibility and maintainability:

1. **Repository Pattern**
   - Abstracts data access layer
   - Makes it easy to change data sources
   - Provides clean interfaces for data operations

2. **Observer Pattern**
   - Monitors update progress
   - Provides logging capabilities
   - Supports multiple observers
   - Loosely coupled notification system

3. **Command Pattern**
   - Encapsulates update operations
   - Separates command from execution
   - Makes it easy to add new commands

4. **Configuration Pattern**
   - Centralizes API configuration
   - Makes it easy to modify API parameters
   - Supports different environments

## 🚀 Usage

### Basic Usage

```python
from tasks.missingtopics.repositories.article_repository import WikiArticleRepository, MissingTopicsConfig
from tasks.missingtopics.repositories.topic_repository import WikiTopicRepository
from tasks.missingtopics.use_cases.update_missing_topics import UpdateMissingTopicsUseCase
from tasks.missingtopics.observers.logging_observer import LoggingObserver

# Initialize repositories
topic_repository = WikiTopicRepository()
article_repository = WikiArticleRepository()

# Create use case
use_case = UpdateMissingTopicsUseCase(
    topic_repository=topic_repository,
    article_repository=article_repository,
    batch_size=50,
    delay_seconds=3
)

# Add observers
use_case.add_observer(LoggingObserver())

# Execute update
use_case.execute()
```

### Custom Configuration

```python
# Configure with custom settings
config = MissingTopicsConfig(
    base_url="https://missingtopics.toolforge.org/",
    language="ar",
    project="wikipedia",
    depth=1,
    wikimode=1,
    nosingles=1,
    limitnum=1
)

article_repository = WikiArticleRepository(config=config)
```

## 📋 Requirements

- Python 3.6+
- pywikibot
- pymysql
- requests
- wikitextparser

## 🛠️ Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install pywikibot pymysql requests wikitextparser
```

3. Configure Pywikibot with your wiki credentials

## 🔧 Configuration

The system can be configured through various components:

1. **API Configuration**:
   - Base URL
   - Language
   - Project
   - Depth and other parameters

2. **Performance Settings**:
   - Batch size for processing
   - Delay between requests
   - Rate limiting

3. **Logging**:
   - Configurable logging levels
   - Multiple observers support
   - Detailed error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🔍 Project Structure

```
tasks/missingtopics/
├── README.md
├── main.py
├── entities/
│   └── topic_entity.py
├── repositories/
│   ├── article_repository.py
│   └── topic_repository.py
├── use_cases/
│   └── update_missing_topics.py
└── observers/
    └── logging_observer.py
```

## ✨ Features

- Clean Architecture implementation
- Efficient batch processing
- Rate limiting for API requests
- Comprehensive error handling
- Multiple observer support
- Type hints for better IDE support
- Configurable API settings
- Detailed logging system

## 🧪 Testing

The project includes a comprehensive test suite:

### Running Tests

```bash
# Run all tests
pytest tests/tasks/missingtopics/

# Run with coverage
pytest tests/tasks/missingtopics/ --cov=tasks.missingtopics
```

### Test Structure

1. **Unit Tests**:
   - Repository tests
   - Use case tests
   - Entity tests
   - Observer tests

2. **Mock Objects**:
   - API responses
   - Database results
   - Wiki pages

3. **Test Coverage**:
   - Aims for high coverage
   - Covers error cases
   - Tests edge conditions

## 🔮 Future Improvements

1. Add caching mechanism for API responses
2. Implement async/await support
3. Add more update strategies
4. Enhance error recovery
5. Add integration tests
6. Support more languages
7. Add metrics collection
8. Implement rate limiting strategies

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 