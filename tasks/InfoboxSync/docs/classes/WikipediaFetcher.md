# WikipediaFetcher Class

## Class Reference

**Namespace**: `tasks.InfoboxSync.fetch.interfaces` or `tasks.InfoboxSync.fetch.fetch`

**Inherits**: `ABC` (Abstract Base Class)

**Design Pattern**: Template Method Pattern

## Overview

Abstract base class that defines the skeletal structure for Wikipedia page fetching operations. Uses the Template Method pattern to provide a common algorithm for fetching page information while allowing subclasses to customize specific steps.

## Constructor

```python
def __init__(self, observer: Optional[FetchObserver] = None):
    """
    Initialize the Wikipedia fetcher.

    Args:
        observer: Optional observer for monitoring fetch operations
    """
```

### Attributes

- **`observer`**: `FetchObserver` - Observer instance for monitoring operations
- **`site_name`**: `str` - Name identifier for the wiki site (set by subclasses)

## Abstract Methods

### `get_site_name() -> str`
**Must be implemented by subclasses**

Returns the site name identifier for this fetcher.
```python
def get_site_name(self) -> str:
    """Return the site name identifier (e.g., 'ar', 'en')."""
    pass
```

### `_check_page_exists(page_title: str) -> PageInfo`
**Must be implemented by subclasses**

Checks if a Wikipedia page exists and creates a PageInfo object.
```python
def _check_page_exists(self, page_title: str) -> PageInfo:
    """Check page existence and return PageInfo."""
    pass
```

### `_fetch_page_content(page_info: PageInfo) -> PageInfo`
**Must be implemented by subclasses**

Retrieves the full page content for existing pages.
```python
def _fetch_page_content(self, page_info: PageInfo) -> PageInfo:
    """Fetch full page content."""
    pass
```

### `_fetch_langlinks(page_info: PageInfo) -> PageInfo`
**Must be implemented by subclasses**

Retrieves language links (interwiki links) for existing pages.
```python
def _fetch_langlinks(page_info: PageInfo) -> PageInfo:
    """Fetch language links (interwiki links)."""
    pass
```

## Template Method

### `fetch_page_info(page_title: str) -> PageInfo`

**Template Method Pattern Implementation**

The main orchestration method that defines the fetch algorithm:

```python
def fetch_page_info(self, page_title: str) -> PageInfo:
    """
    Template method: Main page fetching algorithm.

    Algorithm:
    1. Check page existence
    2. If exists: fetch content and langlinks
    3. Notify observer and return result
    """
    # Step 1: Notify start
    self.observer.on_page_check_start(page_title, self.get_site_name())

    # Step 2: Check existence
    page_info = self._check_page_exists(page_title)

    # Step 3: If exists, fetch additional data
    if page_info.exists:
        page_info = self._fetch_page_content(page_info)
        page_info = self._fetch_langlinks(page_info)

    # Step 4: Notify completion and return
    self.observer.on_page_check_complete(page_info)
    return page_info
```

## Implementation Examples

### Concrete Implementation Pattern

```python
class CustomWikipediaFetcher(WikipediaFetcher):
    def __init__(self, site_name: str, observer=None):
        super().__init__(observer)
        self.site_name = site_name

    def get_site_name(self) -> str:
        return self.site_name

    def _check_page_exists(self, page_title: str) -> PageInfo:
        # Custom implementation
        return PageInfo(title=page_title, exists=True)

    def _fetch_page_content(self, page_info: PageInfo) -> PageInfo:
        # Custom implementation
        page_info.content = "Sample content"
        return page_info

    def _fetch_langlinks(self, page_info: PageInfo) -> PageInfo:
        # Custom implementation
        page_info.langlinks = {"en": "English Title"}
        return page_info
```

## Usage Examples

### Basic Usage

```python
from tasks.InfoboxSync.fetch.fetch import WikipediaFetcher

# Create concrete fetcher
fetcher = PywikibotFetcher('ar')

# Fetch page information
page_info = fetcher.fetch_page_info("مصر")

# Check results
if page_info.exists:
    print(f"Page content: {len(page_info.content)} characters")
    print(f"Langlinks: {page_info.langlinks}")
else:
    print(f"Page not found: {page_info.error}")
```

