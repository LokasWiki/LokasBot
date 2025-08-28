# Fetch Module Troubleshooting Guide

## Overview

This guide provides solutions to common issues encountered when using the Fetch module of the InfoboxSync pipeline. Issues are categorized by symptom, cause, and resolution steps.

## Quick Diagnosis

### Health Check Script

Before diving into specific issues, run this health check:

```python
# quick_health_check.py
from tasks.InfoboxSync.fetch import fetch_wikipedia_data
import logging

logging.basicConfig(level=logging.INFO)

def run_health_check():
    """Quick diagnostic check for fetch system."""
    print("🔍 Fetch Module Health Check")
    print("=" * 50)

    # Test 1: Basic import
    try:
        from tasks.InfoboxSync.fetch import fetch_wikipedia_data
        print("✅ Module import: OK")
    except ImportError as e:
        print(f"❌ Module import: FAILED - {e}")
        return False

    # Test 2: Simple fetch
    try:
        result = fetch_wikipedia_data("Test")
        print("⚠️  Simple fetch test: No error (expected for non-existent page)")
    except Exception as e:
        print(f"❌ Simple fetch test: FAILED - {e}")

    print("\nHealth check complete")
    return True

if __name__ == "__main__":
    run_health_check()
```

## Common Issues and Solutions

### 1. ImportError: pywikibot is required

**Symptom:**
```
ImportError: pywikibot is required for Wikipedia operations. Install with: pip install pywikibot
```

**Causes:**
- Pywikibot not installed
- Import path issues

**Solutions:**

**A. Install pywikibot:**
```bash
pip install pywikibot
# or for specific versions:
pip install pywikibot==8.3.2
```

**B. Environment issues:**
```bash
# Check Python environment
python --version
which python
pip list | grep pywikibot

# Use virtual environment
python -m venv wiki_env
source wiki_env/bin/activate  # Linux/Mac
wiki_env\Scripts\activate     # Windows
pip install pywikibot
```

**C. Alternative installation methods:**
```bash
# Using conda
conda install -c conda-forge pywikibot

# From source
git clone https://gerrit.wikimedia.org/r/pywikibot/core.git
cd core
python setup.py install
```

### 2. SyncResult errors: Arabic page does not exist

**Symptom:**
```python
result = fetch_wikipedia_data("NonExistentArabicPage")
# Result: {'sync_possible': False, 'error': "Arabic page 'NonExistentArabicPage' does not exist"}
```

**Causes:**
- Page actually doesn't exist
- Typos in page title
- Encoding issues

**Solutions:**

**A. Verify page existence:**
```python
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

def verify_page_exists(ar_title: str) -> bool:
    """Check if Arabic page exists before sync."""
    fetcher = WikipediaSyncFetcher()

    # Check Arabic page only
    ar_result = fetcher.ar_fetcher.fetch_page_info(ar_title)
    return ar_result.exists

# Usage
if verify_page_exists("مصر"):
    result = fetch_wikipedia_data("مصر")
else:
    print("Arabic page does not exist")
```

**B. Handle encoding issues:**
```python
def sanitize_arabic_title(title: str) -> str:
    """Clean and validate Arabic page title."""
    # Remove leading/trailing whitespace
    title = title.strip()

    # Replace problematic characters
    title = title.replace('أ', 'ا')  # Normalize alef
    title = title.replace('إ', 'ا')  # Normalize alef with hamza
    title = title.replace('آ', 'ا')  # Normalize alef with madda

    return title

# Usage
clean_title = sanitize_arabic_title("   أحمد    ")
result = fetch_wikipedia_data(clean_title)
```

**C. Log all errors for debugging:**
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fetch_debug.log'),
        logging.StreamHandler()
    ]
)

# Now run fetch operations - detailed logs will be captured
result = fetch_wikipedia_data("مشكلة")
```

### 3. No corresponding English page found

**Symptom:**
```python
result = fetch_wikipedia_data("UniqueArabicConcept")
# Result: {'sync_possible': False, 'error': "No corresponding English page found"}
```

**Causes:**
- Page exists in Arabic but not in English
- Missing language links (interwiki links)
- Language link parsing issues

**Solutions:**

**A. Manual langlink checking:**
```python
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

