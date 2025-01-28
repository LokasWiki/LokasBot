# Wiki Page Update Task

A clean architecture implementation of a Wikipedia page update system using various design patterns. This task is designed to update wiki pages with new content while providing flexibility, maintainability, and extensibility.

## 🏗️ Architecture

The project follows Clean Architecture principles and is organized into the following layers:

### 1. Entities
- `PageEntity`: Core business object that represents a wiki page with its properties (title, text, summary)

### 2. Use Cases
- `UpdatePageUseCase`: Contains the business logic for updating pages
- `UpdateStrategy`: Abstract strategy for different content update methods
  - `ReplaceContentStrategy`: Replaces entire page content
  - `AppendContentStrategy`: Adds new content at the end
  - `PrependContentStrategy`: Adds new content at the beginning

### 3. Repositories
- `PageRepository`: Abstract interface for page operations
- `PywikibotPageRepository`: Concrete implementation using Pywikibot
- `RepositoryFactory`: Factory for creating repository instances

### 4. Observers
- `PageUpdateObserver`: Abstract observer for monitoring page updates
- `ConsoleLogger`: Logs updates to console
- `FileLogger`: Logs updates to a file

## 🎨 Design Patterns

The project implements several design patterns to achieve flexibility and maintainability:

1. **Factory Pattern** (`RepositoryFactory`)
   - Centralizes repository creation
   - Makes it easy to add new repository types
   - Encapsulates repository initialization logic

2. **Strategy Pattern** (`UpdateStrategy`)
   - Allows different content update behaviors
   - Easy to switch between strategies
   - Extensible for new update methods

3. **Observer Pattern** (`PageUpdateObserver`)
   - Provides logging and monitoring capabilities
   - Supports multiple observers
   - Loosely coupled notification system

4. **Command Pattern** (through use cases)
   - Encapsulates update operations
   - Separates command from execution
   - Makes it easy to add new commands

## 🚀 Usage

### Basic Usage

```python
from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.repositories.repository_factory import RepositoryFactory, RepositoryType
from tasks.sandbox.use_cases.update_page_use_case import UpdatePageUseCase
from tasks.sandbox.observers.page_update_observer import ConsoleLogger, FileLogger
from tasks.sandbox.use_cases.update_strategies import ReplaceContentStrategy

# Create repository using factory
repository = RepositoryFactory.create_repository(RepositoryType.PYWIKIBOT)

# Create use case and add observers
use_case = UpdatePageUseCase(repository)
use_case.add_observer(ConsoleLogger())
use_case.add_observer(FileLogger("updates.log"))

# Set update strategy
use_case.set_strategy(ReplaceContentStrategy())

# Create page entity
page = PageEntity(
    title="Page Title",
    text="New content",
    summary="Update summary"
)

# Execute update
use_case.execute(page)
```

### Using Different Update Strategies

```python
from tasks.sandbox.use_cases.update_strategies import AppendContentStrategy, PrependContentStrategy

# To append content
use_case.set_strategy(AppendContentStrategy())

# To prepend content
use_case.set_strategy(PrependContentStrategy())
```

## 📋 Requirements

- Python 3.7+
- pywikibot
- typing-extensions (for Python < 3.8)

## 🛠️ Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install pywikibot
```

3. Configure Pywikibot with your wiki credentials

## 🔧 Configuration

The system can be configured through various components:

1. **Logging**:
   - Console logging is enabled by default
   - File logging can be configured with custom file paths
   - Additional loggers can be added by implementing `PageUpdateObserver`

2. **Update Strategies**:
   - Default strategy is `ReplaceContentStrategy`
   - Can be changed at runtime using `set_strategy()`
   - New strategies can be added by implementing `UpdateStrategy`

3. **Repositories**:
   - Default repository is `PywikibotPageRepository`
   - New repositories can be added through `RepositoryFactory`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Project Structure

```
tasks/sandbox/
├── README.md
├── main.py
├── entities/
│   └── page_entity.py
├── repositories/
│   ├── repository_factory.py
│   └── pywikibot_page_repository.py
├── use_cases/
│   ├── update_page_use_case.py
│   ├── page_repository.py
│   └── update_strategies.py
└── observers/
    └── page_update_observer.py
