# Fetch Stage Documentation

## Overview

The Fetch stage is the first component of the InfoboxSync pipeline. It is responsible for retrieving Wikipedia page data from both Arabic and English Wikipedia sites, establishing the foundation for the synchronization process. This stage ensures that the required pages exist and gathers their content and metadata for further processing.

## Design Patterns Used

### 1. Template Method Pattern
- **Base Class**: `WikipediaFetcher` (abstract)
- **Implementation**: Defined in `interfaces.py` and implemented in `fetch.py`
- **Purpose**: Defines the skeleton of the page fetching algorithm while allowing subclasses to customize specific steps
- **Hook Methods**:
  - `get_site_name()` - Returns the site identifier
  - `_check_page_exists()` - Checks if page exists on the wiki
  - `_fetch_page_content()` - Retrieves full page content
  - `_fetch_langlinks()` - Fetches language links (interwiki links)

### 2. Observer Pattern
- **Subject**: `WikipediaFetcher` classes
- **Observer Interface**: `FetchObserver` (abstract base class)
- **Observers**:
  - `LoggingFetchObserver` - Logs fetch operations
  - `MetricsFetchObserver` - Collects performance metrics
- **Purpose**: Enables monitoring and logging of fetch operations without coupling the fetchers to specific monitoring implementations

### 3. Strategy Pattern
- **Context**: `WikipediaSyncFetcher`
- **Strategies**:
  - `PywikibotFetcher` for Arabic Wikipedia
  - `PywikibotFetcher` for English Wikipedia
- **Purpose**: Allows different fetch strategies for different Wikipedia languages and implementations

## Core Classes and Components

### Data Models

#### PageInfo
```python
@dataclass
class PageInfo:
    title: str                    # Page title
    exists: bool                  # Whether page exists on wiki
    content: Optional[str]        # Full wikitext content
    langlinks: Optional[Dict[str, str]]  # Language links (e.g., {'en': 'English Title'})
    error: Optional[str]          # Error message if operation failed
```

#### SyncResult
```python
@dataclass
class SyncResult:
    arabic: PageInfo             # Arabic Wikipedia page info
    english: Optional[PageInfo]  # English Wikipedia page info
    sync_possible: bool          # Whether sync can proceed
    error: Optional[str]         # Error message if sync not possible
```

### Fetch Strategy Implementations

#### PywikibotFetcher
- **Purpose**: Concrete implementation using pywikibot library
- **Features**:
  - Lazy initialization of pywikibot sites
  - Efficient page existence checking
  - Content and langlinks retrieval
  - Comprehensive error handling

#### Key Methods:
- `fetch_page_info()` - Main template method implementation
- `_check_page_exists()` - Uses pywikibot.Page.exists()
- `_fetch_page_content()` - Retrieves page.text
- `_fetch_langlinks()` - Parses page.langlinks()

### Observer Implementations

#### LoggingFetchObserver
- Logs all fetch operations
- Provides debug information for troubleshooting
- Tracks page check start/completion/error events

#### MetricsFetchObserver
- Collects performance metrics:
  - `pages_checked`: Total pages checked
  - `pages_found`: Pages that exist
  - `pages_not_found`: Pages that don't exist
  - `errors`: Total errors encountered

## Core Fetch Flow

### 1. Arabic Page Check
```python
# Step 1: Check if Arabic page exists
ar_page_info = self.ar_fetcher.fetch_page_info(ar_page_title)
if not ar_page_info.exists:
    return {
        'sync_possible': False,
        'error': f"Arabic page '{ar_page_title}' does not exist"
    }
```

### 2. English Page Discovery
```python
# Step 2: Find corresponding English page
en_page_title = self._find_english_page_title(ar_page_info)
```

**English Page Discovery Methods:**
1. **Primary**: Check langlinks from Arabic page (`ar_page_info.langlinks['en']`)
2. **Fallback**: Direct title match (same title in both languages)

### 3. English Page Fetch
```python
# Step 3: Fetch English page content
en_page_info = self.en_fetcher.fetch_page_info(en_page_title)
```

## API Usage

### Main Entry Points

#### fetch_wikipedia_data()
```python
def fetch_wikipedia_data(ar_page_title: str) -> Dict[str, Any]:
    """
    Main function to fetch Wikipedia data for sync operation.

    Args:
        ar_page_title: Arabic page title to sync

    Returns:
        Dictionary with Arabic and English page data
    """
```