### With Custom Observer

```python
from tasks.InfoboxSync.fetch.observers import MetricsFetchObserver

# Create fetcher with metrics observer
metrics_observer = MetricsFetchObserver()
fetcher = PywikibotFetcher('en', observer=metrics_observer)

# Fetch multiple pages
pages = ['Egypt', 'France', 'Germany']
for page in pages:
    page_info = fetcher.fetch_page_info(page)

# Get metrics
stats = metrics_observer.get_metrics()
print(f"Pages checked: {stats['pages_checked']}")
print(f"Success rate: {stats['pages_found']/stats['pages_checked']:.1%}")
```

## Error Handling

The template method includes comprehensive error handling:

```python
def fetch_page_info(self, page_title: str) -> PageInfo:
    try:
        # Main algorithm...
        return page_info
    except Exception as e:
        error_msg = f"Error fetching page '{page_title}': {str(e)}"
        self.observer.on_error(error_msg)
        return PageInfo(title=page_title, exists=False, error=error_msg)
```

## Extension Points

### Adding New Wiki Sources

```python
class RESTApiFetcher(WikipediaFetcher):
    """Wikipedia fetcher using REST API instead of pywikibot."""

    def __init__(self, api_url: str, observer=None):
        super().__init__(observer)
        self.api_url = api_url

    def get_site_name(self) -> str:
        return "custom"

    def _check_page_exists(self, page_title: str) -> PageInfo:
        # REST API implementation
        response = requests.get(f"{self.api_url}/page/{page_title}")
        return PageInfo(
            title=page_title,
            exists=response.status_code == 200
        )

    def _fetch_page_content(self, page_info: PageInfo) -> PageInfo:
        # REST API implementation
        page_info.content = "REST API content"
        return page_info

    def _fetch_langlinks(self, page_info: PageInfo) -> PageInfo:
        # REST API implementation
        page_info.langlinks = {"en": "English Title"}
        return page_info
```

### Custom Observers

```python
class PerformanceObserver(FetchObserver):
    """Observer that measures fetch performance."""

    def __init__(self):
        self.request_times = []
        self.start_time = None

    def on_page_check_start(self, page_title: str, site: str):
        self.start_time = time.time()

    def on_page_check_complete(self, page_info: PageInfo):
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.request_times.append(elapsed)
            self.start_time = None

    def get_average_response_time(self) -> float:
        return sum(self.request_times) / len(self.request_times) if self.request_times else 0
```

## Testing

### Unit Testing the Template Method

```python
import unittest.mock as mock

def test_template_method():
    # Mock subclass implementation
    fetcher = mock.Mock(spec=WikipediaFetcher)

    # Setup mock return values
    page_info = PageInfo(title="Test", exists=True)
    fetcher.get_site_name.return_value = "test"
    fetcher._check_page_exists.return_value = page_info
    fetcher._fetch_page_content.return_value = page_info
    fetcher._fetch_langlinks.return_value = page_info

    # Call template method on real base class
    base_fetcher = WikipediaFetcher()
    result = base_fetcher.fetch_page_info("test")

    # Verify template method called hooks in correct order
    fetcher._check_page_exists.assert_called_once()
    fetcher._fetch_page_content.assert_called_once()
    fetcher._fetch_langlinks.assert_called_once()

def test_error_handling():
    fetcher = WikipediaFetcher()
    page_info = fetcher._check_page_exists("NonExistent")
    assert not page_info.exists
    assert page_info.error is not None
```

## Related Classes

- **Concrete Implementations**: `PywikibotFetcher` (Main concrete implementation)
- **Data Models**: `PageInfo`, `SyncResult`
- **Observers**: `FetchObserver`, `LoggingFetchObserver`, `MetricsFetchObserver`
- **Coordinators**: `WikipediaSyncFetcher` (Uses multiple WikipediaFetcher instances)

---

**File Location**: `tasks/InfoboxSync/fetch/interfaces.py` (interface) and `tasks/InfoboxSync/fetch/fetch.py` (base implementation)
**Status**: Abstract Base Class - must be subclassed
**Since**: v1.0