# WikipediaSyncFetcher Class

## Class Reference

**Namespace**: `tasks.InfoboxSync.fetch.sync_fetcher`

**Inherits**: `object` (No inheritance - orchestration class)

**Design Pattern**: Strategy Pattern (Coordinator/Facade)

## Overview

The main orchestration class for the fetch stage that coordinates the synchronization process between Arabic and English Wikipedia pages. Uses the Strategy Pattern by encapsulating different fetch strategies and providing a unified interface for bi-lingual Wikipedia data retrieval.

## Constructor

```python
def __init__(self, observer: Optional[FetchObserver] = None):
    """
    Initialize the synchronization fetcher with dual-language support.

    Args:
        observer: Optional observer for monitoring sync operations
    """
    # Creates Arabic and English fetchers automatically
    self.ar_fetcher = PywikibotFetcher('ar', observer)
    self.en_fetcher = PywikibotFetcher('en', observer)
```

### Attributes

- **`observer`**: `FetchObserver` - Observer for monitoring sync operations
- **`ar_fetcher`**: `PywikibotFetcher` - Arabic Wikipedia fetcher instance
- **`en_fetcher`**: `PywikibotFetcher` - English Wikipedia fetcher instance

## Core Methods

### `fetch_arabic_and_english_pages(ar_page_title: str) -> Dict[str, Any]`

**Main Entry Point**: Orchestrates the complete bi-lingual fetch process.

```python
def fetch_arabic_and_english_pages(self, ar_page_title: str) -> Dict[str, Any]:
    """
    Fetch Arabic page and its corresponding English equivalent.

    Comprehensive bi-lingual retrieval with fallback strategies:
    1. Verify Arabic page exists
    2. Find English equivalent via multiple methods
    3. Fetch English page content and metadata
    4. Return structured result with sync status

    Args:
        ar_page_title: Title of the Arabic Wikipedia page

    Returns:
        Dict containing both pages' information and sync status

    Return Format:
    {
        'arabic': PageInfo       # Arabic page data
        'english': PageInfo      # English page data (or None)
        'sync_possible': bool    # Whether sync can proceed
        'error': str or None     # Error message if any
    }
    """
```

**Implementation Flow:**

```python
# Algorithm Steps:
1. Fetch Arabic page → Check existence
2. Extract English title → Via langlinks or fallback
3. Fetch English page → With full content and metadata
4. Return structured result → With sync feasibility status
```

### `fetch_sync_result(ar_page_title: str) -> SyncResult`

**Structured Return Method**: Returns typed `SyncResult` object instead of dictionary.

```python
def fetch_sync_result(self, ar_page_title: str) -> SyncResult:
    """
    Fetch synchronization result with type-safe dataclass return.

    Args:
        ar_page_title: Title of the Arabic Wikipedia page

    Returns:
        SyncResult object with structured page data
    """
    result = self.fetch_arabic_and_english_pages(ar_page_title)
    return SyncResult(
        arabic=result['arabic'],
        english=result['english'],
        sync_possible=result['sync_possible'],
        error=result['error']
    )
```

### `_find_english_page_title(ar_page_info: PageInfo) -> Optional[str]`

**Private Method**: Intelligent English page discovery with multiple fallback strategies.

```python
def _find_english_page_title(self, ar_page_info: PageInfo) -> Optional[str]:
    """
    Discover corresponding English page title using multiple strategies.

    Discovery Methods (in order of preference):
    1. Direct Language Links: ar_page_info.langlinks['en']
    2. Title Match Fallback: Same title in English Wikipedia
    3. Advanced Matching: Future enhancement for complex title relationships

    Args:
        ar_page_info: Arabic page information with langlinks

    Returns:
        English page title or None if not found
    """
```

**Discovery Strategies:**

1. **Primary Method**: Direct language links from Arabic page
```python
if ar_page_info.langlinks and 'en' in ar_page_info.langlinks:
    return ar_page_info.langlinks['en']
```

2. **Fallback Method**: Direct title matching
```python
return ar_page_info.title  # Same name, different language
```

## Usage Patterns

### Basic Synchronization

