# Photo Lab - Testing Guide

This guide covers how to test the Photo Lab task, including unit tests, integration tests, and manual testing procedures.

## Table of Contents

- [Testing Overview](#testing-overview)
- [Running Tests](#running-tests)
- [Unit Tests](#unit-tests)
- [Mock Repository](#mock-repository)
- [Writing New Tests](#writing-new-tests)
- [Integration Testing](#integration-testing)
- [Manual Testing](#manual-testing)
- [Test Coverage](#test-coverage)

## Testing Overview

The Photo Lab task uses Python's built-in `unittest` framework for testing. The testing strategy follows the Clean Architecture principles:

- **Unit Tests**: Test individual components in isolation
- **Mock Repository**: Fake implementation for testing without wiki access
- **Integration Tests**: Test components working together (optional)

### Test Directory Structure

```
tasks/photo_lab/tests/
├── __init__.py
├── mock_wiki_repository.py    # Mock implementation
├── test_photo_request.py       # PhotoRequest tests
├── test_archive_entry.py       # ArchiveEntry tests
└── test_use_cases.py           # Use case tests
```

## Running Tests

### Run All Tests

```bash
cd /home/lokas/PycharmProjects/pythonProject3/code
python -m unittest discover -s tasks/photo_lab/tests -v
```

### Run Specific Test File

```bash
python -m unittest tasks.photo_lab.tests.test_photo_request -v
```

### Run Specific Test Class

```bash
python -m unittest tasks.photo_lab.tests.test_photo_request.TestPhotoRequest -v
```

### Run Specific Test Method

```bash
python -m unittest tasks.photo_lab.tests.test_photo_request.TestPhotoRequest.test_create_photo_request -v
```

## Unit Tests

### PhotoRequest Tests

**File**: `tests/test_photo_request.py`

Tests the `PhotoRequest` entity:

| Test | Description |
|------|-------------|
| `test_create_photo_request` | Test basic construction |
| `test_request_page_title_auto_generation` | Test auto-generated page title |
| `test_mark_as_archivable` | Test marking as ready |
| `test_str_representation` | Test string output |
| `test_repr` | Test detailed representation |

### ArchiveEntry Tests

**File**: `tests/test_archive_entry.py`

Tests the `ArchiveEntry` and `ArchivePage` entities:

#### ArchiveEntry Tests

| Test | Description |
|------|-------------|
| `test_create_archive_entry` | Test construction |
| `test_get_archive_page_title` | Test page title generation |
| `test_format_for_archive` | Test formatting |

#### ArchivePage Tests

| Test | Description |
|------|-------------|
| `test_create_archive_page` | Test construction |
| `test_is_full_empty` | Test empty archive |
| `test_is_full_at_limit` | Test at capacity |
| `test_is_full_over_limit` | Test over capacity |
| `test_add_entry` | Test adding entries |
| `test_get_header` | Test header generation |
| `test_get_content` | Test content generation |

### Use Case Tests

**File**: `tests/test_use_cases.py`

Tests the use cases with the mock repository:

#### ExtractPendingRequests Tests

| Test | Description |
|------|-------------|
| `test_extract_single_request` | Extract one request |
| `test_extract_multiple_requests` | Extract many requests |
| `test_extract_no_requests` | Handle empty page |
| `test_extract_empty_page` | Handle no content |

#### CheckRequestStatus Tests

| Test | Description |
|------|-------------|
| `test_request_with_perspective` | Has perspective template |
| `test_request_without_perspective` | No perspective template |
| `test_get_archivable_requests` | Filter archivable |

#### ManageArchives Tests

| Test | Description |
|------|-------------|
| `test_create_first_archive` | First archive creation |
| `test_get_existing_archive` | Use existing archive |
| `test_create_new_when_full` | Create when full |
| `test_add_entry_to_archive` | Add entry |
| `test_find_latest_archive_number` | Find latest |

## Mock Repository

### MockWikiRepository

**File**: `tests/mock_wiki_repository.py`

The `MockWikiRepository` class provides a fake implementation of the `WikiRepository` interface for testing.

#### Features

- In-memory page storage
- Template counting simulation
- Archive page tracking
- No network calls

#### Usage

```python
from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository
from tasks.photo_lab.domain.use_cases.extract_pending_requests import ExtractPendingRequests

# Create mock repository
mock_repo = MockWikiRepository()

# Set up test data
mock_repo.add_page(
    "ويكيبيديا:ورشة الصور/طلبات",
    "{{طلب ورشة صور|Test Page}}"
)

# Use in tests
use_case = ExtractPendingRequests(mock_repo)
requests = use_case.execute()

# Assert results
assert len(requests) == 1
assert requests[0].page_name == "Test Page"
```

#### Methods

| Method | Description |
|--------|-------------|
| `add_page(title, content)` | Add a page to mock storage |
| `add_template_to_page(title, template, count)` | Set template count |
| `add_archive_page(number, title)` | Add archive page |

## Writing New Tests

### Test Template

```python
"""
Tests for [Component Name].
"""

import unittest

from tasks.photo_lab.domain.entities.[entity] import [Entity]
from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository


class Test[Entity](unittest.TestCase):
    """Test cases for [Entity]."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize common test data
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_[specific_behavior](self):
        """Test [what is being tested]."""
        # Arrange
        input_data = ...
        expected = ...
        
        # Act
        result = function(input_data)
        
        # Assert
        self.assertEqual(result, expected)
    
    def test_[edge_case](self):
        """Test [edge case description]."""
        # Test edge case
        pass


if __name__ == '__main__':
    unittest.main()
```

### Testing Entities

```python
import unittest
from tasks.photo_lab.domain.entities.photo_request import PhotoRequest


class TestPhotoRequest(unittest.TestCase):
    """Test PhotoRequest entity."""
    
    def test_mark_as_archivable(self):
        """Test marking request as ready."""
        # Arrange
        request = PhotoRequest(
            page_name="Test",
            template_text="{{...}}"
        )
        
        # Pre-condition
        self.assertFalse(request.has_perspective)
        
        # Act
        request.mark_as_archivable()
        
        # Assert
        self.assertTrue(request.has_perspective)
        self.assertTrue(request.is_ready_for_archive())
```

### Testing Use Cases

```python
import unittest
from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository
from tasks.photo_lab.domain.use_cases.extract_pending_requests import ExtractPendingRequests


class TestExtractPendingRequests(unittest.TestCase):
    """Test extract use case."""
    
    def setUp(self):
        """Set up mock repository."""
        self.mock_repo = MockWikiRepository()
        self.use_case = ExtractPendingRequests(self.mock_repo)
    
    def test_extract_single_request(self):
        """Test extracting one request."""
        # Arrange
        content = "{{طلب ورشة صور|Test Page}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        # Act
        requests = self.use_case.execute()
        
        # Assert
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].page_name, "Test Page")
```

### Testing with Exceptions

```python
def test_handles_missing_page(self):
    """Test behavior when page doesn't exist."""
    # Don't add the page - simulate missing page
    
    # Act & Assert
    with self.assertRaises(Exception):
        self.use_case.execute()
```

## Integration Testing

Integration tests verify that components work together correctly. These may require actual wiki access or a more sophisticated mock.

### Integration Test Example

```python
"""
Integration tests for photo lab workflow.
"""

import unittest
from tasks.photo_lab.presentation.controllers.photo_lab_controller import PhotoLabController
from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository


class TestPhotoLabWorkflow(unittest.TestCase):
    """Test complete workflow."""
    
    def test_full_workflow(self):
        """Test complete archiving workflow."""
        # Set up test data
        mock_repo = MockWikiRepository()
        
        # Main page with two requests
        mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            "{{طلب ورشة صور|Page 1}}\n{{طلب ورشة صور|Page 2}}"
        )
        
        # Page 1 has perspective (ready)
        mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/Page 1",
            "{{منظور}}"
        )
        mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/طلبات/Page 1",
            "منظور",
            1
        )
        
        # Page 2 doesn't have perspective (not ready)
        mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/Page 2",
            "No perspective yet"
        )
        
        # Run controller
        controller = PhotoLabController(mock_repo)
        results = controller.run()
        
        # Verify results
        self.assertTrue(results['success'])
        self.assertEqual(results['total_requests'], 2)
        self.assertEqual(results['archivable_requests'], 1)
        self.assertEqual(len(results['archived']), 1)
        self.assertEqual(results['archived'][0], "Page 1")
```

## Manual Testing

### Dry Run Mode

Test the bot without making changes:

```bash
python -m tasks.photo_lab.main --dry-run --verbose
```

Expected output:
```
INFO: Extracting requests from ويكيبيديا:ورشة الصور/طلبات
INFO: Found 5 pending requests
INFO: Found 2 requests ready for archiving
INFO: Would archive: ['Page 1', 'Page 2']
```

### Testing on a Sandbox Page

1. Create a test page on your user sandbox
2. Temporarily modify the code to use sandbox page
3. Run the bot
4. Verify changes
5. Revert code changes

Example modification in `extract_pending_requests.py`:
```python
# Temporarily change for testing
MAIN_PAGE_TITLE = "مستخدم:YourUsername/صندوق رمل/طلبات"
```

### Verification Checklist

When testing manually, verify:

- [ ] Main page is read correctly
- [ ] All requests are extracted
- [ ] Perspective template detection works
- [ ] Archive pages are found/created correctly
- [ ] Archive page format is correct
- [ ] Templates are removed from main page
- [ ] Edit summaries are appropriate

## Test Coverage

### Current Coverage

| Component | Tests | Status |
|-----------|-------|--------|
| PhotoRequest | 5 | ✓ Complete |
| ArchiveEntry | 3 | ✓ Complete |
| ArchivePage | 7 | ✓ Complete |
| ExtractPendingRequests | 4 | ✓ Complete |
| CheckRequestStatus | 3 | ✓ Complete |
| ManageArchives | 5 | ✓ Complete |

### Coverage Goals

Aim for:
- **100%** entity method coverage
- **90%+** use case line coverage
- **All** public API methods tested

### Measuring Coverage

Install coverage tool:
```bash
pip install coverage
```

Run with coverage:
```bash
coverage run -m unittest discover -s tasks/photo_lab/tests
coverage report
coverage html  # Generate HTML report
```

## Debugging Failed Tests

### Enable Verbose Output

```bash
python -m unittest discover -s tasks/photo_lab/tests -v 2>&1
```

### Debug Single Test

Add debug prints or use debugger:

```python
def test_something(self):
    result = function()
    print(f"DEBUG: result = {result}")  # Add debug output
    self.assertEqual(result, expected)
```

### Common Test Failures

| Issue | Cause | Solution |
|-------|-------|----------|
| ImportError | Missing dependencies | `pip install wikitextparser` |
| AssertionError | Wrong expected value | Check test data |
| KeyError | Missing page in mock | Call `add_page()` first |
| AttributeError | Wrong attribute name | Check entity definition |

## Continuous Integration

When adding tests to CI/CD:

```yaml
# Example GitHub Actions snippet
- name: Run Photo Lab Tests
  run: |
    python -m unittest discover \
      -s tasks/photo_lab/tests \
      -v
```

## See Also

- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
- [README.md](README.md) - Overview
- Python unittest documentation: https://docs.python.org/3/library/unittest.html
