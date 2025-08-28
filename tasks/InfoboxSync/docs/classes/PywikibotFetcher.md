# PywikibotFetcher Class

## Class Reference

**Namespace**: `tasks.InfoboxSync.fetch.fetch`

**Inherits**: `WikipediaFetcher`

**Design Pattern**: Concrete Template Method Implementation

## Overview

Concrete implementation of `WikipediaFetcher` using the pywikibot library for direct Wikipedia API interactions. Handles page existence checking, content retrieval, and language link extraction from both Arabic and English Wikipedia sites.

## Constructor

```python
def __init__(self, site_name: str, observer: Optional[FetchObserver] = None):
    """
    Initialize pywikibot fetcher for specific wiki site.

    Args:
        site_name: Wiki site identifier ('ar' for Arabic, 'en' for English)
        observer: Optional observer for monitoring operations
    """
    super().__init__(observer)
    self.site_name = site_name
    self.site = None  # Lazy initialization
    self._initialize_site()
```

### Attributes

- **`site_name`**: `str` - Wiki site identifier ('ar' or 'en')
- **`site`**: `pywikibot.Site` - pywikibot site object (lazy-loaded)

## Core Methods

### `get_site_name() -> str`
Implements abstract method from parent class.
```python
def get_site_name(self) -> str:
    """Return site name identifier."""
    return self.site_name
```

### `_check_page_exists(page_title: str) -> PageInfo`
Checks if page exists and creates PageInfo with basic properties.
```python
def _check_page_exists(self, page_title: str) -> PageInfo:
    """
    Check page existence using pywikibot.

    Returns PageInfo with exists/content/error status.
    """
    try:
        import pywikibot
        page = pywikibot.Page(self.site, page_title)
        exists = page.exists()

        return PageInfo(
            title=page_title,
            exists=exists,
            content=page.text if exists else None
        )
    except Exception as e:
        logger.error(f"Error checking page existence: {e}")
        return PageInfo(title=page_title, exists=False, error=str(e))
```

### `_fetch_page_content(page_info: PageInfo) -> PageInfo`
Fetches full page content for pages that exist.
```python
def _fetch_page_content(self, page_info: PageInfo) -> PageInfo:
    """
    Fetch full page content.

    Optimization: Content is already fetched in _check_page_exists
    to minimize API calls, so this method is lightweight.
    """
    return page_info  # Content already available
```

### `_fetch_langlinks(page_info: PageInfo) -> PageInfo`
Retrieves interwiki links (language links) for existing pages.
```python
def _fetch_langlinks(page_info: PageInfo) -> PageInfo:
    """
    Fetch language links (interwiki links).

    Creates mapping like: {'ar': 'Arabic Title', 'en': 'English Title'}
    """
    try:
        import pywikibot
        if page_info.exists:
            page = pywikibot.Page(self.site, page_info.title)
            langlinks = {}
            for langlink in page.langlinks():
                langlinks[langlink.site.code] = langlink.title
            page_info.langlinks = langlinks
        return page_info
    except Exception as e:
        logger.error(f"Error fetching langlinks: {e}")
        page_info.langlinks = {}
        return page_info
```

## Private Methods

### `_initialize_site()`
Lazy initialization of pywikibot site object.
```python
def _initialize_site(self):
    """
    Initialize pywikibot site lazily.

    Only creates site object when first fetch operation occurs.
    """
    try:
        import pywikibot
        if self.site is None:
            self.site = pywikibot.Site(self.site_name)
            logger.info(f"Initialized pywikibot site: {self.site_name}")
    except ImportError:
        raise ImportError("pywikibot is required for Wikipedia operations. Install with: pip install pywikibot")
```

## Usage Patterns

### Basic Usage

```python
from tasks.InfoboxSync.fetch.fetch import PywikibotFetcher

# Create fetcher for Arabic Wikipedia
ar_fetcher = PywikibotFetcher('ar')

# Fetch page information
page_info = ar_fetcher.fetch_page_info("مصر")

if page_info.exists:
    print(f"Arabic page found: {page_info.title}")
    print(f"Content length: {len(page_info.content)} characters")
    print(f"Language links: {list(page_info.langlinks.keys())}")
else:
    print(f"Arabic page not found: {page_info.error}")
```

### Arabic-English Synchronization

```python
from tasks.InfoboxSync.fetch.fetch import PywikibotFetcher

# Create fetchers for both languages
ar_fetcher = PywikibotFetcher('ar')
en_fetcher = PywikibotFetcher('en')

def fetch_sync_pair(ar_title: str):
    """Fetch Arabic page and its English equivalent."""

    # Step 1: Fetch Arabic page
    ar_page = ar_fetcher.fetch_page_info(ar_title)

    if not ar_page.exists:
        return None, None

    # Step 2: Get English title from langlinks
    en_title = ar_page.langlinks.get('en') if ar_page.langlinks else None

    if not en_title:
        return ar_page, None

    # Step 3: Fetch English page
    en_page = en_fetcher.fetch_page_info(en_title)

    return ar_page, en_page

# Usage
arabic_page, english_page = fetch_sync_pair("مصر")  # Egypt
```

### Performance Monitoring