def investigate_langlinks(ar_title: str) -> dict:
    """Investigate language links for a page."""
    fetcher = WikipediaSyncFetcher()

    # Get Arabic page
    ar_page = fetcher.ar_fetcher.fetch_page_info(ar_title)

    if not ar_page.exists:
        return {'error': 'Arabic page does not exist'}

    analysis = {
        'arabic_title': ar_page.title,
        'has_langlinks': bool(ar_page.langlinks),
        'langlinks_count': len(ar_page.langlinks or {}),
        'available_languages': list(ar_page.langlinks.keys()) if ar_page.langlinks else []
    }

    # Check for English specifically
    if ar_page.langlinks and 'en' in ar_page.langlinks:
        analysis['english_title'] = ar_page.langlinks['en']
        en_page = fetcher.en_fetcher.fetch_page_info(ar_page.langlinks['en'])
        analysis['english_exists'] = en_page.exists
        if not en_page.exists:
            analysis['english_error'] = en_page.error
    else:
        analysis['english_title'] = None
        analysis['english_exists'] = False

    return analysis

# Usage
analysis = investigate_langlinks("الجبر")
print(f"Langlinks: {analysis['available_languages']}")
if analysis['english_title']:
    print(f"English equivalent: {analysis['english_title']}")
```

**B. Alternative English page discovery:**
```python
def find_alternative_english_title(ar_title: str) -> str:
    """Try to find English equivalent through various methods."""
    # Method 1: Direct translation (basic)
    arabic_to_english_translations = {
        'كرة القدم': 'Football',
        'باريس': 'Paris',
        'ألمانيا': 'Germany'
    }

    if ar_title in arabic_to_english_translations:
        return arabic_to_english_translations[ar_title]

    # Method 2: Remove Arabic-specific prefixes/suffixes
    cleaned = ar_title.replace('ال', '')  # Remove 'al-'

    # Method 3: check other language codes
    alternative_codes = ['en-us', 'en-gb', 'en-ca']

    return None  # Fallback

# Usage
alt_en_title = find_alternative_english_title("الجبر")
if alt_en_title:
    print(f"Alternative English title found: {alt_en_title}")
```

### 4. Network and API Issues

**Symptom:**
```
TimeoutError: Request timed out
HTTPError: 429 Client Error: Too Many Requests
```

**Causes:**
- Network connectivity issues
- Rate limiting by Wikipedia
- API downtime
- DNS resolution problems

**Solutions:**

**A. Implement retry logic:**
```python
import time
import random
from functools import wraps

