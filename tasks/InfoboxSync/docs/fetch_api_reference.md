# Fetch Module API Reference

## Overview

This API reference provides comprehensive documentation for the Fetch module's public interfaces, data structures, and usage patterns. The fetch module enables bi-lingual Wikipedia data retrieval for Arabic-English infobox synchronization.

## Quick Start

```python
from tasks.InfoboxSync.fetch import fetch_wikipedia_data

# Basic usage - get Arabic page and its English equivalent
result = fetch_wikipedia_data("مصر")  # Returns dict with page data
```

## Main API Functions

### `fetch_wikipedia_data(ar_page_title: str) -> Dict[str, Any]`

**Primary Entry Point**: Main function for fetching bi-lingual Wikipedia data.

#### Parameters
- **`ar_page_title`** (`str`): Arabic Wikipedia page title to fetch

#### Returns
`Dict[str, Any]` with the following structure:
```python
{
    'arabic': PageInfo,          # Arabic page data (always present)
    'english': PageInfo | None,  # English page data (if found)
    'sync_possible': bool,       # True if sync can proceed
    'error': str | None         # Error message (if any)
}
```

#### Usage Examples

**Basic successful sync:**
```python
result = fetch_wikipedia_data("مصر")
if result['sync_possible']:
    arabic_content = result['arabic'].content
    english_content = result['english'].content
    print("Sync ready!")
```

**Handling failures:**
```python
result = fetch_wikipedia_data("NonExistentPage")
if not result['sync_possible']:
    print(f"Cannot proceed: {result['error']}")
```

### `fetch_sync_result(ar_page_title: str) -> SyncResult`

**Type-Safe Entry Point**: Returns structured `SyncResult` object instead of dictionary.

#### Parameters
- **`ar_page_title`** (`str`): Arabic Wikipedia page title

#### Returns
`SyncResult` dataclass:
```python
@dataclass
class SyncResult:
    arabic: PageInfo
    english: Optional[PageInfo]
    sync_possible: bool
    error: Optional[str]
```

#### Usage Example
```python
from tasks.InfoboxSync.fetch import fetch_sync_result

result = fetch_sync_result("خير الدين مضوي")
if result.sync_possible:
    # Type-safe access
    ar_title = result.arabic.title
    en_title = result.english.title
```

### `fetch_data(url: str) -> Dict[str, Any]` *(DEPRECATED)*

**Legacy Entry Point**: For backward compatibility. Extracts page title from Wikipedia URL.

#### Parameters
- **`url`** (`str`): Wikipedia page URL (e.g., "https://en.wikipedia.org/wiki/Egypt")

#### Usage
```python
# Extract page title from URL
result = fetch_data("https://ar.wikipedia.org/wiki/مصر")
```

#### Deprecation Warning
This function is deprecated. Use `fetch_wikipedia_data(page_title)` instead.

## Data Structures

### `PageInfo` Dataclass

Represents information about a Wikipedia page.

#### Attributes
```python
@dataclass
class PageInfo:
    title: str                    # Page title
    exists: bool                  # Whether page exists
    content: Optional[str] = None # Full page content in wikitext
    langlinks: Optional[Dict[str, str]] = None  # Language links
    error: Optional[str] = None   # Error message if fetch failed
```

#### Usage
```python
page = result['arabic']

# Check page status
if page.exists:
    content_length = len(page.content)
    has_langlinks = bool(page.langlinks)
else:
    error_message = page.error
```

#### Common Langlinks Structure
```python
page.langlinks = {
    'en': 'English Title',
    'fr': 'French Title',
    'de': 'German Title'
    # ... other language links
}
```

## Advanced Classes

### `WikipediaSyncFetcher`

Main orchestration class for bi-lingual page fetching.

#### Constructor
```python
WikipediaSyncFetcher(observer: Optional[FetchObserver] = None)
```

#### Key Methods

**`fetch_arabic_and_english_pages(ar_page_title: str) -> Dict[str, Any]`**
- Core method with custom observer support
- Returns same format as `fetch_wikipedia_data()`

**`fetch_sync_result(ar_page_title: str) -> SyncResult`**
- Type-safe version of above method