```python
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

# Create sync fetcher
sync_fetcher = WikipediaSyncFetcher()

# Fetch bi-lingual page data
result = sync_fetcher.fetch_arabic_and_english_pages("مصر")  # Egypt

if result['sync_possible']:
    arabic_page = result['arabic']
    english_page = result['english']

    print(f"Arabic: {arabic_page.title}")
    print(f"English: {english_page.title}")
    print(f"Arabic Content: {len(arabic_page.content)} chars")
    print(f"English Content: {len(english_page.content)} chars")
else:
    print(f"Sync failed: {result['error']}")
```

### Advanced Monitoring

```python
from tasks.InfoboxSync.fetch.observers import MetricsFetchObserver

# Create fetcher with performance monitoring
metrics_observer = MetricsFetchObserver()
sync_fetcher = WikipediaSyncFetcher(observer=metrics_observer)

# Process multiple pages
pages = ["مصر", "باريس", "برلين"]
for ar_page in pages:
    result = sync_fetcher.fetch_arabic_and_english_pages(ar_page)

# Analyze performance
stats = metrics_observer.get_metrics()
print(f"Total pages processed: {stats['pages_checked']}")
print(f"Sync success rate: {stats['pages_found']/stats['pages_checked']:.1%}")
```

### Type-Safe Operations

```python
# Use structured return type for better type safety
sync_result = sync_fetcher.fetch_sync_result("خير الدين مضوي")

if sync_result.sync_possible:
    ar_page = sync_result.arabic
    en_page = sync_result.english

    # Type-safe processing
    print(f"Sync ready - AR: {ar_page.title}, EN: {en_page.title}")
else:
    print(f"Sync blocked: {sync_result.error}")
```

## Failure Scenarios and Recovery

### Common Failure Patterns

1. **Arabic Page Missing**: Most common failure
```python
result = sync_fetcher.fetch_arabic_and_english_pages("محمد بن سلمان")
# Result: {'sync_possible': False, 'error': "Arabic page 'محمد بن سلمان' does not exist"}
```

2. **No English Equivalent**: Second most common
```python
# Arabic page exists but no English langlink
result['sync_possible'] = False
result['error'] = "No corresponding English page found for 'Unique Arabic Term'"
```

3. **English Page Missing**: Rare but possible
```python
# Arabic page has langlink but English page deleted/renamed
en_page = {'exists': False, 'error': "English page 'Old English Title' does not exist"}
```

### Automatic Error Recovery

```python
def robust_sync(ar_page_title: str) -> Optional[Dict]:
    """
    Robust synchronization with comprehensive error handling.
    """
    try:
        result = sync_fetcher.fetch_arabic_and_english_pages(ar_page_title)

        # Check sync feasibility
        if not result['sync_possible']:
            error_type = categorize_error(result['error'])

            if error_type == 'arabic_missing':
                # Suggest creating Arabic page first
                return handle_arabic_missing(ar_page_title)

            elif error_type == 'english_missing':
                # Try alternative English title
                return attempt_alternative_search(ar_page_title)

            else:
                # Log for manual review
                log_sync_failure(result)
                return None

        return result

    except Exception as e:
        logger.error(f"Unexpected sync error for {ar_page_title}: {e}")
        return None
```

## Performance Optimization

### Efficient Fetch Strategy

```python
# Single API call per page (Arabic + English = 2 calls total)
ar_page = ar_fetcher.fetch_page_info(ar_page_title)     # 1 API call
en_page = en_fetcher.fetch_page_info(en_page_title)     # 1 API call

# Optimized for minimal network overhead
total_api_calls = 2  # vs 4+ for naive implementations
```

### Lazy Loading Pattern

```python
# Pywikibot sites initialized only when needed
sync_fetcher = WikipediaSyncFetcher()  # No immediate API connections

# First fetch triggers initialization
result = sync_fetcher.fetch_arabic_and_english_pages("مصر")  # Sites created here
```

### Connection Reuse

```python
# Same pywikibot site objects reused across multiple fetches
for page in ["مصر", "باريس", "برلين"]:
    result = sync_fetcher.fetch_arabic_and_english_pages(page)
    # Reuses same Arabic and English site connections
```

## Integration Patterns

### Pipeline Integration

```python
# Used by test.py as primary fetch interface
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

class InfoboxSyncPipeline:
    def __init__(self):
        self.fetcher = WikipediaSyncFetcher()

    def run_pipeline(self, ar_page_title: str):
        # Stage 1: Fetch
        wiki_data = self.fetcher.fetch_arabic_and_english_pages(ar_page_title)

        if not wiki_data['sync_possible']:
            return {'error': wiki_data['error']}

        # Continue to parse, translate, etc.
        return self._process_sync_data(wiki_data)
```

