# Missing Topics Task

A clean architecture implementation of a system that identifies and updates Wikipedia pages listing missing articles by topic/specialty in Arabic Wikipedia. The task identifies articles that exist in English Wikipedia but are missing in Arabic Wikipedia, organized by different specialties or topics.

## 🏗️ Architecture

The project follows Clean Architecture principles and is organized into the following layers:

### 1. Entities
- `Topic`: Core business object representing a topic with its missing articles
- `Article`: Represents a missing article with its properties (title, link count, English version)

### 2. Use Cases
- `UpdateMissingTopicsUseCase`: Contains the business logic for updating missing topics pages
  - Supports dynamic bot name configuration
  - Implements batch processing and rate limiting
  - Uses observer pattern for progress monitoring
  - Includes dynamic timestamp updates

### 3. Repositories
- `ArticleRepository`: Abstract interface for article operations
  - `WikiArticleRepository`: Concrete implementation for fetching missing articles
  - Configurable database connections for different wikis
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
   - Supports configurable database connections

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
   - Configurable database settings

## 🚀 Usage

### Basic Usage

```python
from tasks.missingtopics.repositories.article_repository import WikiArticleRepository, MissingTopicsConfig, DatabaseConfig
from tasks.missingtopics.repositories.topic_repository import WikiTopicRepository
from tasks.missingtopics.use_cases.update_missing_topics import UpdateMissingTopicsUseCase
from tasks.missingtopics.observers.logging_observer import LoggingObserver

# Initialize repositories with custom configurations
db_config = DatabaseConfig(
    host="enwiki.analytics.db.svc.wikimedia.cloud",
    db_name="enwiki_p"
)

article_repository = WikiArticleRepository(db_config=db_config)
topic_repository = WikiTopicRepository()

# Create use case with custom settings
use_case = UpdateMissingTopicsUseCase(
    topic_repository=topic_repository,
    article_repository=article_repository,
    bot_name="CustomBot",  # Configure custom bot name
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

# Configure database settings
db_config = DatabaseConfig(
    host="custom.host",
    db_name="custom_wiki",
    db_port=3306,
    charset='utf8mb4'
)

article_repository = WikiArticleRepository(
    config=config,
    db_config=db_config
)
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

2. **Database Configuration**:
   - Host and port
   - Database name
   - Character set
   - Connection settings

3. **Performance Settings**:
   - Batch size for processing
   - Delay between requests
   - Rate limiting

4. **Bot Configuration**:
   - Custom bot name
   - Dynamic timestamps
   - Update messages

5. **Logging**:
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
- Dynamic bot name configuration
- Real-time timestamp updates
- Configurable database connections

## 🧪 Testing

The project includes a comprehensive test suite covering all components:

### Running Tests

```bash
# Run all tests
pytest tests/tasks/missingtopics/

# Run specific test file
pytest tests/tasks/missingtopics/test_article_repository.py

# Run with coverage
pytest tests/tasks/missingtopics/ --cov=tasks.missingtopics

# Run with verbose output
pytest -v tests/tasks/missingtopics/
```

### Test Structure

1. **Entity Tests** (`test_topic_entity.py`):
   - Article class tests
     - Creation and properties
     - English version handling
     - Wiki link formatting
   - Topic class tests
     - Creation and properties
     - Article management
     - Edge cases

2. **Repository Tests**:
   - Article Repository (`test_article_repository.py`)
     - Missing articles retrieval
     - English version lookups
     - Database configuration
     - Error handling
     - Connection management
   - Topic Repository (`test_topic_repository.py`)
     - Topic retrieval
     - Page saving
     - Query formatting
     - Error scenarios

3. **Use Case Tests** (`test_update_missing_topics.py`):
   - Update process
   - Batch processing
   - Bot name configuration
   - Content generation
   - Error handling
   - Observer notifications

4. **Observer Tests** (`test_logging_observer.py`):
   - Event handling
   - Log message formatting
   - Error logging
   - Integration with logging system

### Test Coverage

Each component is tested for:

1. **Happy Path**:
   - Normal operation scenarios
   - Expected inputs and outputs
   - Successful operations

2. **Error Handling**:
   - Invalid inputs
   - Network failures
   - Database errors
   - API errors

3. **Edge Cases**:
   - Empty collections
   - Boundary conditions
   - Special characters
   - Resource cleanup

4. **Integration Points**:
   - Database interactions
   - API calls
   - File operations
   - External services

### Mocking Strategy

The test suite uses mocking to isolate components:

1. **External Services**:
   - Database connections
   - API endpoints
   - File systems
   - Wiki interactions

2. **Internal Components**:
   - Repositories
   - Observers
   - Configuration

### Test Fixtures

Common test fixtures provide:

1. **Mock Data**:
   - Sample topics
   - Test articles
   - Database results
   - API responses

2. **Configuration**:
   - Database settings
   - API parameters
   - Test environment setup

### Best Practices

The test suite follows these principles:

1. **Isolation**: Each test is independent
2. **Readability**: Clear arrange-act-assert pattern
3. **Maintainability**: DRY principles with fixtures
4. **Coverage**: Comprehensive testing of all features

## 🔮 Future Improvements

1. Add caching mechanism for API responses
2. Implement async/await support
3. Add more update strategies
4. Enhance error recovery
5. Add integration tests
6. Support more languages
7. Add metrics collection
8. Implement rate limiting strategies
9. Add database connection pooling
10. Enhance timestamp formatting options

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Logging System

The project includes a comprehensive logging system that provides detailed insights into the application's operation:

### Log Levels

- **INFO**: Important operational events
  - Topic processing start/completion
  - Batch processing updates
  - Article statistics
  - Wikidata lookup results

- **DEBUG**: Detailed operational data
  - API requests and responses
  - Database queries and results
  - Performance metrics

- **WARNING**: Potential issues
  - Failed API responses
  - Rate limiting events
  - Data inconsistencies

- **ERROR**: Critical issues
  - Processing failures
  - API errors
  - Database connection issues

### Configuration

Logging can be configured in `main.py`:

```python
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Console output
        ]
    )
```

### Observer Pattern

The logging system uses the Observer pattern through `LoggingObserver`:

- Monitors all major operations
- Provides real-time feedback
- Supports multiple observers
- Configurable log levels
- Structured logging format

### Log Events

1. **Topic Processing**
   - Start and completion of topic updates
   - Error handling and recovery
   - Statistics and summaries

2. **Batch Operations**
   - Batch processing progress
   - Success/failure rates
   - Performance metrics

3. **API Interactions**
   - Request details
   - Response status
   - Error handling

4. **Database Operations**
   - Query execution
   - Result statistics
   - Performance metrics

### Usage Example

```python
from tasks.missingtopics.observers.logging_observer import LoggingObserver

# Create and configure observer
observer = LoggingObserver()

# Add to use case
use_case = UpdateMissingTopicsUseCase(...)
use_case.add_observer(observer)
```

### Testing

The logging system includes comprehensive tests:

```python
def test_logging_capture(observer, log_capture):
    observer.on_topic_start(topic)
    log_output = log_capture.getvalue()
    assert "Starting to process topic" in log_output
``` 