```

## ✨ Features

- Clean Architecture implementation
- Multiple design patterns for flexibility
- Extensible logging system
- Different update strategies
- Factory-based repository creation
- Type hints for better IDE support
- Comprehensive error handling
- Easy to test and maintain

## 🔮 Future Improvements

1. Add more repository implementations (e.g., MediaWiki API)
2. Implement caching mechanism
3. Add more update strategies
4. Enhance error handling and recovery
5. Add unit and integration tests
6. Implement async/await support
7. Add more logging formats (e.g., JSON, structured)

## 🧪 Testing

The project includes a comprehensive test suite that covers all components and design patterns. Here's how to work with the tests:

### Continuous Integration

The project uses GitHub Actions for continuous integration and automated testing. The CI pipeline:

1. **Triggers**:
   - On push to main/master branches
   - On pull requests to main/master
   - When changes are made to:
     - `tasks/sandbox/**`
     - `tests/tasks/sandbox/**`
     - GitHub Actions workflow file

2. **Test Environment**:
   - Runs on Ubuntu latest
   - Tests against Python versions:
     - 3.8
     - 3.9
     - 3.10
     - 3.11

3. **CI Process**:
```yaml
name: Python Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
    - name: Run tests
      run: python -m pytest tests/tasks/sandbox/test_*.py -v
```

4. **Coverage Reporting**:
   - Uses `coverage.py` and `pytest-cov`
   - Generates coverage reports
   - Uploads to Codecov
   - Tracks test coverage trends

5. **CI Features**:
   - Matrix testing across Python versions
   - Automatic dependency installation
   - Coverage reporting
   - Fail-fast on test failures

### Running Tests Locally vs CI

1. **Local Testing**:
```bash
# Run tests without coverage
python3 -m unittest tests/tasks/sandbox/test_*.py -v

# Run tests with coverage
coverage run -m pytest tests/tasks/sandbox/test_*.py -v
coverage report
```

2. **CI Testing**:
   - Automatically runs on GitHub
   - Tests all Python versions
   - Generates coverage reports
   - Updates status badges

### Test Status Badge

[![Python Tests](https://github.com/{username}/{repository}/actions/workflows/python-tests.yml/badge.svg)](https://github.com/{username}/{repository}/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/{username}/{repository}/branch/main/graph/badge.svg)](https://codecov.io/gh/{username}/{repository})

### Test Structure

The test suite is organized to match the project structure:

```
tests/tasks/sandbox/
├── test_main.py                    # Tests for main script
├── test_page_entity.py            # Entity tests
├── test_page_update_observer.py   # Observer pattern tests
├── test_pywikibot_repository.py   # Repository tests
├── test_repository_factory.py     # Factory pattern tests
├── test_update_strategies.py      # Strategy pattern tests
└── test_update_page_use_case.py  # Use case tests
```

### Test Categories

1. **Unit Tests**:
   - `test_page_entity.py`: Tests the core domain entity
   - `test_update_strategies.py`: Tests different content update strategies
   - `test_repository_factory.py`: Tests repository creation

2. **Integration Tests**:
   - `test_pywikibot_repository.py`: Tests wiki interaction
   - `test_update_page_use_case.py`: Tests business logic flow

3. **Pattern Tests**:
   - Factory Pattern: `test_repository_factory.py`
   - Strategy Pattern: `test_update_strategies.py`
   - Observer Pattern: `test_page_update_observer.py`
   - Command Pattern: `test_update_page_use_case.py`

### Writing Tests

Follow these guidelines when adding new tests:

1. **Test Structure**:
```python
def test_something(self):
    """Clear description of what is being tested"""
    # Arrange
    # Set up your test data and mocks
    
    # Act
    # Execute the code being tested
    
    # Assert
    # Verify the results
```

2. **Mocking**:
```python
@patch('tasks.sandbox.main.UpdatePageUseCase')
def test_with_mock(self, mock_use_case):
    mock_instance = Mock()
    mock_use_case.return_value = mock_instance
    # Test implementation
```

3. **Test Cases to Include**:
   - Happy path (normal operation)
   - Edge cases (empty values, special characters)
   - Error conditions (nonexistent pages, network issues)
   - Pattern-specific behavior (strategy changes, observer notifications)

### Test Coverage

Key areas covered by tests:

1. **Entities**:
   - Initialization
   - Empty values
   - Special characters and Unicode

2. **Use Cases**:
   - Page update execution
   - Strategy application
   - Observer notifications

3. **Repositories**:
   - Page saving
   - Page retrieval
   - Error handling

4. **Patterns**:
   - Factory creation
   - Strategy selection
   - Observer notifications
   - Command execution

### Best Practices

1. **Test Organization**:
   - Use descriptive test names
   - Group related tests in test classes
   - Use setUp for common initialization

2. **Assertions**:
   - Use specific assertions (assertEqual, assertTrue, etc.)
   - Include meaningful error messages
   - Test both positive and negative cases

3. **Mocking**:
   - Mock external dependencies
   - Verify mock calls and arguments
   - Use appropriate mock return values

4. **Documentation**:
   - Add clear docstrings to test methods
   - Explain test purpose and expectations
   - Document any special setup requirements

### Troubleshooting Tests

Common issues and solutions:

1. **Import Errors**:
   - Ensure PYTHONPATH includes the code directory
   - Check import statements use correct paths
   - Verify file structure matches imports

2. **Mock Issues**:
   - Verify mock paths match actual imports
   - Check mock return values are appropriate
   - Ensure mocks are set up before use

3. **Test Failures**:
   - Check test data matches expectations
   - Verify mock configurations
   - Review assertion error messages 