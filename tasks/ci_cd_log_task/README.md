# CI/CD Log Task - Clean Architecture Implementation

A refactored implementation of the CI/CD Log Task following Clean Architecture principles. This bot fetches commit information and contributors from GitHub and posts formatted log messages to a wiki page.

## 🏗️ Architecture Overview

This project follows **Clean Architecture** principles with a clear separation of concerns across four layers:

```
┌─────────────────────────────────────────────────┐
│                Presentation Layer               │
│           (BotController, main.py)              │
├─────────────────────────────────────────────────┤
│                  Use Cases Layer                │
│   (FetchCommitData, FetchContributors,          │
│    CreateLogMessage)                            │
├─────────────────────────────────────────────────┤
│                   Domain Layer                  │
│       (Entities, Repository Interfaces)         │
├─────────────────────────────────────────────────┤
│               Infrastructure Layer             │
│       (GitHubAPI, WikiOperations)               │
└─────────────────────────────────────────────────┘
```

### 🏛️ Layer Responsibilities

#### Domain Layer (`domain/`)
- **Entities**: Core business data structures (`CommitInfo`, `BotLog`)
- **Repository Interfaces**: Contracts for data access (`GitHubRepository`, `WikiRepository`)
- **Pure business logic**: No external dependencies

#### Use Cases Layer (`domain/use_cases/`)
- **Business Logic**: Application-specific workflows
- **Orchestration**: Coordinates between repositories and entities
- **Error Handling**: Graceful error handling with fallbacks

#### Infrastructure Layer (`infrastructure/`)
- **External Services**: GitHub API client, Wiki operations
- **Data Access**: Concrete implementations of repository interfaces
- **External Dependencies**: All third-party library interactions

#### Presentation Layer (`presentation/`)
- **Controllers**: Main application logic (`BotController`)
- **Configuration**: Environment variable handling
- **Workflow Orchestration**: Coordinates the entire process

## 📁 Project Structure

```
tasks/ci_cd_log_task/
├── main.py                          # Application entry point
├── domain/                          # Business logic layer
│   ├── entities/                    # Core data models
│   │   ├── commit_info.py          # GitHub commit information
│   │   └── bot_log.py              # Bot log message entity
│   ├── use_cases/                   # Business logic
│   │   ├── fetch_commit_data.py    # GitHub commit fetching
│   │   ├── fetch_contributors.py   # Contributors fetching
│   │   └── create_log_message.py   # Log message creation
│   └── repositories/               # Data access interfaces
│       ├── github_repository.py    # GitHub operations interface
│       └── wiki_repository.py      # Wiki operations interface
├── infrastructure/                 # External service implementations
│   ├── github_api.py              # GitHub API client
│   └── wiki_operations.py         # Wiki operations with pywikibot
├── presentation/                   # Application controllers
│   └── bot_controller.py          # Main application controller
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pywikibot
- requests

### Installation

1. **Install dependencies:**
   ```bash
   pip install pywikibot requests
   ```

2. **Set environment variables:**
   ```bash
   export LOGNAME="YourBotName"  # Tool name for the log
   ```

3. **Configure pywikibot** (if not already configured):
   ```bash
   # Run this in your terminal
   python -c "import pywikibot; pywikibot.config.authenticate()"
   ```

### Running the Application

1. **Basic execution:**
   ```bash
   python tasks/ci_cd_log_task/main.py
   ```

2. **Detailed reporting mode:**
   ```bash
   python tasks/ci_cd_log_task/main.py --detailed
   ```

3. **From the task directory:**
   ```bash
   cd tasks/ci_cd_log_task
   python main.py
   ```

## ⚙️ Configuration

The application uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `LOGNAME` | Tool name for the bot log | "غير متوفر" |

### Repository Configuration
The application is currently configured to work with:
- **GitHub Repository**: `LokasWiki/LokasBot`
- **Branch**: `main`
- **Wiki Site**: Arabic Wikipedia (`ar`)

To modify these settings, edit the configuration in `presentation/bot_controller.py`.

## 🔧 Key Components

### Domain Entities

#### `CommitInfo`
Represents GitHub commit information:
```python
commit = CommitInfo(
    commit_message="Fix bug in logging",
    commit_date="2024-01-01T12:00:00Z",
    commit_html_url="https://github.com/...",
    last_commit_author="developer"
)
```

#### `BotLog`
Represents a formatted bot log message:
```python
log = BotLog(
    tool_name="MyBot",
    bot_version="1.0.0",
    commit_info=commit_info,
    contributors=["user1", "user2"]
)
```

### Use Cases

#### `FetchCommitData`
Fetches the latest commit from GitHub:
```python
use_case = FetchCommitData(github_repository)
commit_info = use_case.execute("LokasWiki", "LokasBot", "main")
```

#### `FetchContributors`
Fetches repository contributors:
```python
use_case = FetchContributors(github_repository)
contributors = use_case.execute("LokasWiki", "LokasBot")
```

#### `CreateLogMessage`
Creates formatted wiki log messages:
```python
use_case = CreateLogMessage()
bot_log = use_case.execute(tool_name, version, commit_info, contributors)
```

### Infrastructure

#### `GitHubAPI`
Implements GitHub repository interface:
```python
github_api = GitHubAPI()
commit_info = github_api.fetch_latest_commit("owner", "repo", "main")
```

#### `WikiOperations`
Implements wiki repository interface:
```python
wiki_ops = WikiOperations(site_name="ar")
wiki_ops.save_log_message(bot_log)
```

## 🧪 Testing

### Unit Testing
Each layer can be tested independently:

```python
# Test domain entities
commit_info = CommitInfo.create_unavailable()
assert commit_info.commit_message == "غير متوفر"