class WikipediaRetryMechanism:
    """Intelligent retry mechanism for Wikipedia API calls."""

    def __init__(self, max_attempts: int = 3, backoff_factor: float = 2.0):
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor

    def execute_with_retry(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry."""
        last_exception = None

        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except (TimeoutError, ConnectionError, OSError) as e:
                last_exception = e

                if attempt < self.max_attempts - 1:
                    # Exponential backoff with jitter
                    wait_time = self.backoff_factor ** attempt + random.uniform(0, 1)
                    print(f"Attempt {attempt + 1} failed, retrying in {wait_time:.1f}s: {e}")
                    time.sleep(wait_time)
                else:
                    print(f"Final attempt failed: {e}")

        raise last_exception

# Usage
retry_mechanism = WikipediaRetryMechanism(max_attempts=3)

def robust_fetch(page_title: str):
    return retry_mechanism.execute_with_retry(fetch_wikipedia_data, page_title)

# Test
try:
    result = robust_fetch("مصر")
    print("Fetch successful after retry")
except Exception as e:
    print(f"All retry attempts failed: {e}")
```

**B. Rate limit handling:**
```python
import time

class RateLimiter:
    """Rate limiter for Wikipedia API calls."""

    def __init__(self, requests_per_minute: int = 20):
        self.requests_per_minute = requests_per_minute
        self.requests = []
        self.min_interval = 60.0 / requests_per_minute

    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        now = time.time()
        cutoff = now - 60  # 1 minute window

        # Remove old requests
        self.requests = [req for req in self.requests if req > cutoff]

        if len(self.requests) >= self.requests_per_minute:
            # Wait until oldest request expires
            wait_time = self.requests[0] - cutoff
            if wait_time > 0:
                time.sleep(wait_time)
            self.requests = self.requests[1:]

        self.requests.append(now)

# Usage in batch processing
rate_limiter = RateLimiter(requests_per_minute=15)

def rate_limited_fetch(pages):
    results = {}
    for page in pages:
        rate_limiter.wait_if_needed()
        results[page] = fetch_wikipedia_data(page)
    return results
```

**C. Network diagnostics:**
```python
import socket
import requests

def diagnose_network_connectivity():
    """Diagnose network connectivity to Wikipedia."""
    diagnoses = {}

    # Test 1: DNS resolution
    try:
        ip = socket.gethostbyname('ar.wikipedia.org')
        diagnoses['dns_resolution'] = f"✅ ar.wikipedia.org -> {ip}"
    except socket.error as e:
        diagnoses['dns_resolution'] = f"❌ DNS resolution failed: {e}"

    # Test 2: Basic connectivity
    try:
        response = requests.get('https://ar.wikipedia.org/api/rest_v1/', timeout=10)
        diagnoses['api_connectivity'] = f"✅ HTTP {response.status_code}"
    except requests.RequestException as e:
        diagnoses['api_connectivity'] = f"❌ HTTP request failed: {e}"

    # Test 3: Pywikibot connectivity
    try:
        import pywikibot
        site = pywikibot.Site('ar')
        diagnoses['pywikibot_site'] = f"✅ Site created for {site}"
    except Exception as e:
        diagnoses['pywikibot_site'] = f"❌ Pywikibot site creation failed: {e}"

    return diagnoses

# Usage
diagnostics = diagnose_network_connectivity()
for test, result in diagnostics.items():
    print(f"{test}: {result}")
```

### 5. Pywikibot Configuration Issues

**Symptom:**
```
NoUsernameError: User is not logged in
SiteDefinitionError: Unknown site
```

**Causes:**
- Missing pywikibot user configuration
- Incorrect site configuration
- Authentication issues

**Solutions:**

**A. Configure pywikibot:**
```bash
# Step 1: Generate config files
pywikibot generate_user_files

# Step 2: Configure user-config.py
# Edit the generated user-config.py file
vim ~/.pywikibot/user-config.py  # Linux/Mac
# notepad %USERPROFILE%\.pywikibot\user-config.py  # Windows
```

**B. Minimal user-config.py:**
```python
# Minimal configuration for Wikipedia access
mylang = 'ar'           # Default language
family = 'wikipedia'    # Wikimedia family

# For API access without login (read-only operations)
usernames = {
    'wikipedia': {
        'ar': 'YourBotName',  # Optional bot name
        'en': 'YourBotName'
    }
}

# Rate limiting
maxlag = 5              # Maximum lag in seconds
put_throttle = 1.0      # Throttle for writes (we only read)

# Disable SSL verification if needed (not recommended for production)
# verify_ssl = False
```

**C. Test configuration:**
```python
import pywikibot

def test_pywikibot_config():
    """Test pywikibot configuration."""
    try:
        # Test Arabic Wikipedia
        site_ar = pywikibot.Site('ar')
        print(f"✅ Arabic site: {site_ar}")

        # Test English Wikipedia
        site_en = pywikibot.Site('en')
        print(f"✅ English site: {site_en}")

        # Test page fetch
        page = pywikibot.Page(site_ar, 'مصر')
        if page.exists():
            print("✅ Page fetch test passed")
            print(f"   Page length: {len(page.text)} chars")
        else:
            print("❌ Test page does not exist")

    except Exception as e:
        print(f"❌ Pywikibot configuration error: {e}")

test_pywikibot_config()
```

### 6. Memory and Performance Issues

**Symptom:**
```
MemoryError: Out of memory during large batch processing
Slow response times, high CPU usage
```

**Causes:**
- Large page content stored in memory
- No connection pooling
- Inefficient batch processing

**Solutions:**

**A. Memory-efficient processing:**
```python
def memory_efficient_batch_processing(page_titles, batch_size=10):
    """Process pages in batches to manage memory usage."""
    results = {}

    for i in range(0, len(page_titles), batch_size):
        batch = page_titles[i:i + batch_size]

        # Process batch
        batch_results = {}
        for title in batch:
            result = fetch_wikipedia_data(title)

            # Store only essential data to save memory
            batch_results[title] = {
                'sync_possible': result['sync_possible'],
                'arabic_exists': result['arabic']['exists'] if result['arabic'] else False,
                'english_exists': result['english']['exists'] if result['english'] else False,
                'error': result['error'],
                'metadata': {
                    'arabic_length': len(result['arabic']['content']) if result.get('arabic', {}).get('content') else 0,
                    'english_length': len(result['english']['content']) if result.get('english', {}).get('content') else 0
                }
            }

        # Store batch results
        results.update(batch_results)

        # Force garbage collection
        import gc
        gc.collect()

    return results

# Usage
pages = ['مصر', 'باريس', 'برلين', 'روما'] * 25  # 100 pages
results = memory_efficient_batch_processing(pages, batch_size=10)
```

**B. Streaming large content:**
```python
def process_large_pages_with_streaming(page_titles):
    """Process large pages without storing all content in memory."""
    summary_results = {}

    for title in page_titles:
        result = fetch_wikipedia_data(title)

        if result['sync_possible']:
            arabic_content = result['arabic']['content'] or ''
            english_content = result['english']['content'] or ''

            # Calculate metrics without storing full content
            summary_results[title] = {
                'sync_possible': True,
                'content_metrics': {
                    'arabic_chars': len(arabic_content),
                    'english_chars': len(english_content),
                    'arabic_infobox_count': arabic_content.count('{{صندوق'),
                    'english_infobox_count': english_content.count('{{Infobox')
                }
            }

            # Clear content to free memory
            result['arabic']['content'] = None
            result['english']['content'] = None
        else:
            summary_results[title] = {
                'sync_possible': False,
                'error': result['error']
            }

    return summary_results
```

### 7. Threading and Concurrency Issues

**Symptom:**
```
Threading errors, race conditions, inconsistent results
```

**Causes:**
- Shared state in single fetcher instance
- Thread-unsafe pywikibot usage
- Improper thread synchronization

**Solutions:**

**A. Thread-safe implementation:**
```python
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class ThreadSafeBatchProcessor:
    """Thread-safe batch processor for concurrent fetching."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.lock = threading.Lock()
        self.processed_count = 0

    def process_concurrent(self, page_titles):
        """Process pages concurrently with proper synchronization."""
        results = {}
        errors = []

        def safe_fetch(title):
            """Thread-safe fetch operation."""
            try:
                result = fetch_wikipedia_data(title)

                with self.lock:
                    self.processed_count += 1
                    if self.processed_count % 10 == 0:
                        print(f"Processed {self.processed_count}/{len(page_titles)} pages")

                return title, result, None
            except Exception as e:
                with self.lock:
                    errors.append((title, str(e)))
                return title, None, str(e)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_title = {
                executor.submit(safe_fetch, title): title
                for title in page_titles
            }

            for future in as_completed(future_to_title):
                title, result, error = future.result()

                if error:
                    results[title] = {'success': False, 'error': error}
                else:
                    results[title] = {'success': True, 'data': result}

        return {
            'results': results,
            'errors': errors,
            'summary': {
                'total': len(page_titles),
                'successful': len([r for r in results.values() if r['success']]),
                'failed': len(errors)
            }
        }

# Usage
processor = ThreadSafeBatchProcessor(max_workers=3)
result = processor.process_concurrent(['مصر', 'باريس', 'برلين', 'روما'])

print(f"Success rate: {result['summary']['successful']}/{result['summary']['total']}")
```

**B. Per-thread fetcher instances:**
```python
def thread_local_fetcher():
    """Create thread-local fetcher instances."""
    import threading
    from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

    # Thread-local storage for fetchers
    local_data = threading.local()

    if not hasattr(local_data, 'fetcher'):
        local_data.fetcher = WikipediaSyncFetcher()

    return local_data.fetcher

def concurrent_fetch_with_isolation(page_titles):
    """Concurrent fetching with thread isolation."""
    def fetch_in_thread(title):
        """Fetch in isolated thread context."""
        fetcher = thread_local_fetcher()
        return title, fetch_wikipedia_data(title)

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_title = {
            executor.submit(fetch_in_thread, title): title
            for title in page_titles
        }

        for future in as_completed(future_to_title):
            title, result = future.result()
            results[title] = result

    return results
```

## Debug Tools and Diagnostic Scripts

### Comprehensive Debug Script

```python
# debug_fetch.py - Comprehensive debugging tool
import logging
import json
import time
from tasks.InfoboxSync.fetch import fetch_wikipedia_data
from tasks.InfoboxSync.fetch.sync_fetcher import WikipediaSyncFetcher

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fetch_debug.log'),
        logging.StreamHandler()
    ]
)

