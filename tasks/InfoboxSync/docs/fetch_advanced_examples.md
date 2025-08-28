# Fetch Module: Advanced Usage Examples

## Overview

This document provides advanced usage examples for the Fetch module, showcasing complex patterns, performance optimizations, and integration scenarios for the InfoboxSync pipeline.

## Table of Contents

1. [Batch Processing](#batch-processing)
2. [Custom Observers](#custom-observers)
3. [Error Recovery Patterns](#error-recovery-patterns)
4. [Performance Optimization](#performance-optimization)
5. [Integration Patterns](#integration-patterns)
6. [Monitoring and Analytics](#monitoring-and-analytics)
7. [Testing Strategies](#testing-strategies)
8. [Migration Patterns](#migration-patterns)

## Batch Processing

### Large-Scale Page Processing

```python
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from tasks.InfoboxSync.fetch import fetch_wikipedia_data
import logging

logger = logging.getLogger(__name__)

class BatchFetchProcessor:
    """Process large batches of Wikipedia pages efficiently."""

    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.rate_limiter = RateLimiter(requests_per_minute=30)

    def process_page_batch(self, page_titles: List[str],
                          handle_errors: bool = True) -> Dict[str, Any]:
        """
        Process a batch of page titles with error handling and rate limiting.

        Args:
            page_titles: List of Arabic page titles
            handle_errors: Whether to handle individual page errors gracefully

        Returns:
            Dictionary mapping page titles to results
        """
        results = {}

        def fetch_with_error_handling(title: str) -> tuple:
            """Fetch single page with error handling."""
            try:
                self.rate_limiter.wait_if_needed()
                result = fetch_wikipedia_data(title)
                return title, result, None
            except Exception as e:
                error = f"Failed to fetch '{title}': {str(e)}"
                logger.error(error)
                return title, None, error

        # Process in parallel with error handling
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_title = {
                executor.submit(fetch_with_error_handling, title): title
                for title in page_titles
            }

            for future in as_completed(future_to_title):
                title, result, error = future.result()

                if error and not handle_errors:
                    raise ValueError(f"Batch processing failed: {error}")

                results[title] = {
                    'data': result,
                    'error': error,
                    'success': result is not None
                }

        # Summarize batch results
        successful = sum(1 for r in results.values() if r['success'])
        failed = len(results) - successful

        logger.info(f"Batch completed: {successful} successful, {failed} failed")

        return {
            'results': results,
            'summary': {
                'total': len(page_titles),
                'successful': successful,
                'failed': failed,
                'success_rate': successful / len(page_titles) if page_titles else 0
            }
        }

class RateLimiter:
    """Simple rate limiter for Wikipedia API calls."""

    def __init__(self, requests_per_minute: int = 30):
        from datetime import datetime, timedelta
        self.requests_per_minute = requests_per_minute
        self.requests = []
        self.min_interval = 60.0 / requests_per_minute

    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        import time
        from datetime import datetime, timedelta

        now = datetime.now()
        cutoff = now - timedelta(minutes=1)

        # Remove old requests
        self.requests = [req for req in self.requests if req > cutoff]

        if len(self.requests) >= self.requests_per_minute:
            # Wait until oldest request expires
            wait_time = (self.requests[0] - cutoff).total_seconds()
            if wait_time > 0:
                time.sleep(wait_time)
            self.requests = self.requests[1:]

        self.requests.append(now)
```

### Usage Example

```python
processor = BatchFetchProcessor(max_workers=3)

# Process football players
players = [
    "ليونيل ميسي", "كريستيانو رونالدو", "محمد صلاح",
    "خير الدين مضوي", "الباسيليو راموس", "أندريس إنييستا"
]

batch_results = processor.process_page_batch(players)

# Analyze results
for player, result in batch_results['results'].items():
    if result['success']:
        data = result['data']
        if data['sync_possible']:
            print(f"✓ {player}: Ready for sync")
        else:
            print(f"⚠ {player}: {data['error']}")
    else:
        print(f"✗ {player}: {result['error']}")
```

## Custom Observers

### Performance Monitoring Observer

```python
from tasks.InfoboxSync.fetch.observers import FetchObserver
from tasks.InfoboxSync.fetch.models import PageInfo
import time
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    request_count: int = 0
    total_time: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    response_times: List[float] = field(default_factory=list)
    error_types: Dict[str, int] = field(default_factory=dict)
    arabic_pages_fetched: int = 0
    english_pages_fetched: int = 0

class PerformanceObserver(FetchObserver):
    """Observer that tracks detailed performance metrics."""

    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.start_times = {}  # Request start times
        self.current_request = None

    def on_page_check_start(self, page_title: str, site: str):
        """Track when page check starts."""
        request_key = f"{site}:{page_title}"

        if request_key not in self.start_times:
            self.start_times[request_key] = time.time()
            self.current_request = request_key
            self.metrics.request_count += 1

        logger.info(f"Starting fetch for {site}:{page_title}")

    def on_page_check_complete(self, page_info: PageInfo):
        """Track when page check completes."""
        if self.current_request and self.current_request in self.start_times:
            start_time = self.start_times.pop(self.current_request)
            response_time = time.time() - start_time

            self.metrics.response_times.append(response_time)
            self.metrics.total_time += response_time

            if page_info.exists:
                self.metrics.success_count += 1

                # Track site-specific metrics
                if hasattr(page_info, '_site_name'):
                    if page_info._site_name == 'ar':
                        self.metrics.arabic_pages_fetched += 1
                    elif page_info._site_name == 'en':
                        self.metrics.english_pages_fetched += 1
            else:
                self.metrics.failure_count += 1
                self._categorize_error(page_info.error)

        logger.info(f"Completed fetch for {page_info.title} in {response_time:.2f}s")

    def on_error(self, error: str):
        """Track error occurrences."""
        self.metrics.failure_count += 1
        self._categorize_error(error)

        logger.error(f"Fetch error: {error}")

    def _categorize_error(self, error: str):
        """Categorize errors for analysis."""
        if not error:
            error_category = "unknown"
        elif "timeout" in error.lower():
            error_category = "timeout"
        elif "not found" in error.lower():
            error_category = "not_found"
        elif "forbidden" in error.lower():
            error_category = "forbidden"
        elif "network" in error.lower():
            error_category = "network"
        else:
            error_category = "other"

        self.metrics.error_types[error_category] = (
            self.metrics.error_types.get(error_category, 0) + 1
        )

    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        total_requests = self.metrics.success_count + self.metrics.failure_count

        return {
            'total_requests': total_requests,
            'success_rate': self.metrics.success_count / total_requests if total_requests > 0 else 0,
            'average_response_time': (
                sum(self.metrics.response_times) / len(self.metrics.response_times)
                if self.metrics.response_times else 0
            ),
            'min_response_time': min(self.metrics.response_times) if self.metrics.response_times else 0,
            'max_response_time': max(self.metrics.response_times) if self.metrics.response_times else 0,
            'total_time': self.metrics.total_time,
            'error_distribution': self.metrics.error_types,
            'pages_per_site': {
                'arabic': self.metrics.arabic_pages_fetched,
                'english': self.metrics.english_pages_fetched
            }
        }
```

### Usage with Performance Observer

```python
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

# Create fetcher with performance monitoring
performance_observer = PerformanceObserver()
fetcher = WikipediaSyncFetcher(observer=performance_observer)

# Perform operations
pages = ["مصر", "باريس", "برلين", "ألمانيا"]
for page in pages:
    result = fetcher.fetch_arabic_and_english_pages(page)

# Get performance report
summary = performance_observer.get_summary()
print(".2%")
print(f"Average response time: {summary['average_response_time']:.2f}s")
print(f"Pages fetched: AR={summary['pages_per_site']['arabic']}, EN={summary['pages_per_site']['english']}")

if summary['error_distribution']:
    print("Error distribution:")
    for error_type, count in summary['error_distribution'].items():
        print(f"  {error_type}: {count}")
```

## Error Recovery Patterns

### Intelligent Retry Mechanism

```python
import random
import time
from typing import Optional, Callable, Any
from functools import wraps

class RetryMechanism:
    """Intelligent retry mechanism for fetch operations."""

    def __init__(self, max_attempts: int = 3, backoff_factor: float = 1.5):
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor

    def execute_with_retry(self, operation: Callable, *args, **kwargs) -> Any:
        """Execute operation with exponential backoff retry."""
        last_exception = None

        for attempt in range(self.max_attempts):
            try:
                return operation(*args, **kwargs)

            except Exception as e:
                last_exception = e
                error_msg = str(e).lower()

                # Don't retry certain errors
                if any(error_type in error_msg for error_type in [
                    'not found', 'forbidden', 'unauthorized', 'page does not exist'
                ]):
                    logger.info(f"Not retrying non-retryable error: {e}")
                    break

                if attempt < self.max_attempts - 1:
                    wait_time = self.backoff_factor ** attempt * random.uniform(0.5, 1.5)
                    logger.info(f"Attempt {attempt + 1} failed, retrying in {wait_time:.1f}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {self.max_attempts} attempts failed: {e}")

        raise last_exception

def retry_on_failure(max_attempts: int = 3, backoff_factor: float = 1.5):
    """Decorator for adding retry functionality."""
    retry_mechanism = RetryMechanism(max_attempts, backoff_factor)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return retry_mechanism.execute_with_retry(func, *args, **kwargs)
        return wrapper
    return decorator

class RobustFetchService:
    """Fetch service with built-in retry and error recovery."""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.retry_mechanism = RetryMechanism(max_retries)
        self.fetcher = WikipediaSyncFetcher()

    @retry_on_failure(max_attempts=3)
    def fetch_with_recovery(self, page_title: str) -> Dict[str, Any]:
        """Fetch page with automatic recovery attempts."""
        try:
            result = self.fetcher.fetch_arabic_and_english_pages(page_title)

            # Additional recovery logic
            if not result['sync_possible'] and result['arabic']['exists']:
                # Try alternative English title matching
                result = self._attempt_alternative_matching(result, page_title)

            return result

        except Exception as e:
            # Log and attempt recovery at service level
            logger.error(f"Failed to fetch '{page_title}' after retries: {e}")
            return {
                'arabic': PageInfo(title=page_title, exists=False, error=str(e)),
                'english': None,
                'sync_possible': False,
                'error': f"Service unavailable: {str(e)}"
            }

    def _attempt_alternative_matching(self, result: Dict[str, Any],
                                    original_title: str) -> Dict[str, Any]:
        """Attempt alternative English page matching strategies."""
        arabic_page = result['arabic']

        if not arabic_page.get('langlinks'):
            return result

        # Try different language codes if 'en' not found
        alternative_codes = ['en', 'en-us', 'en-gb', 'en-ca']

        for code in alternative_codes:
            if code in arabic_page['langlinks']:
                english_title = arabic_page['langlinks'][code]

                # Try fetching with this title
                try:
                    english_result = self.retry_mechanism.execute_with_retry(
                        self.fetcher.ar_fetcher.fetch_page_info, english_title
                    )

                    if english_result.exists:
                        return {
                            'arabic': arabic_page,
                            'english': english_result,
                            'sync_possible': True,
                            'error': None
                        }

                except Exception as e:
                    logger.debug(f"Alternative matching failed for {code}:{english_title}: {e}")
                    continue

        return result  # Return original result if all alternatives fail
```

### Usage Example

```python
service = RobustFetchService(max_retries=3)

# Process with automatic retries and recovery
pages = ["مصر", "صفحة_غير_موجودة", "مشكلة_شبكة", "باريس"]
results = {}

for page in pages:
    try:
        result = service.fetch_with_recovery(page)
        results[page] = result

        if result['sync_possible']:
            print(f"✓ {page}: Successfully fetched")
        else:
            print(f"⚠ {page}: {result['error']}")

    except Exception as e:
        print(f"✗ {page}: Service error - {e}")
        results[page] = None
```

## Performance Optimization

### Connection Pooling

```python
from concurrent.futures import ThreadPoolExecutor
import threading
from typing import Dict, Any

class FetchServicePool:
    """Thread-safe fetch service pool with connection reuse."""

    def __init__(self, pool_size: int = 5):
        self.pool_size = pool_size
        self.services = []
        self.lock = threading.Lock()
        self._initialize_pool()

    def _initialize_pool(self):
        """Initialize pool of fetch services."""
        for _ in range(self.pool_size):
            service = WikipediaSyncFetcher()
            self.services.append(service)

    def get_service(self) -> WikipediaSyncFetcher:
        """Get available service from pool."""
        with self.lock:
            if self.services:
                return self.services.pop(0)
            else:
                # Create new service if pool exhausted
                return WikipediaSyncFetcher()

    def return_service(self, service: WikipediaSyncFetcher):
        """Return service to pool for reuse."""
        with self.lock:
            if len(self.services) < self.pool_size:
                self.services.append(service)

    def process_batch(self, tasks: List[str]) -> Dict[str, Any]:
        """Process batch with connection pooling."""
        results = {}

        def process_task(task: str, service: WikipediaSyncFetcher) -> tuple:
            try:
                result = service.fetch_arabic_and_english_pages(task)
                return task, result
            finally:
                self.return_service(service)

        with ThreadPoolExecutor(max_workers=self.pool_size) as executor:
            future_to_task = {
                executor.submit(process_task, task, self.get_service()): task
                for task in tasks
            }

            for future in as_completed(future_to_task):
                task, result = future.result()
                results[task] = result

        return results
```

### Memory-Efficient Processing

```python
class MemoryOptimizedFetchPipeline:
    """Pipeline that minimizes memory usage during batch processing."""

    def __init__(self):
        self.fetcher = WikipediaSyncFetcher()

    def process_with_memory_limits(self, page_titles: List[str],
                                  batch_size: int = 10) -> Dict[str, Any]:
        """
        Process pages with memory limits and intermediate cleanup.

        Args:
            page_titles: List of page titles to process
            batch_size: Number of pages to process before cleanup

        Returns:
            Dictionary of results
        """
        results = {}

        for i in range(0, len(page_titles), batch_size):
            batch = page_titles[i:i + batch_size]

            # Process batch
            batch_results = {}
            for title in batch:
                result = self.fetcher.fetch_arabic_and_english_pages(title)
                batch_results[title] = result

            # Store batch results
            results.update(batch_results)

            # Explicit cleanup to free memory
            self._cleanup_batch_data(batch_results)

            logger.info(f"Processed batch {i//batch_size + 1}, "
                       f"total processed: {min(i + batch_size, len(page_titles))}")

        return results

    def _cleanup_batch_data(self, batch_results: Dict[str, Any]):
        """Clean up batch data to free memory."""
        for title, result in batch_results.items():
            if 'arabic' in result and result['arabic']:
                # Keep only essential data, discard large content
                arabic_page = result['arabic']
                essential = {
                    'title': arabic_page.get('title'),
                    'exists': arabic_page.get('exists'),
                    'has_content': bool(arabic_page.get('content')),
                    'content_length': len(arabic_page.get('content', '')),
                    'langlinks_count': len(arabic_page.get('langlinks', {}))
                }
                result['arabic_summary'] = essential
                result['arabic'].pop('content', None)  # Remove large content

            if 'english' in result and result['english']:
                english_page = result['english']
                essential = {
                    'title': english_page.get('title'),
                    'exists': english_page.get('exists'),
                    'has_content': bool(english_page.get('content')),
                    'content_length': len(english_page.get('content', ''))
                }
                result['english_summary'] = essential
                result['english'].pop('content', None)
```

## Integration Patterns

### Pipeline Integration

```python
from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

@runtime_checkable
class PipelineStage(Protocol):
    """Protocol for pipeline stages."""

    def process(self, input_data: Any) -> Any:
        """Process input data."""
        ...

    def can_process(self, input_data: Any) -> bool:
        """Check if stage can process input."""
        ...

class FetchStage:
    """Fetch stage implementation for pipeline."""

    def __init__(self):
        self.fetcher = WikipediaSyncFetcher()

    def process(self, page_title: str) -> Dict[str, Any]:
        """Fetch stage processing."""
        result = self.fetcher.fetch_arabic_and_english_pages(page_title)

        if result['sync_possible']:
            return {
                'stage': 'fetch',
                'status': 'success',
                'data': result,
                'next_stages': ['parse', 'translate', 'construct']
            }
        else:
            return {
                'stage': 'fetch',
                'status': 'failure',
                'data': result,
                'error': result['error'],
                'next_stages': []
            }

    def can_process(self, input_data: Any) -> bool:
        """Check if fetch stage can process input."""
        return isinstance(input_data, str) and input_data.strip()

class PipelineOrchestrator:
    """Orchestrate multi-stage processing with fetch integration."""

    def __init__(self):
        self.stages = {
            'fetch': FetchStage(),
            # Add other stages here
        }
        self.retry_mechanism = RetryMechanism(max_attempts=3)

    def process_full_pipeline(self, inputs: List[str]) -> Dict[str, Any]:
        """Process inputs through full pipeline."""
        results = {}

        for input_data in inputs:
            try:
                result = self._process_single_input(input_data)
                results[str(input_data)] = result

            except Exception as e:
                logger.error(f"Pipeline failed for {input_data}: {e}")
                results[str(input_data)] = {
                    'status': 'error',
                    'error': str(e)
                }

        return results

    def _process_single_input(self, input_data: str) -> Dict[str, Any]:
        """Process single input through pipeline stages."""
        current_data = input_data

        for stage_name, stage in self.stages.items():
            if not stage.can_process(current_data):
                continue

            logger.info(f"Processing {input_data} through {stage_name} stage")

            # Execute with retry
            processed_data = self.retry_mechanism.execute_with_retry(
                stage.process, current_data
            )

            # Handle stage results
            if processed_data.get('status') == 'failure':
                return processed_data

            # Prepare for next stage
            if 'next_stages' in processed_data and processed_data['next_stages']:
                current_data = processed_data['data']
            else:
                break

        return processed_data
```

## Monitoring and Analytics

### Comprehensive Monitoring System

```python
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta

class AnalyticsSystem:
    """Comprehensive analytics for fetch operations."""

    def __init__(self, log_directory: str = 'analytics'):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        self.current_session = datetime.now().isoformat()
        self.session_data = []

    def log_operation(self, operation: str, page_title: str,
                     result: Any, duration: float, metadata: Dict[str, Any] = None):
        """Log individual operation."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'page_title': page_title,
            'duration': duration,
            'success': self._is_success(result),
            'result_summary': self._summarize_result(result),
            'metadata': metadata or {}
        }

        self.session_data.append(log_entry)

        # Immediate file write for durability
        self._write_log_entry(log_entry)

    def _is_success(self, result: Any) -> bool:
        """Determine if operation was successful."""
        if isinstance(result, dict):
            return result.get('sync_possible', False)
        if hasattr(result, 'sync_possible'):
            return result.sync_possible
        return False

    def _summarize_result(self, result: Any) -> Dict[str, Any]:
        """Create summary of operation result."""
        if isinstance(result, dict):
            return {
                'sync_possible': result.get('sync_possible'),
                'arabic_exists': result.get('arabic', {}).get('exists'),
                'english_exists': result.get('english', {}).get('exists') if result.get('english') else False,
                'error': result.get('error')
            }
        elif hasattr(result, 'sync_possible'):
            return {
                'sync_possible': result.sync_possible,
                'arabic_exists': result.arabic.exists,
                'english_exists': result.english.exists if result.english else False,
                'error': result.error
            }
        else:
            return {'type': type(result).__name__}

    def _write_log_entry(self, entry: Dict[str, Any]):
        """Write log entry to file."""
        log_file = self.log_directory / f"fetch_log_{self.current_session.split('T')[0]}.jsonl"

        with open(log_file, 'a', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

    def generate_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate analytics report for specified period."""
        cutoff_date = datetime.now() - timedelta(days=days)

        # Load and filter recent data
        all_entries = []
        for log_file in self.log_directory.glob('*.jsonl'):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            entry = json.loads(line)
                            entry_time = datetime.fromisoformat(entry['timestamp'])
                            if entry_time >= cutoff_date:
                                all_entries.append(entry)
            except Exception as e:
                logger.warning(f"Error reading log file {log_file}: {e}")

        return self._analyze_entries(all_entries)

    def _analyze_entries(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze log entries and generate insights."""
        if not entries:
            return {'message': 'No data available'}

        total_operations = len(entries)
        successful_operations = sum(1 for e in entries if e['success'])
        failed_operations = total_operations - successful_operations

        # Performance metrics
        durations = [e['duration'] for e in entries]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # Error analysis
        error_counts = {}
        for entry in entries:
            if not entry['success'] and entry['result_summary'].get('error'):
                error = entry['result_summary']['error']
                error_counts[error] = error_counts.get(error, 0) + 1

        # Hourly distribution
        hourly_stats = {}
        for entry in entries:
            hour = datetime.fromisoformat(entry['timestamp']).hour
            if hour not in hourly_stats:
                hourly_stats[hour] = {'total': 0, 'successful': 0, 'total_duration': 0}
            hourly_stats[hour]['total'] += 1
            hourly_stats[hour]['total_duration'] += entry['duration']
            if entry['success']:
                hourly_stats[hour]['successful'] += 1

        return {
            'period_days': 7,
            'summary': {
                'total_operations': total_operations,
                'successful_operations': successful_operations,
                'failed_operations': failed_operations,
                'success_rate': successful_operations / total_operations if total_operations > 0 else 0,
                'average_duration': avg_duration
            },
            'performance': {
                'min_duration': min(durations) if durations else 0,
                'max_duration': max(durations) if durations else 0,
                'median_duration': sorted(durations)[len(durations)//2] if durations else 0
            },
            'errors': error_counts,
            'hourly_distribution': hourly_stats,
            'top_error_types': sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }

    def get_health_check(self) -> Dict[str, Any]:
        """Quick health check of the fetch system."""
        recent_entries = self.session_data[-50:]  # Last 50 operations

        if not recent_entries:
            return {'status': 'unknown', 'message': 'No recent data'}

        recent_success_rate = sum(1 for e in recent_entries if e['success']) / len(recent_entries)
        recent_avg_duration = sum(e['duration'] for e in recent_entries) / len(recent_entries)

        status = 'healthy' if recent_success_rate > 0.8 and recent_avg_duration < 30 else 'degraded'
        if recent_success_rate < 0.5:
            status = 'unhealthy'

        return {
            'status': status,
            'success_rate': recent_success_rate,
            'average_duration': recent_avg_duration,
            'recent_operations': len(recent_entries),
            'timestamp': datetime.now().isoformat()
        }
```

## Testing Strategies

### Comprehensive Test Suite

```python
import pytest
from unittest.mock import Mock, patch
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher
from tasks.InfoboxSync.fetch.models import PageInfo, SyncResult

class TestFetchAdvancedScenarios:
    """Test advanced fetch scenarios."""

    @pytest.fixture
    def mock_fetcher(self):
        """Create mock fetcher for testing."""
        fetcher = WikipediaSyncFetcher()
        return fetcher

    def test_network_timeout_recovery(self, mock_fetcher):
        """Test recovery from network timeouts."""
        with patch.object(mock_fetcher.ar_fetcher, 'fetch_page_info') as mock_ar:
            # First call times out, second succeeds
            mock_ar.side_effect = [
                PageInfo(title="مصر", exists=False, error="Timeout"),
                PageInfo(title="مصر", exists=True, content="Arabic content")
            ]

            result = mock_fetcher.fetch_arabic_and_english_pages("مصر")

            assert mock_ar.call_count == 2  # Two attempts
            assert result['arabic']['exists'] is True

    def test_langlink_fallback_strategies(self, mock_fetcher):
        """Test various English page finding strategies."""
        arabic_page = PageInfo(
            title="كرة القدم",
            exists=True,
            langlinks={'en': 'Football', 'fr': 'Football', 'de': 'Fußball'}
        )

        with patch.object(mock_fetcher.ar_fetcher, 'fetch_page_info', return_value=arabic_page), \
             patch.object(mock_fetcher.en_fetcher, 'fetch_page_info') as mock_en:

            mock_en.return_value = PageInfo(title="Football", exists=True, content="English content")

            result = mock_fetcher.fetch_arabic_and_english_pages("كرة القدم")

            assert result['sync_possible'] is True
            assert result['english']['title'] == "Football"

    def test_concurrent_access_safety(self, mock_fetcher):
        """Test thread safety of concurrent access."""
        import threading
        import time

        results = []
        errors = []

        def worker(worker_id: int):
            try:
                for i in range(10):
                    result = mock_fetcher.fetch_arabic_and_english_pages(f"Test{i}_{worker_id}")
                    results.append(result)
            except Exception as e:
                errors.append(e)

        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(results) == 50  # 5 workers * 10 requests each
        assert len(errors) == 0   # No thread safety issues

    def test_performance_under_load(self, mock_fetcher):
        """Test fetcher performance under simulated load."""
        import time

        start_time = time.time()
        pages = [f"PerformanceTest{i}" for i in range(100)]

        results = {}
        for page in pages:
            result = mock_fetcher.fetch_arabic_and_english_pages(page)
            results[page] = result

        end_time = time.time()

        total_time = end_time - start_time
        avg_time_per_page = total_time / len(pages)

        # Performance assertions
        assert total_time < 60  # Should complete in less than 1 minute
        assert avg_time_per_page < 0.5  # Average less than 0.5 seconds per page

        print(f"Processed {len(pages)} pages in {total_time:.2f}s ({avg_time_per_page:.2f}s/page)")

    def test_error_classification(self, mock_fetcher):
        """Test proper error classification for different failure modes."""
        test_cases = [
            {
                'error': 'Arabic page does not exist',
                'expected_category': 'arabic_missing',
                'sync_possible': False
            },
            {
                'error': 'No corresponding English page found',
                'expected_category': 'no_english_equivalent',
                'sync_possible': False
            },
            {
                'error': 'Network timeout',
                'expected_category': 'network_error',
                'sync_possible': False
            }
        ]

        for test_case in test_cases:
            with patch.object(mock_fetcher.ar_fetcher, 'fetch_page_info') as mock_ar:
                mock_ar.return_value = PageInfo(
                    title="TestPage",
                    exists=test_case.get('arabic_exists', True),
                    error=test_case['error']
                )

                result = mock_fetcher.fetch_arabic_and_english_pages("TestPage")

                assert result['sync_possible'] == test_case['sync_possible']
                if not test_case['sync_possible']:
                    assert test_case['error'] in result['error']

    @pytest.mark.parametrize("batch_size,expected_success_rate", [
        (10, 0.9),
        (50, 0.85),
        (100, 0.8)
    ])
    def test_batch_processing_efficiency(self, batch_size, expected_success_rate):
        """Test batch processing at different scales."""
        from tasks.InfoboxSync.fetch_advanced_examples import BatchFetchProcessor

        processor = BatchFetchProcessor(max_workers=3)
        test_pages = [f"BatchTest{i}" for i in range(batch_size)]

        # Mock successful responses
        with patch('tasks.InfoboxSync.fetch.fetch_wikipedia_data') as mock_fetch:
            mock_fetch.return_value = {
                'arabic': {'title': 'Test', 'exists': True, 'content': 'Content'},
                'english': {'title': 'Test', 'exists': True, 'content': 'Content'},
                'sync_possible': True,
                'error': None
            }

            batch_result = processor.process_page_batch(test_pages, handle_errors=False)

            assert len(batch_result['results']) == batch_size
            success_count = sum(1 for r in batch_result['results'].values() if r['success'])
            actual_success_rate = success_count / batch_size

            assert actual_success_rate >= expected_success_rate

            # Performance check
            summary = batch_result['summary']
            assert summary['total'] == batch_size
            assert summary['successful'] == success_count
```

## Migration Patterns

### Gradual Migration from Legacy Code

```python
import warnings
from typing import Union, Optional

class LegacyAdapter:
    """Adapter to ease migration from legacy fetch interfaces."""

    def __init__(self):
        self.new_fetcher = WikipediaSyncFetcher()

    def fetch_page_legacy_format(self, arabic_title: str,
                               return_old_format: bool = True) -> Union[Dict, SyncResult]:
        """
        Fetch page with option to return legacy format for gradual migration.

        Args:
            arabic_title: Arabic page title
            return_old_format: If True, return old dict format for compatibility

        Returns:
            Either legacy dict format or new SyncResult format
        """
        sync_result = self.new_fetcher.fetch_sync_result(arabic_title)

        if return_old_format:
            # Convert SyncResult to old dict format
            warnings.warn(
                "Using legacy dict format. Consider migrating to SyncResult format.",
                DeprecationWarning,
                stacklevel=2
            )

            return {
                'arabic': {
                    'title': sync_result.arabic.title,
                    'exists': sync_result.arabic.exists,
                    'content': sync_result.arabic.content,
                    'langlinks': sync_result.arabic.langlinks,
                    'error': sync_result.arabic.error
                },
                'english': {
                    'title': sync_result.english.title if sync_result.english else None,
                    'exists': sync_result.english.exists if sync_result.english else False,
                    'content': sync_result.english.content if sync_result.english else None,
                    'langlinks': sync_result.english.langlinks if sync_result.english else None,
                    'error': sync_result.english.error if sync_result.english else None
                },
                'sync_possible': sync_result.sync_possible,
                'error': sync_result.error
            }

        return sync_result

class ConfigurationMigrationHelper:
    """Helper for migrating configuration settings."""

    @staticmethod
    def convert_legacy_config(legacy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert legacy configuration to new format."""
        new_config = {
            'fetcher_type': 'WikipediaSyncFetcher',
            'observer_type': legacy_config.get('observer', 'LoggingFetchObserver'),
            'max_retries': legacy_config.get('max_retries', 3),
            'timeout': legacy_config.get('timeout_seconds', 30),
            'rate_limit': legacy_config.get('requests_per_minute', 30)
        }

        # Handle deprecated settings
        if 'use_cache' in legacy_config:
            warnings.warn("'use_cache' is deprecated. Consider using external caching.",
                         DeprecationWarning)

        if 'old_api_format' in legacy_config:
            warnings.warn("'old_api_format' is deprecated. Use SyncResult format.",
                         DeprecationWarning)

        return new_config

# Utility functions for migration
def migrate_batch_processing(old_batch_function, new_fetcher):
    """Migrate batch processing functions to new interface."""

    def new_batch_function(page_titles):
        """New batch function using modern interface."""
        warnings.warn("Batch function migrated. Review implementation for optimizations.",
                     UserWarning, stacklevel=2)

        results = {}
        for title in page_titles:
            try:
                sync_result = new_fetcher.fetch_sync_result(title)
                results[title] = {
                    'success': sync_result.sync_possible,
                    'data': sync_result,
                    'error': sync_result.error
                }
            except Exception as e:
                results[title] = {
                    'success': False,
                    'data': None,
                    'error': str(e)
                }

        return results

    return new_batch_function
```

These advanced patterns demonstrate how to build robust, scalable, and maintainable fetch implementations for complex Wikipedia data synchronization scenarios. The examples show proper error handling, performance optimization, and integration with modern Python development practices.