# SyncResult Data Model

## Class Reference

**Namespace**: `tasks.InfoboxSync.fetch.models`

**Type**: Dataclass (Python 3.7+)

**Purpose**: Structured container for bi-lingual Wikipedia page synchronization results

## Overview

`SyncResult` is a data class that encapsulates the complete result of a Wikipedia synchronization fetch operation. It provides type-safe access to both Arabic and English page data along with synchronization status and error information.

## Definition

```python
from dataclasses import dataclass
from typing import Optional
from .models import PageInfo

@dataclass
class SyncResult:
    """Structured result container for bi-lingual Wikipedia synchronization."""
    arabic: PageInfo                    # Arabic Wikipedia page information
    english: Optional[PageInfo]         # English Wikipedia page information (if found)
    sync_possible: bool                # Whether synchronization can proceed
    error: Optional[str]                # Error message (if synchronization fails)
```

## Constructor

### Automatic Construction
```python
# Dataclass provides automatic constructor
sync_result = SyncResult(
    arabic=ar_page_info,
    english=en_page_info,
    sync_possible=True,
    error=None
)
```

### Factory Methods
```python
# From WikipediaSyncFetcher
sync_result = fetcher.fetch_sync_result("مصر")

# Conversion from dictionary (internal use)
dict_result = fetcher.fetch_arabic_and_english_pages("مصر")
sync_result = SyncResult(
    arabic=dict_result['arabic'],
    english=dict_result['english'],
    sync_possible=dict_result['sync_possible'],
    error=dict_result['error']
)
```

## Attributes

### `arabic: PageInfo`

**Required**: Always contains Arabic Wikipedia page information.

**Structure**:
```python
PageInfo(
    title="Arabic Page Title",      # Arabic page title
    exists=True,                     # Whether page exists on Arabic Wikipedia
    content="Arabic wikitext...",    # Full page content (if exists)
    langlinks={'en': 'English Title'}, # Language links
    error=None                       # Error message (if any)
)
```

### `english: Optional[PageInfo]`

**Optional**: English Wikipedia page information. May be `None` if English equivalent is not found.

**Structure**:
```python
PageInfo(
    title="English Page Title",      # English page title
    exists=True,                     # Whether page exists on English Wikipedia
    content="English wikitext...",   # Full page content (if exists)
    langlinks={'ar': 'Arabic Title'}, # Language links
    error=None                       # Error message (if any)
)
```

### `sync_possible: bool`

**Required**: Boolean flag indicating whether the synchronization process can proceed.

**Values**:
- **`True`**: Both Arabic and English pages exist and are accessible
- **`False`**: Synchronization cannot proceed (page missing, error occurred)

### `error: Optional[str]`

**Optional**: Error message describing why synchronization failed. Only populated when `sync_possible=False`.

**Common Error Messages**:
- `"Arabic page '{title}' does not exist"`
- `"No corresponding English page found for '{title}'"`
- `"English page '{title}' does not exist"`

## Usage Patterns

### Basic Type-Safe Access

```python
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

fetcher = WikipediaSyncFetcher()
result = fetcher.fetch_sync_result("مصر")

# Type-safe property access
arabic_title = result.arabic.title
english_title = result.english.title if result.english else None
can_proceed = result.sync_possible
error_msg = result.error
```

### Pattern Matching (Python 3.10+)

```python
def handle_sync_result(result: SyncResult) -> str:
    """Process sync result with pattern matching."""
    match result:
        case SyncResult(sync_possible=False, error=err):
            return f"Synchronization failed: {err}"
        case SyncResult(arabic=ar, english=en) if ar.exists and en.exists:
            return f"Ready to sync: '{ar.title}' ↔ '{en.title}'"
        case SyncResult(arabic=ar) if ar.exists:
            return f"Arabic page found but no English equivalent for '{ar.title}'"
```

### Error Handling

```python
def process_with_error_handling(result: SyncResult) -> dict:
    """Process sync result with comprehensive error handling."""
    if not result.sync_possible:
        # Categorize error for specific handling
        error_msg = result.error or "Unknown error"

        if "does not exist" in error_msg and "Arabic" in error_msg:
            return {"status": "arabic_missing", "action": "suggest_creation"}
        elif "No corresponding English" in error_msg:
            return {"status": "english_missing", "action": "manual_lookup"}
        else:
            return {"status": "other_error", "action": "investigate"}

    # Safe to access both pages
    return {
        "status": "ready",
        "arabic_content": result.arabic.content,
        "english_content": result.english.content
    }
```

## Common Usage Scenarios

### 1. Successful Synchronization