#### Advanced Usage
```python
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher
from tasks.InfoboxSync.fetch.observers import MetricsFetchObserver

# Create with monitoring
observer = MetricsFetchObserver()
fetcher = WikipediaSyncFetcher(observer=observer)

# Fetch data
result = fetcher.fetch_arabic_and_english_pages("مصر")

# Get performance metrics
stats = observer.get_metrics()
print(f"Pages processed: {stats['pages_checked']}")
```

### `PywikibotFetcher`

Concrete fetcher implementation using pywikibot library.

#### Constructor
```python
PywikibotFetcher(site_name: str, observer: Optional[FetchObserver] = None)
```

#### Parameters
- **`site_name`**: Wikipedia site identifier ('ar' for Arabic, 'en' for English)

#### Usage
```python
from tasks.InfoboxSync.fetch.fetch import PywikibotFetcher

# Arabic Wikipedia fetcher
ar_fetcher = PywikibotFetcher('ar')

# Fetch single page
page = ar_fetcher.fetch_page_info("مصر")
print(f"Content length: {len(page.content)}")
```

## Observer Pattern

### `FetchObserver` Interface

Abstract base class for monitoring fetch operations.

#### Key Methods
```python
class FetchObserver(ABC):
    def on_page_check_start(self, page_title: str, site: str):
        """Called when page fetch begins."""
        pass

    def on_page_check_complete(self, page_info: PageInfo):
        """Called when page fetch completes."""
        pass

    def on_error(self, error: str):
        """Called when errors occur."""
        pass
```

### Built-in Observers

#### `LoggingFetchObserver`
Default observer that logs all fetch operations to configured logger.

#### `MetricsFetchObserver`
Collects performance metrics for monitoring and analysis.

**Metrics collected:**
```python
{
    'pages_checked': int,     # Total pages processed
    'pages_found': int,       # Pages that exist
    'pages_not_found': int,   # Pages that don't exist
    'errors': int            # Total errors encountered
}
```

#### Usage
```python
from tasks.InfoboxSync.fetch.observers import MetricsFetchObserver

observer = MetricsFetchObserver()

# Use with any fetcher
fetcher = WikipediaSyncFetcher(observer=observer)

# After operations
stats = observer.get_metrics()
success_rate = stats['pages_found'] / stats['pages_checked']
```

## Error Handling

### Common Error Scenarios

#### 1. Arabic Page Not Found
```python
result = fetch_wikipedia_data("NonExistentArabicPage")
# Result: {'sync_possible': False, 'error': "Arabic page 'NonExistentArabicPage' does not exist"}
```

#### 2. No English Equivalent
```python
result = fetch_wikipedia_data("UniqueArabicTerm")
# Result: {'sync_possible': False, 'error': "No corresponding English page found"}
```

#### 3. Network/API Errors
```python
result = fetch_wikipedia_data("مصر")  # During network outage
# Result: {'arabic': PageInfo(exists=False, error="Network timeout"), ...}
```

### Error Handling Pattern

```python
def robust_fetch(ar_page_title: str):
    """Robust fetch with comprehensive error handling."""
    try:
        result = fetch_wikipedia_data(ar_page_title)

        if not result['sync_possible']:
            error_msg = result.get('error', 'Unknown error')

            # Categorize and handle specific errors
            if 'does not exist' in error_msg:
                # Handle missing Arabic page
                return handle_missing_page(ar_page_title)
            elif 'No corresponding English' in error_msg:
                # Handle missing English equivalent
                return attempt_alternative_lookup(ar_page_title)
            else:
                # Log for investigation
                logger.error(f"Sync failed for {ar_page_title}: {error_msg}")
                return None

        return result

    except Exception as e:
        logger.error(f"Unexpected error fetching {ar_page_title}: {e}")
        return None
```

## Configuration

### Pywikibot Setup

**Required for all fetch operations:**

```bash
# Install pywikibot
pip install pywikibot

# Generate user configuration
pywikibot generate_user_files

# Configure user-config.py with:
# - Bot credentials (mylang, family)
# - User agent settings
# - Rate limiting preferences
```

### Environment Considerations