**Return Format:**
```python
{
    'arabic': PageInfo(...),      # Arabic page information
    'english': PageInfo(...),     # English page information
    'sync_possible': bool,        # Whether sync can proceed
    'error': str or None         # Error message if any
}
```

**Usage Example:**
```python
from fetch.fetch import fetch_wikipedia_data

result = fetch_wikipedia_data("محمد بن سلمان")
if result['sync_possible']:
    arabic_page = result['arabic']
    english_page = result['english']
    print(f"Arabic: {arabic_page.title}")
    print(f"English: {english_page.title}")
    print(f"Content length: {len(english_page.content)}")
```

### Advanced Usage with Custom Observers

```python
from fetch.observers import MetricsFetchObserver
from fetch.fetch import WikipediaSyncFetcher

# Use metrics observer for monitoring
metrics_observer = MetricsFetchObserver()
fetcher = WikipediaSyncFetcher(observer=metrics_observer)

result = fetcher.fetch_arabic_and_english_pages("مصر")

# Get performance metrics
metrics = metrics_observer.get_metrics()
print(f"Pages checked: {metrics['pages_checked']}")
print(f"Success rate: {metrics['pages_found']/metrics['pages_checked']:.2%}")
```

## Error Handling

The fetch stage includes comprehensive error handling:

### Common Error Scenarios:
1. **Arabic page doesn't exist** → `sync_possible: False`
2. **No English equivalent found** → `sync_possible: False`
3. **English page doesn't exist** → `sync_possible: False`
4. **Network/API errors** → Logged and handled gracefully
5. **Pywikibot configuration issues** → Clear error messages

### Error Recovery:
- Each fetch operation is isolated
- Errors don't cascade between Arabic and English fetches
- Failed fetches provide detailed error messages
- Logging provides debugging information

## Dependencies

- **pywikibot**: Wikipedia API integration
  - Page existence checking
  - Content retrieval
  - Language links extraction
- **Standard Library**: `logging`, `typing`, `dataclasses`

## Configuration Requirements

### Pywikibot Setup:
```bash
# Generate user configuration
pywikibot generate_user_files

# Configure user-config.py with bot credentials
# Set up family and mylang settings for Wikipedia access
```

### Environment Setup:
- Ensure pywikibot is properly configured for both Arabic and English Wikipedia
- Bot account with appropriate permissions for read operations
- Network access to Wikipedia APIs

## Performance Considerations

### Optimization Strategies:
1. **Lazy Initialization**: pywikibot sites initialized only when needed
2. **Efficient Content Fetching**: Content retrieved together with existence check
3. **Minimal API Calls**: Langlinks fetched only for existing pages
4. **Observer Pattern**: Monitoring doesn't impact fetch performance

### Metrics Collection:
- Pages checked per operation
- Success/failure rates
- Error frequencies
- Performance timing (through logging)

## Extension Points

### Adding New Wikipedia Languages:
```python
class GermanFetcher(PywikibotFetcher):
    def get_site_name(self) -> str:
        return 'de'
```

### Custom Observers:
```python
class CustomMetricsObserver(FetchObserver):
    def on_page_check_complete(self, page_info: PageInfo):
        # Custom monitoring logic
        send_to_monitoring_system(page_info)
```

### Alternative Fetch Implementations:
```python
class RESTFetcher(WikipediaFetcher):
    """Wikipedia API-based fetcher as alternative to pywikibot"""
    def _check_page_exists(self, page_title: str) -> PageInfo:
        # REST API implementation
        pass
```

## Testing and Validation

### Test Scenarios:
- Existing Arabic page with English equivalent
- Non-existent Arabic page
- Arabic page without English equivalent
- Network connectivity issues
- API rate limiting
- Malformed page titles

### Validation Checks:
- Page existence verification
- Content retrieval confirmation
- Langlinks parsing correctness
- Error message accuracy
- Observer callback execution

## Logging and Monitoring

### Log Levels:
- **INFO**: Page checks started/completed
- **WARNING**: Pages not found, fallback methods used
- **ERROR**: Network issues, API errors, configuration problems

### Monitoring Integration:
- Observer pattern allows integration with monitoring systems
- Metrics collection for dashboard integration
- Performance tracking for optimization
- Error alerting and reporting

This fetch stage provides a robust, extensible foundation for the InfoboxSync pipeline, ensuring reliable data retrieval while maintaining clean architecture through well-applied design patterns.