# Test use cases with mocked repositories
mock_github = Mock(GitHubRepository)
use_case = FetchCommitData(mock_github)
result = use_case.execute("owner", "repo")
```

### Integration Testing
Test with real external services:

```python
# Test GitHub API integration
github_api = GitHubAPI()
commit_info = github_api.fetch_latest_commit("LokasWiki", "LokasBot", "main")
assert commit_info.commit_message is not None
```

## 🏗️ Architecture Benefits

### 1. **Separation of Concerns**
- Each layer has a single, well-defined responsibility
- Clear boundaries between business logic and infrastructure
- Easier to understand and maintain

### 2. **Testability**
- Business logic can be tested without external dependencies
- Mock implementations for repositories in unit tests
- Each use case can be tested in isolation

### 3. **Maintainability**
- Changes to one layer don't affect others
- Clear interfaces make it easy to understand dependencies
- Easier to onboard new developers

### 4. **Reusability**
- Components can be reused in different contexts
- Repository interfaces allow for different implementations
- Use cases can be composed in different ways

### 5. **Dependency Inversion**
- High-level modules don't depend on low-level modules
- Both depend on abstractions (interfaces)
- Follows SOLID principles

## 🔄 Migration from Original Implementation

The original `bot.py` script has been refactored into clean architecture:

### Before (Original Structure)
```python
# Everything mixed together
import os, datetime, pywikibot, requests

# Configuration, data fetching, and wiki operations all in one file
site = pywikibot.Site('ar', 'wikipedia')
# ... 100+ lines of mixed concerns
```

### After (Clean Architecture)
```python
# Separated into focused layers
from domain.entities.commit_info import CommitInfo
from domain.use_cases.fetch_commit_data import FetchCommitData
from infrastructure.github_api import GitHubAPI
from presentation.bot_controller import BotController

# Each component has a single responsibility
github_api = GitHubAPI()
fetch_commit = FetchCommitData(github_api)
commit_info = fetch_commit.execute("owner", "repo", "branch")
```

## 📊 Error Handling

The application implements comprehensive error handling:

1. **Network Errors**: Graceful fallback for GitHub API failures
2. **Configuration Errors**: Validation of required environment variables
3. **Wiki Errors**: Safe handling of pywikibot exceptions
4. **Data Validation**: Input validation in use cases

### Error Reporting Modes

1. **Standard Mode**: Simple success/failure reporting
2. **Detailed Mode**: Step-by-step execution reporting with warnings

```bash
# Run with detailed error reporting
python main.py --detailed
```

## 🔍 Logging

The application uses Python's built-in logging with different levels:

- **INFO**: General application flow
- **WARNING**: Non-critical issues with fallbacks
- **ERROR**: Critical failures that stop execution
- **DEBUG**: Detailed execution information (when enabled)

## 🚀 Deployment

### Environment Setup
1. Ensure Python 3.7+ is installed
2. Install dependencies: `pip install pywikibot requests`
3. Configure pywikibot for your wiki site
4. Set required environment variables

### Production Considerations
- Use virtual environments
- Implement proper logging rotation
- Monitor API rate limits
- Set up error notifications
- Consider using environment-specific configurations

## 🤝 Contributing

When contributing to this project:

1. **Follow Clean Architecture principles**
2. **Add tests for new functionality**
3. **Update documentation**
4. **Maintain separation of concerns**
5. **Use type hints consistently**

### Adding New Features

1. **New Use Case**: Add to `domain/use_cases/`
2. **New Entity**: Add to `domain/entities/`
3. **New Repository**: Add interface to `domain/repositories/` and implementation to `infrastructure/`
4. **Update Controller**: Modify `presentation/bot_controller.py`

## 📝 License

This project follows the same license as the parent project.

## 🆘 Troubleshooting

### Common Issues

1. **GitHub API Rate Limits**
   - Solution: Implement authentication or use API tokens
   - Status: Not implemented (uses anonymous requests)

2. **Wiki Authentication**
   - Solution: Ensure pywikibot is properly configured
   - Check: Run `python -c "import pywikibot; print(pywikibot.config.authenticate())"`

3. **Import Errors**
   - Solution: Ensure all `__init__.py` files are present
   - Check: Verify package structure is correct

### Getting Help

1. Check the logs for detailed error messages
2. Run with `--detailed` flag for more information
3. Verify all dependencies are installed
4. Check environment variable configuration

---

**Note**: This implementation maintains full backward compatibility with the original functionality while providing a much more maintainable and testable architecture.