class FetchDebugger:
    """Comprehensive debugging tool for fetch operations."""

    def __init__(self):
        self.fetcher = WikipediaSyncFetcher()

    def debug_single_page(self, arabic_title: str) -> dict:
        """Debug single page fetch operation."""
        debug_info = {
            'start_time': time.time(),
            'arabic_title': arabic_title,
            'steps': []
        }

        try:
            # Step 1: Test Arabic page
            debug_info['steps'].append({'step': 'arabic_fetch_start', 'time': time.time()})
            ar_page = self.fetcher.ar_fetcher.fetch_page_info(arabic_title)

            debug_info['steps'].append({
                'step': 'arabic_fetch_complete',
                'time': time.time(),
                'exists': ar_page.exists,
                'error': ar_page.error,
                'has_content': bool(ar_page.content),
                'content_length': len(ar_page.content) if ar_page.content else 0,
                'has_langlinks': bool(ar_page.langlinks)
            })

            if not ar_page.exists:
                debug_info['conclusion'] = 'arabic_page_missing'
                return debug_info

            # Step 2: Test English page discovery
            debug_info['steps'].append({'step': 'english_discovery_start', 'time': time.time()})

            if ar_page.langlinks and 'en' in ar_page.langlinks:
                english_title = ar_page.langlinks['en']
                debug_info['steps'].append({
                    'step': 'english_title_found',
                    'english_title': english_title
                })

                # Step 3: Test English page fetch
                debug_info['steps'].append({'step': 'english_fetch_start', 'time': time.time()})
                en_page = self.fetcher.en_fetcher.fetch_page_info(english_title)

                debug_info['steps'].append({
                    'step': 'english_fetch_complete',
                    'time': time.time(),
                    'exists': en_page.exists,
                    'error': en_page.error,
                    'content_length': len(en_page.content) if en_page.content else 0
                })

                debug_info['conclusion'] = 'sync_possible' if en_page.exists else 'english_page_missing'
            else:
                debug_info['steps'].append({'step': 'no_english_langlink'})
                debug_info['conclusion'] = 'no_english_equivalent'

        except Exception as e:
            debug_info['error'] = str(e)
            debug_info['conclusion'] = 'exception'

        debug_info['total_time'] = time.time() - debug_info['start_time']

        # Save debug info
        with open(f'debug_{arabic_title.replace("/", "_")}.json', 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, ensure_ascii=False, indent=2)

        return debug_info

    def compare_pages(self, arabic_title: str, english_title: str) -> dict:
        """Compare Arabic and English page information."""
        ar_page = self.fetcher.ar_fetcher.fetch_page_info(arabic_title)
        en_page = self.fetcher.en_fetcher.fetch_page_info(english_title)

        return {
            'arabic': {
                'title': ar_page.title,
                'exists': ar_page.exists,
                'content_length': len(ar_page.content) if ar_page.content else 0,
                'langlinks': ar_page.langlinks
            },
            'english': {
                'title': en_page.title,
                'exists': en_page.exists,
                'content_length': len(en_page.content) if en_page.content else 0
            },
            'comparison': {
                'both_exist': ar_page.exists and en_page.exists,
                'content_ratio': (
                    len(en_page.content) / len(ar_page.content)
                    if ar_page.content and en_page.content else 0
                )
            }
        }

