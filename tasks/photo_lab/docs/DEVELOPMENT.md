# Photo Lab - Development Guide

This guide is for developers who want to understand, modify, or extend the Photo Lab task.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Adding Features](#adding-features)
- [Common Modifications](#common-modifications)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Access to the LokasBot codebase

### Setup Development Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pythonProject3
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install pywikibot wikitextparser
   ```

4. **Configure pywikibot** (if not already configured):
   ```bash
   # Follow pywikibot configuration guide
   # Typically involves creating a user-config.py file
   ```

### Verify Setup

Run the tests to verify everything works:

```bash
python -m unittest discover -s tasks/photo_lab/tests -v
```

All tests should pass (some may be skipped if wikitextparser is not installed).

## Development Environment

### IDE Recommendations

- **VS Code**: Recommended extensions:
  - Python
  - Pylance
  - Markdown All in One

### Project Structure

```
tasks/photo_lab/
├── docs/                    # Documentation
├── domain/                  # Business logic
│   ├── entities/           # Data models
│   ├── repositories/       # Interfaces
│   └── use_cases/          # Business operations
├── infrastructure/         # External implementations
├── presentation/           # Controllers/UI
├── tests/                  # Unit tests
└── main.py                # Entry point
```

### Key Files to Know

| File | Purpose |
|------|---------|
| `domain/entities/photo_request.py` | PhotoRequest entity |
| `domain/entities/archive_entry.py` | ArchiveEntry and ArchivePage entities |
| `domain/repositories/wiki_repository.py` | Repository interface |
| `infrastructure/wiki/pywikibot_wiki.py` | Wiki implementation |
| `presentation/controllers/photo_lab_controller.py` | Workflow orchestration |
| `main.py` | CLI entry point |

## Adding Features

### Adding a New Use Case

Let's say you want to add a use case that sends notifications when requests are archived.

1. **Create the use case file**:
   ```bash
   touch tasks/photo_lab/domain/use_cases/send_notifications.py
   ```

2. **Implement the use case**:
   ```python
   """
   Use case for sending notifications about archived requests.
   """
   import logging
   from typing import List
   
   from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
   from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository
   
   
   class SendNotifications:
       """Send notifications when requests are archived."""
       
       def __init__(self, wiki_repository: WikiRepository):
           self.wiki_repository = wiki_repository
           self.logger = logging.getLogger(__name__)
       
       def execute(self, archived_requests: List[PhotoRequest]) -> None:
           """Send notifications for archived requests."""
           for request in archived_requests:
               # Implement notification logic
               self.logger.info(f"Notification sent for: {request.page_name}")
   ```

3. **Add to use_cases `__init__.py`**:
   ```python
   from .send_notifications import SendNotifications
   
   __all__ = [
       # ... existing imports
       'SendNotifications'
   ]
   ```

4. **Use in controller**:
   ```python
   from tasks.photo_lab.domain.use_cases.send_notifications import SendNotifications
   
   # In PhotoLabController.__init__:
   self.send_notifications = SendNotifications(wiki_repository)
   
   # In run method:
   if results['archived']:
       self.send_notifications.execute(archivable_requests)
   ```

### Adding a New Entity

Let's add a `RequestComment` entity to track comments on requests.

1. **Create entity file**:
   ```bash
   touch tasks/photo_lab/domain/entities/request_comment.py
   ```

2. **Implement entity**:
   ```python
   """
   Domain entity representing a comment on a photo request.
   """
   
   from dataclasses import dataclass
   from datetime import datetime
   
   
   @dataclass
   class RequestComment:
       """Represents a comment on a photo request."""
       
       author: str
       text: str
       timestamp: datetime = None
       
       def __post_init__(self):
           if self.timestamp is None:
               self.timestamp = datetime.now()
   ```

3. **Export from entities `__init__.py`**:
   ```python
   from .request_comment import RequestComment
   
   __all__ = [
       # ... existing imports
       'RequestComment'
   ]
   ```

### Adding a Repository Method

Let's add a method to get page history.

1. **Add to interface** (`domain/repositories/wiki_repository.py`):
   ```python
   @abstractmethod
   def get_page_history(self, page_title: str) -> List[dict]:
       """Get revision history of a page."""
       pass
   ```

2. **Implement in `PywikibotWiki`** (`infrastructure/wiki/pywikibot_wiki.py`):
   ```python
   def get_page_history(self, page_title: str) -> List[dict]:
       """Get page revision history."""
       try:
           page = pywikibot.Page(self.site, page_title)
           history = []
           for revision in page.revisions():
               history.append({
                   'id': revision.revid,
                   'timestamp': revision.timestamp,
                   'user': revision.user
               })
           return history
       except Exception as e:
           self.logger.error(f"Error getting history: {str(e)}")
           return []
   ```

3. **Implement in `MockWikiRepository`** (`tests/mock_wiki_repository.py`):
   ```python
   def get_page_history(self, page_title: str) -> List[dict]:
       """Mock implementation."""
       return [
           {
               'id': 12345,
               'timestamp': datetime.now(),
               'user': 'TestUser'
           }
       ]
   ```

## Common Modifications

### Changing Archive Capacity

To change the number of entries per archive page from 10 to a different number:

1. **Find the constant** in `domain/use_cases/manage_archives.py`:
   ```python
   MAX_ENTRIES_PER_ARCHIVE = 10
   ```

2. **Change to desired value**:
   ```python
   MAX_ENTRIES_PER_ARCHIVE = 20
   ```

### Adding New Template to Check

To check for additional templates on request pages:

1. **Add constant** in `domain/use_cases/check_request_status.py`:
   ```python
   PERSPECTIVE_TEMPLATE = "منظور"
   ADDITIONAL_TEMPLATE = "صورة أخرى"  # New
   ```

2. **Modify check logic**:
   ```python
   def _check_request(self, request: PhotoRequest) -> bool:
       has_perspective = self.wiki_repository.has_template(
           request.request_page_title,
           self.PERSPECTIVE_TEMPLATE
       )
       has_additional = self.wiki_repository.has_template(
           request.request_page_title,
           self.ADDITIONAL_TEMPLATE
       )
       return has_perspective or has_additional
   ```

### Modifying Archive Header

To change the archive page header format:

1. **Edit** `domain/entities/archive_entry.py` in `ArchivePage.get_header()`:
   ```python
   def get_header(self) -> str:
       return f"""{{{{أرشيف نقاش}}}}
   {{{{تصفح أرشيف|{self.page_number}}}}}
   {{{{تمت الأرشفة}}}}
   {{{{معلومات إضافية|تاريخ={datetime.now().strftime('%Y-%m-%d')}}}}}
   
   """
   ```

## Best Practices

### Code Style

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all classes and methods
- Maximum line length: 100 characters

### Testing

- Write unit tests for new entities
- Write unit tests for new use cases
- Use the mock repository for testing
- Ensure all tests pass before committing

### Logging

- Use appropriate log levels:
  - `DEBUG`: Detailed information for debugging
  - `INFO`: General information about operation
  - `WARNING`: Warning messages for recoverable issues
  - `ERROR`: Error messages for failures

Example:
```python
self.logger.debug(f"Processing request: {request.page_name}")
self.logger.info(f"Archived {count} requests")
self.logger.warning(f"Page not found: {page_title}")
self.logger.error(f"Failed to save: {str(e)}")
```

### Error Handling

- Catch specific exceptions first, general ones last
- Log errors with context
- Don't let one failure stop the entire process
- Return meaningful error messages

Example:
```python
try:
    result = operation()
except SpecificError as e:
    self.logger.error(f"Specific error: {str(e)}")
    # Handle specifically
except Exception as e:
    self.logger.exception(f"Unexpected error: {str(e)}")
    # Handle generally
```

### Documentation

- Update docstrings when modifying code
- Update relevant documentation files in `docs/`
- Add examples for new features

## Troubleshooting

### Common Issues

#### "No module named 'wikitextparser'"

**Solution**:
```bash
pip install wikitextparser
```

#### "Pywikibot configuration not found"

**Solution**:
Configure pywikibot following the official guide. Usually requires creating `user-config.py`.

#### "Page does not exist" errors

**Check**:
- Page title is correct (Arabic characters)
- Namespace is correct
- Page actually exists on the wiki

#### Tests fail with import errors

**Solution**:
```bash
# Run from project root
cd /home/lokas/PycharmProjects/pythonProject3/code
python -m unittest discover -s tasks/photo_lab/tests
```

### Debugging

#### Enable Debug Logging

```bash
python -m tasks.photo_lab.main --verbose
```

#### Dry Run Mode

Test changes without modifying the wiki:

```bash
python -m tasks.photo_lab.main --dry-run
```

#### Using Python Debugger

Add this to your code to start the debugger:

```python
import pdb; pdb.set_trace()
```

### Getting Help

- Check existing documentation in `docs/`
- Review similar tasks in `tasks/` directory
- Look at tests for usage examples

## See Also

- [README.md](README.md) - Overview
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture
- [WORKFLOW.md](WORKFLOW.md) - Workflow
- [API.md](API.md) - API Reference
- [TESTING.md](TESTING.md) - Testing Guide