#### Rate Limiting
```python
# Respect Wikipedia API limits
# Default: ~100 requests/hour per IP
# Bot accounts may have higher limits
```

#### User Agent
```python
# Set descriptive user agent for API requests
# Identifies your application to Wikipedia
```

## Performance Guidelines

### Efficient Usage Patterns

#### 1. Reuse Fetcher Instances
```python
# Good: Reuse instance
fetcher = WikipediaSyncFetcher()
result1 = fetcher.fetch_arabic_and_english_pages("مصر")
result2 = fetcher.fetch_arabic_and_english_pages("باريس")

# Bad: Create new instance each time (slower)
result1 = WikipediaSyncFetcher().fetch_arabic_and_english_pages("مصر")
result2 = WikipediaSyncFetcher().fetch_arabic_and_english_pages("باريس")
```

#### 2. Batch Processing
```python
# Process multiple pages efficiently
pages = ["مصر", "باريس", "برلين"]
results = {}

fetcher = WikipediaSyncFetcher()
for page in pages:
    results[page] = fetcher.fetch_arabic_and_english_pages(page)
```

#### 3. Lazy Initialization
```python
# Connections established only when needed
fetcher = WikipediaSyncFetcher()  # No API calls yet
result = fetcher.fetch_arabic_and_english_pages("مصر")  # API calls happen here
```

## Testing

### Unit Testing Examples

#### Mock Successful Fetch
```python
import unittest.mock as mock

def test_successful_sync():
    from tasks.InfoboxSync.fetch import fetch_wikipedia_data

    # Mock the internal fetcher
    with mock.patch('tasks.InfoboxSync.fetch.sync_fetcher.WikipediaSyncFetcher') as MockFetcher:
        mock_instance = MockFetcher.return_value

        # Setup mock return
        mock_result = {
            'arabic': PageInfo(title="مصر", exists=True, content="محتوى"),
            'english': PageInfo(title="Egypt", exists=True, content="Content"),
            'sync_possible': True,
            'error': None
        }
        mock_instance.fetch_arabic_and_english_pages.return_value = mock_result

        # Test
        result = fetch_wikipedia_data("مصر")
        assert result['sync_possible'] is True
        assert result['arabic'].title == "مصر"
```

## Migration Guide

### From Legacy Usage
```python
# Old way (deprecated)
from tasks.InfoboxSync.fetch import fetch_data
result = fetch_data("https://ar.wikipedia.org/wiki/مصر")

# New way (recommended)
from tasks.InfoboxSync.fetch import fetch_wikipedia_data
result = fetch_wikipedia_data("مصر")
```

### From Direct Pywikibot
```python
# Old way: Direct pywikibot usage
import pywikibot
site = pywikibot.Site('ar')
page = pywikibot.Page(site, 'مصر')
content = page.text

# New way: Abstracted interface
from tasks.InfoboxSync.fetch import fetch_wikipedia_data
result = fetch_wikipedia_data("مصر")
content = result['arabic'].content
```

## Best Practices

### 1. Error Handling
```python
# Always check sync_possible before processing
result = fetch_wikipedia_data(page_title)
if not result['sync_possible']:
    handle_sync_failure(result['error'])
    return

# Safe to access page content
arabic_content = result['arabic'].content
english_content = result['english'].content
```

### 2. Resource Management
```python
# Use context managers for batch operations
class BatchProcessor:
    def __init__(self):
        self.fetcher = WikipediaSyncFetcher()

    def process_pages(self, page_list):
        results = []
        for page in page_list:
            result = self.fetcher.fetch_arabic_and_english_pages(page)
            results.append(result)
        return results
```

### 3. Monitoring Integration
```python
# Integrate with monitoring systems
observer = MetricsFetchObserver()
fetcher = WikipediaSyncFetcher(observer=observer)

# Operations...

# Report to monitoring system
stats = observer.get_metrics()
monitoring_system.record('wiki_fetch_success_rate', stats['pages_found'] / stats['pages_checked'])
```

## Related Modules

- **Parse Module**: Use fetched content with `parse_data()`
- **Observer Module**: Custom monitoring implementations
- **Models Module**: Data structure definitions

See also: `fetch_stage.md` for detailed architecture and design pattern documentation.