```python
from tasks.InfoboxSync.fetch.observers import MetricsFetchObserver

# Create fetcher with metrics monitoring
metrics_observer = MetricsFetchObserver()
fetcher = PywikibotFetcher('ar', observer=metrics_observer)

# Perform multiple fetches
pages = ["مصر", "باريس", "برلين"]
for page_title in pages:
    page_info = fetcher.fetch_page_info(page_title)

# Get performance statistics
stats = metrics_observer.get_metrics()
print(f"Total pages checked: {stats['pages_checked']}")
print(f"Successful fetches: {stats['pages_found']}")
print(f"Failure rate: {stats['pages_not_found']/stats['pages_checked']:.1%}")
```

## Error Handling

### Typical Error Scenarios

1. **Network Connection Issues**
   ```python
   # Handled in _initialize_site()
   ImportError: pywikibot is required...
   ```

2. **Page Access Issues**
   ```python
   # Handled in _check_page_exists()
   page_info.error = "Page access denied"  # For protected pages
   ```

3. **Language Link Issues**
   ```python
   # Handled in _fetch_langlinks()
   page_info.langlinks = {}  # On langlinks fetch failure
   ```

### Exception Handling Pattern

```python
def _check_page_exists(self, page_title: str) -> PageInfo:
    try:
        # Core operation
        return PageInfo(title=page_title, exists=True)
    except Exception as e:
        logger.error(f"Error checking page {page_title}: {e}")
        return PageInfo(title=page_title, exists=False, error=str(e))
```

## Performance Characteristics

### Optimization Strategies

1. **Lazy Site Initialization**
   ```python
   # Site object created only when first needed
   self.site = pywikibot.Site(self.site_name)  # On-demand creation
   ```

2. **Efficient Content Fetching**
   ```python
   # Content retrieved once in _check_page_exists()
   # _fetch_page_content() is lightweight
   return page_info  # No additional API call
   ```

3. **Minimal API Calls**
   ```python
   # Langlinks only fetched for existing pages
   if page_info.exists:
       # Fetch langlinks...
   ```

### Memory Management

```python
# pywikibot site object reused across operations
# No memory leaks from repeated object creation
self.site = pywikibot.Site(self.site_name)  # Single persistent object
```

## Integration Examples

### With WikipediaSyncFetcher

```python
from tasks.InfoboxSync.fetch.fetch import WikipediaSyncFetcher

# WikipediaSyncFetcher uses PywikibotFetcher internally
sync_fetcher = WikipediaSyncFetcher()

# This creates and configures PywikibotFetcher instances
result = sync_fetcher.fetch_arabic_and_english_pages("مصر")
```

### Custom Site Configurations

```python
class CustomPywikibotFetcher(PywikibotFetcher):
    """Customized pywikibot fetcher with specific settings."""

    def __init__(self, site_name: str, rate_limit: float = 0.1, observer=None):
        self.rate_limit = rate_limit
        super().__init__(site_name, observer)

    def _initialize_site(self):
        super()._initialize_site()
        # Apply custom settings
        if hasattr(self.site, 'throttle'):
            self.site.throttle.setDelay(self.rate_limit)
```

## Testing

### Unit Testing

```python
import unittest.mock as mock

def test_pywikibot_fetcher_initialization():
    """Test lazy site initialization."""
    fetcher = PywikibotFetcher('test')

    # Site should be None initially
    assert fetcher.site is None

    # Trigger initialization
    with mock.patch('pywikibot.Site') as mock_site:
        fetcher._initialize_site()
        mock_site.assert_called_once_with('test')
        assert fetcher.site is not None

def test_page_exists_check():
    """Test page existence checking."""
    fetcher = PywikibotFetcher('test')

    with mock.patch('pywikibot.Page') as mock_page:
        # Mock existing page
        mock_page_instance = mock.Mock()
        mock_page_instance.exists.return_value = True
        mock_page_instance.text = "Page content"
        mock_page.return_value = mock_page_instance

        result = fetcher._check_page_exists("Test Page")

        assert result.exists is True
        assert result.title == "Test Page"
        assert result.content == "Page content"
```

## Related Classes

- **Parent Class**: `WikipediaFetcher` (Abstract template method)
- **Sibling Classes**: Other concrete fetchers (RESTApiFetcher, etc.)
- **Data Models**: `PageInfo` (Result container)
- **Observers**: `FetchObserver`, `LoggingFetchObserver`, `MetricsFetchObserver`
- **Coordinators**: `WikipediaSyncFetcher` (Multi-language coordination)

## Configuration Requirements

### Pywikibot Setup

```bash
# Install pywikibot
pip install pywikibot

# Generate user configuration
pywikibot generate_user_files

# Configure user-config.py with:
# - Bot credentials
# - Site settings
# - API configurations
```

### Required Permissions

- **Read Access**: For page content and metadata retrieval
- **Rate Limits**: Respect Wikipedia API rate limiting
- **User Agent**: Proper user agent string for API identification

---

**File Location**: `tasks/InfoboxSync/fetch/fetch.py`
**Status**: Production-ready concrete implementation
**Dependencies**: `pywikibot`, `WikipediaFetcher` base class
**Since**: v1.0