```python
result = fetcher.fetch_sync_result("مصر")
# SyncResult(
#     arabic=PageInfo(title="مصر", exists=True, content="..."),
#     english=PageInfo(title="Egypt", exists=True, content="..."),
#     sync_possible=True,
#     error=None
# )

print(f"Arabic: {result.arabic.title}")
print(f"English: {result.english.title}")
print("Synchronization ready!")
```

### 2. Arabic Page Missing

```python
result = fetcher.fetch_sync_result("NonExistentPage")
# SyncResult(
#     arabic=PageInfo(title="NonExistentPage", exists=False, error="Page not found"),
#     english=None,
#     sync_possible=False,
#     error="Arabic page 'NonExistentPage' does not exist"
# )

print(f"Cannot proceed: {result.error}")
```

### 3. No English Equivalent

```python
result = fetcher.fetch_sync_result("UniqueArabicConcept")
# SyncResult(
#     arabic=PageInfo(title="UniqueArabicConcept", exists=True, content="..."),
#     english=None,
#     sync_possible=False,
#     error="No corresponding English page found for 'UniqueArabicConcept'"
# )

print("Arabic page exists, but no English equivalent found")
```

## Comparison with Dictionary Format

### Dictionary Format (Legacy)
```python
dict_result = fetcher.fetch_arabic_and_english_pages("مصر")
# {
#     'arabic': PageInfo(...),
#     'english': PageInfo(...),
#     'sync_possible': True,
#     'error': None
# }

# Access with string keys (runtime errors possible)
arabic_page = dict_result['arabic']  # KeyError if missing
english_page = dict_result['english'] # KeyError if missing
```

### SyncResult Format (Recommended)
```python
sync_result = fetcher.fetch_sync_result("مصر")
# SyncResult(arabic=..., english=..., sync_possible=True, error=None)

# Access with attributes (compile-time safety)
arabic_page = sync_result.arabic    # Always present
english_page = sync_result.english  # Typed as Optional[PageInfo]
```

### Benefits of SyncResult
1. **Type Safety**: Compile-time checking of attribute access
2. **IDE Support**: Auto-completion and refactoring
3. **Documentation**: Self-documenting data structure
4. **Pattern Matching**: Support for advanced Python pattern matching

## Integration Examples

### Pipeline Integration

```python
from typing import List
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

class InfoboxSyncPipeline:
    def __init__(self):
        self.fetcher = WikipediaSyncFetcher()

    def batch_process(self, arabic_titles: List[str]) -> List[dict]:
        """Process multiple pages with SyncResult."""
        results = []

        for title in arabic_titles:
            sync_result = self.fetcher.fetch_sync_result(title)

            if sync_result.sync_possible:
                # Proceed with parsing, translation, etc.
                processed = self._process_pages(sync_result)
                results.append({
                    'title': title,
                    'status': 'processed',
                    'data': processed
                })
            else:
                results.append({
                    'title': title,
                    'status': 'skipped',
                    'reason': sync_result.error
                })

        return results
```

### Observer Pattern

```python
class SyncMetricsObserver:
    """Observer that analyzes SyncResult patterns."""

    def __init__(self):
        self.total_requests = 0
        self.successful_syncs = 0
        self.failure_reasons = {}

    def analyze_result(self, result: SyncResult):
        """Analyze sync result and update metrics."""
        self.total_requests += 1

        if result.sync_possible:
            self.successful_syncs += 1
        else:
            error_category = self._categorize_error(result.error)
            self.failure_reasons[error_category] = (
                self.failure_reasons.get(error_category, 0) + 1
            )

    def get_success_rate(self) -> float:
        """Calculate sync success rate."""
        return self.successful_syncs / self.total_requests if self.total_requests > 0 else 0.0

    def _categorize_error(self, error: Optional[str]) -> str:
        """Categorize error messages."""
        if not error:
            return "unknown"
        if "Arabic page" in error and "does not exist" in error:
            return "arabic_missing"
        if "English page" in error and "does not exist" in error:
            return "english_missing"
        if "No corresponding English" in error:
            return "no_english_equivalent"
        return "other"
```

## Serialization

### JSON Serialization

```python
import json
from dataclasses import asdict

# Convert to dictionary for JSON serialization
sync_dict = asdict(result)

# Add computed fields if needed
sync_dict['arabic_title'] = result.arabic.title
sync_dict['english_title'] = result.english.title if result.english else None

# Serialize to JSON
json_string = json.dumps(sync_dict, ensure_ascii=False, indent=2)
```

### Database Storage

```python
def save_sync_result(result: SyncResult, db_connection):
    """Save sync result to database."""

    # Prepare data for database insertion
    record = {
        'arabic_title': result.arabic.title,
        'arabic_exists': result.arabic.exists,
        'arabic_content_length': len(result.arabic.content or ''),
        'english_title': result.english.title if result.english else None,
        'english_exists': result.english.exists if result.english else False,
        'sync_possible': result.sync_possible,
        'error_message': result.error,
        'timestamp': datetime.now()
    }

    db_connection.insert('sync_results', record)
```