### Observer Integration

```python
class SyncProgressObserver(FetchObserver):
    """Custom observer for sync-specific monitoring."""

    def __init__(self):
        self.sync_attempts = []
        self.langlink_success_rate = 0.0

    def on_page_check_complete(self, page_info: PageInfo):
        self.sync_attempts.append({
            'title': page_info.title,
            'exists': page_info.exists,
            'has_langlinks': bool(page_info.langlinks)
        })

    def get_sync_stats(self) -> Dict:
        total = len(self.sync_attempts)
        langlinked = sum(1 for a in self.sync_attempts if a['has_langlinks'])
        return {
            'total_attempts': total,
            'langlink_success_rate': langlinked / total if total > 0 else 0.0
        }
```

## Architecture Benefits

### Strategy Pattern Advantages

1. **Loose Coupling**: Fetch strategies can be replaced without affecting sync logic
2. **Easy Testing**: Mock fetchers can replace actual implementations
3. **Extensibility**: New languages supported by adding new fetcher strategies

### Facade Pattern Benefits

1. **Simplified Interface**: Single method call replaces multiple coordination tasks
2. **Unified Error Handling**: Centralized error management across dual-language operations
3. **Consistent Return Types**: Standardized `Dict` or `SyncResult` responses

## Testing Considerations

### Unit Testing Strategy

```python
import unittest.mock as mock

def test_successful_sync():
    """Test successful Arabic-English synchronization."""
    sync_fetcher = WikipediaSyncFetcher()

    # Mock both fetchers
    with mock.patch.object(sync_fetcher.ar_fetcher, 'fetch_page_info') as mock_ar, \
         mock.patch.object(sync_fetcher.en_fetcher, 'fetch_page_info') as mock_en:

        # Setup mock Arabic page with English langlink
        ar_page = PageInfo(
            title="مصر",
            exists=True,
            content="محتوى عربي",
            langlinks={'en': 'Egypt'}
        )
        en_page = PageInfo(
            title="Egypt",
            exists=True,
            content="English content"
        )

        mock_ar.return_value = ar_page
        mock_en.return_value = en_page

        # Test sync operation
        result = sync_fetcher.fetch_arabic_and_english_pages("مصر")

        assert result['sync_possible'] is True
        assert result['arabic'].title == "مصر"
        assert result['english'].title == "Egypt"

def test_arabic_page_missing():
    """Test handling of missing Arabic pages."""
    # Similar mocking pattern with exists=False
```

### Integration Testing

```python
def test_real_wikipedia_sync():
    """Integration test with real Wikipedia (limited usage)."""
    sync_fetcher = WikipediaSyncFetcher()

    # Test with known pages
    result = sync_fetcher.fetch_arabic_and_english_pages("مصر")

    # Verify result structure (not actual content for test stability)
    assert 'arabic' in result
    assert 'english' in result
    assert 'sync_possible' in result
    assert isinstance(result['sync_possible'], bool)
```

## Future Enhancements

### Planned Improvements

1. **Advanced Title Matching**: Fuzzy matching for pages with slightly different names
2. **Batch Processing**: Multiple pages processed efficiently
3. **Caching Layer**: Reduce API calls for frequently accessed pages
4. **Rate Limiting**: Respect Wikipedia API limits across multiple requests

### Extension Points

```python
class EnhancedWikipediaSyncFetcher(WikipediaSyncFetcher):
    """Future enhancement with advanced language matching."""

    def __init__(self, use_cache: bool = False):
        super().__init__()
        self.cache = {} if use_cache else None

    def _find_english_page_title(self, ar_page_info: PageInfo) -> Optional[str]:
        # Add fuzzy matching logic
        if ar_page_info.langlinks and 'en' in ar_page_info.langlinks:
            return ar_page_info.langlinks['en']

        # Try fuzzy title matching (future enhancement)
        return self._fuzzy_title_match(ar_page_info.title)
```

---

**File Location**: `tasks/InfoboxSync/fetch/sync_fetcher.py`
**Status**: Production-ready orchestration class
**Dependencies**: `PywikibotFetcher`, `PageInfo`, `SyncResult`, `FetchObserver`
**Since**: v1.0