# Usage examples
if __name__ == "__main__":
    debugger = FetchDebugger()

    # Debug specific page
    debug_info = debugger.debug_single_page("مصر")
    print(f"Debug conclusion: {debug_info['conclusion']}")
    print(f"Total time: {debug_info['total_time']:.2f}s")

    # Compare pages
    comparison = debugger.compare_pages("كرة القدم", "Football")
    print(f"Comparison: {json.dumps(comparison, ensure_ascii=False, indent=2)}")
```

## Common Configuration Issues

### Virtual Environment Problems

**Symptom:**
```
ModuleNotFoundError in virtual environment
```

**Solutions:**
```bash
# Always activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install all dependencies
pip install pywikibot requests

# Verify installation
python -c "import pywikibot; print('Pywikibot OK')"
```

### IDE and Development Environment Issues

**Symptom:**
```
Import errors in IDE but works on command line
```

**Solutions:**
- Ensure IDE uses correct Python interpreter
- Restart IDE after package installation
- Check virtual environment configuration in IDE
- Verify PYTHONPATH settings

### Encoding and Unicode Issues

**Symptom:**
```
UnicodeDecodeError: 'utf-8' codec can't decode bytes
```

**Solutions:**
```python
# Ensure UTF-8 encoding in all operations
import sys

# Set default encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Use proper encoding when reading files
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Handle Arabic text properly in API calls
response = requests.get('https://ar.wikipedia.org/api/rest_v1/page/summary/مصر')
response.encoding = 'utf-8'
content = response.json()
```

This troubleshooting guide provides comprehensive solutions for the most common issues encountered when using the Fetch module. For additional support, check the logs, review the API documentation, and consider opening an issue on the project repository.