## Testing

### Unit Testing

```python
import pytest
from tasks.InfoboxSync.fetch.models import SyncResult, PageInfo

def test_successful_sync_result():
    """Test SyncResult for successful sync."""
    arabic_page = PageInfo(title="مصر", exists=True, content="محتوى عربي")
    english_page = PageInfo(title="Egypt", exists=True, content="English content")

    result = SyncResult(
        arabic=arabic_page,
        english=english_page,
        sync_possible=True,
        error=None
    )

    assert result.arabic.title == "مصر"
    assert result.english.title == "Egypt"
    assert result.sync_possible is True
    assert result.error is None

def test_failed_sync_result():
    """Test SyncResult for failed sync."""
    arabic_page = PageInfo(title="NonExistent", exists=False, error="Page not found")

    result = SyncResult(
        arabic=arabic_page,
        english=None,
        sync_possible=False,
        error="Arabic page 'NonExistent' does not exist"
    )

    assert result.arabic.exists is False
    assert result.english is None
    assert result.sync_possible is False
    assert "does not exist" in result.error
```

### Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(
    arabic_title=st.text(min_size=1, max_size=100),
    english_title=st.text(min_size=1, max_size=100),
    sync_possible=st.booleans(),
    error_msg=st.text() | st.none()
)
def test_sync_result_properties(arabic_title, english_title, sync_possible, error_msg):
    """Property-based test for SyncResult invariants."""

    arabic_page = PageInfo(title=arabic_title, exists=True)
    english_page = PageInfo(title=english_title, exists=True) if sync_possible else None

    if not sync_possible:
        error_msg = error_msg or f"Cannot sync {arabic_title}"

    result = SyncResult(
        arabic=arabic_page,
        english=english_page,
        sync_possible=sync_possible,
        error=error_msg if not sync_possible else None
    )

    # Verify invariants
    assert result.arabic is not None
    assert result.sync_possible is not None

    if result.sync_possible:
        assert result.english is not None
        assert result.error is None
    else:
        assert result.error is not None
```

## Performance Considerations

### Memory Usage

```python
# SyncResult contains full page content, which can be large
# For memory-constrained environments, consider lazy loading

class MemoryEfficientPipeline:
    def __init__(self):
        self.fetcher = WikipediaSyncFetcher()

    def process_lightweight(self, title: str) -> dict:
        """Process pages without storing full content."""
        result = self.fetcher.fetch_sync_result(title)

        # Return only metadata, not full content
        return {
            'arabic_title': result.arabic.title,
            'arabic_exists': result.arabic.exists,
            'english_title': result.english.title if result.english else None,
            'sync_possible': result.sync_possible,
            'error': result.error,
            'content_length_ar': len(result.arabic.content or ''),
            'content_length_en': len(result.english.content or '') if result.english else 0
        }
```

### Iteration Optimization

```python
# When processing many pages, reuse SyncResult analysis logic

def analyze_sync_results(results: List[SyncResult]) -> dict:
    """Analyze multiple SyncResult instances efficiently."""
    stats = {
        'total': len(results),
        'successful': 0,
        'arabic_missing': 0,
        'english_missing': 0,
        'other_errors': 0
    }

    for result in results:  # Direct iteration over SyncResult objects
        if result.sync_possible:
            stats['successful'] += 1
        elif result.error:
            if "Arabic page" in result.error and "does not exist" in result.error:
                stats['arabic_missing'] += 1
            elif "English" in result.error:
                stats['english_missing'] += 1
            else:
                stats['other_errors'] += 1

    return stats
```

## Related Classes

- **PageInfo**: Basic page information container
- **WikipediaSyncFetcher**: Producer of SyncResult instances
- **FetchObserver**: Observer pattern for monitoring sync operations

## Migration Guide

### From Dictionary Format

```python
# Old code using dictionary format
def process_dict_result(result_dict: dict):
    arabic_page = result_dict['arabic']
    english_page = result_dict.get('english')  # Could raise KeyError
    sync_possible = result_dict['sync_possible']  # Could raise KeyError
    error = result_dict.get('error')  # Safe but verbose

# New code using SyncResult
def process_sync_result(sync_result: SyncResult):
    arabic_page = sync_result.arabic       # Always present
    english_page = sync_result.english     # Optional, typed
    sync_possible = sync_result.sync_possible  # Always present
    error = sync_result.error              # Optional, typed
```

---

**File Location**: `tasks/InfoboxSync/fetch/models.py`
**Since**: v1.0
**Python Version**: 3.7+ (dataclasses)