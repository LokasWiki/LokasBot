# Photo Lab - API Reference

This document provides detailed API documentation for all classes and methods in the Photo Lab task.

## Table of Contents

- [Entities](#entities)
  - [PhotoRequest](#photorequest)
  - [ArchiveEntry](#archiveentry)
  - [ArchivePage](#archivepage)
- [Repository](#repository)
  - [WikiRepository](#wikirepository)
- [Use Cases](#use-cases)
  - [ExtractPendingRequests](#extractpendingrequests)
  - [CheckRequestStatus](#checkrequeststatus)
  - [ManageArchives](#managearchives)
  - [ArchiveCompletedRequests](#archivecompletedrequests)
- [Controller](#controller)
  - [PhotoLabController](#photolabcontroller)

---

## Entities

### PhotoRequest

**File**: `domain/entities/photo_request.py`

Represents a photo workshop request.

#### Constructor

```python
PhotoRequest(
    page_name: str,
    template_text: str,
    has_perspective: bool = False,
    request_page_title: str = ""
)
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page_name` | `str` | required | The article page name being requested |
| `template_text` | `str` | required | Full template text from main page |
| `has_perspective` | `bool` | `False` | Whether request has perspective template |
| `request_page_title` | `str` | auto-generated | Full title of request page |

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `page_name` | `str` | Article page name |
| `template_text` | `str` | Template text |
| `has_perspective` | `bool` | Ready for archiving flag |
| `request_page_title` | `str` | Full request page title |

#### Methods

##### `mark_as_archivable()`

```python
def mark_as_archivable(self) -> None
```

Mark this request as ready for archiving.

**Example**:
```python
request = PhotoRequest(page_name="Test", template_text="{{...}}")
request.mark_as_archivable()
print(request.has_perspective)  # True
```

##### `is_ready_for_archive()`

```python
def is_ready_for_archive(self) -> bool
```

Check if this request is ready to be archived.

**Returns**: `True` if `has_perspective` is `True`

**Example**:
```python
if request.is_ready_for_archive():
    archive_request(request)
```

##### `__str__()`

```python
def __str__(self) -> str
```

String representation.

**Returns**: `"PhotoRequest(page='Test Page', has perspective)"`

---

### ArchiveEntry

**File**: `domain/entities/archive_entry.py`

Represents an archived request entry.

#### Constructor

```python
ArchiveEntry(
    page_name: str,
    template_text: str,
    archived_at: Optional[datetime] = None,
    archive_page_number: int = 0
)
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page_name` | `str` | required | The page name that was requested |
| `template_text` | `str` | required | Template text being archived |
| `archived_at` | `Optional[datetime]` | `datetime.now()` | Timestamp of archiving |
| `archive_page_number` | `int` | `0` | Archive page number |

#### Methods

##### `get_archive_page_title()`

```python
def get_archive_page_title(
    self,
    base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف"
) -> str
```

Get the full archive page title.

**Parameters**:
- `base_prefix` (`str`): Base prefix for archive pages

**Returns**: Full title (e.g., `"ويكيبيديا:ورشة الصور/أرشيف 42"`)

##### `format_for_archive()`

```python
def format_for_archive(self) -> str
```

Format the entry for inclusion in an archive page.

**Returns**: Formatted text with newlines

---

### ArchivePage

**File**: `domain/entities/archive_entry.py`

Represents an archive page holding multiple entries.

#### Constructor

```python
ArchivePage(
    page_number: int,
    entries: list = None,
    base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف"
)
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page_number` | `int` | required | Archive page number |
| `entries` | `list` | `[]` | List of ArchiveEntry objects |
| `base_prefix` | `str` | `"ويكيبيديا:ورشة الصور/أرشيف"` | Page title prefix |

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `title` | `str` | Full page title (e.g., `"ويكيبيديا:ورشة الصور/أرشيف 1"`) |
| `entry_count` | `int` | Number of entries in archive |

#### Methods

##### `is_full()`

```python
def is_full(self, max_entries: int = 10) -> bool
```

Check if the archive page is full.

**Parameters**:
- `max_entries` (`int`): Maximum entries allowed (default: 10)

**Returns**: `True` if archive has reached capacity

##### `add_entry()`

```python
def add_entry(self, entry: ArchiveEntry) -> None
```

Add an entry to this archive page.

**Parameters**:
- `entry` (`ArchiveEntry`): Entry to add

##### `get_header()`

```python
def get_header(self) -> str
```

Get the standard archive page header.

**Returns**: Header with templates

```wikitext
{{تصفح أرشيف|42}}
{{تمت الأرشفة}}
```

##### `get_content()`

```python
def get_content(self) -> str
```

Get the full content of the archive page.

**Returns**: Complete page content including header and all entries

---

## Repository

### WikiRepository

**File**: `domain/repositories/wiki_repository.py`

Abstract interface for wiki operations. Implemented by `PywikibotWiki`.

#### Methods

##### `get_main_requests_page_content()`

```python
@abstractmethod
def get_main_requests_page_content(self) -> str
```

Get the content of the main requests page.

**Returns**: Full wikitext content

**Raises**: `Exception` if page cannot be retrieved

##### `update_main_requests_page()`

```python
@abstractmethod
def update_main_requests_page(
    self,
    content: str,
    summary: str
) -> bool
```

Update the main requests page.

**Parameters**:
- `content` (`str`): New page content
- `summary` (`str`): Edit summary

**Returns**: `True` if successful

##### `get_request_page_content()`

```python
@abstractmethod
def get_request_page_content(self, page_title: str) -> str
```

Get content of a specific request page.

**Parameters**:
- `page_title` (`str`): Full page title

**Returns**: Page content or empty string

##### `has_template()`

```python
@abstractmethod
def has_template(
    self,
    page_title: str,
    template_name: str
) -> bool
```

Check if a page contains a specific template.

**Parameters**:
- `page_title` (`str`): Page to check
- `template_name` (`str`): Template to look for

**Returns**: `True` if template exists

##### `get_all_archive_pages()`

```python
@abstractmethod
def get_all_archive_pages(
    self,
    base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف"
) -> List[Tuple[int, str]]
```

Get all existing archive pages.

**Parameters**:
- `base_prefix` (`str`): Archive page prefix

**Returns**: List of `(page_number, page_title)` tuples, sorted by number

##### `create_archive_page()`

```python
@abstractmethod
def create_archive_page(
    self,
    archive_page: ArchivePage,
    summary: str
) -> bool
```

Create a new archive page.

**Parameters**:
- `archive_page` (`ArchivePage`): Entity to create
- `summary` (`str`): Edit summary

**Returns**: `True` if successful

##### `update_archive_page()`

```python
@abstractmethod
def update_archive_page(
    self,
    archive_page: ArchivePage,
    summary: str
) -> bool
```

Update an existing archive page.

**Parameters**:
- `archive_page` (`ArchivePage`): Entity with updated content
- `summary` (`str`): Edit summary

**Returns**: `True` if successful

##### `page_exists()`

```python
@abstractmethod
def page_exists(self, page_title: str) -> bool
```

Check if a page exists.

**Parameters**:
- `page_title` (`str`): Page to check

**Returns**: `True` if page exists

##### `count_templates_in_page()`

```python
@abstractmethod
def count_templates_in_page(
    self,
    page_title: str,
    template_name: str
) -> int
```

Count template occurrences in a page.

**Parameters**:
- `page_title` (`str`): Page to check
- `template_name` (`str`): Template to count

**Returns**: Number of occurrences

---

## Use Cases

### ExtractPendingRequests

**File**: `domain/use_cases/extract_pending_requests.py`

Extracts photo requests from the main page.

#### Constructor

```python
ExtractPendingRequests(wiki_repository: WikiRepository)
```

#### Methods

##### `execute()`

```python
def execute(self) -> List[PhotoRequest]
```

Execute the use case.

**Returns**: List of `PhotoRequest` entities

**Raises**: `Exception` if page cannot be retrieved

**Example**:
```python
extract_use_case = ExtractPendingRequests(wiki_repo)
requests = extract_use_case.execute()
for request in requests:
    print(request.page_name)
```

---

### CheckRequestStatus

**File**: `domain/use_cases/check_request_status.py`

Checks which requests have the perspective template.

#### Constructor

```python
CheckRequestStatus(wiki_repository: WikiRepository)
```

#### Methods

##### `execute()`

```python
def execute(self, requests: List[PhotoRequest]) -> List[PhotoRequest]
```

Check status of all requests.

**Parameters**:
- `requests` (`List[PhotoRequest]`): Requests to check

**Returns**: Same list with `has_perspective` updated

##### `get_archivable_requests()`

```python
def get_archivable_requests(
    self,
    requests: List[PhotoRequest]
) -> List[PhotoRequest]
```

Filter and return only archivable requests.

**Parameters**:
- `requests` (`List[PhotoRequest]`): All requests

**Returns**: Requests with `has_perspective=True`

---

### ManageArchives

**File**: `domain/use_cases/manage_archives.py`

Manages archive pages.

#### Constructor

```python
ManageArchives(wiki_repository: WikiRepository)
```

#### Methods

##### `get_or_create_latest_archive()`

```python
def get_or_create_latest_archive(self) -> ArchivePage
```

Get latest archive or create new one if full or bot-restricted.

This method intelligently handles:
- **Full archives**: Skips archives with 10+ entries
- **Bot-restricted archives**: Skips archives with `{{bots}}` or `{{nobots}}` templates
- **Auto-creation**: Creates new archive if all existing ones are unusable

**Process**:
1. Find the highest numbered archive
2. Check if bot-restricted → Skip if restricted
3. Check if full (10 entries) → Skip if full
4. If unusable, try next number until finding/creating usable archive

**Returns**: `ArchivePage` entity ready for entries

**Example**:
```
Archive 52: 10 entries (FULL) → Skip
Archive 53: {{bots}} restriction → Skip
Archive 54: Doesn't exist → Create & Return
```

##### `add_entry_to_archive()`

```python
def add_entry_to_archive(
    self,
    archive_page: ArchivePage,
    entry: ArchiveEntry
) -> bool
```

Add entry to archive page.

**Parameters**:
- `archive_page` (`ArchivePage`): Archive to add to
- `entry` (`ArchiveEntry`): Entry to add

**Returns**: `True` if successful

##### `find_latest_archive_number()`

```python
def find_latest_archive_number(self) -> int
```

Find highest archive number.

**Returns**: Highest number or 0 if no archives

---

### ArchiveCompletedRequests

**File**: `domain/use_cases/archive_completed_requests.py`

Archives completed requests and updates main page using **batch mode**.

#### Batch Archiving

Unlike individual archiving, this use case:
- Collects ALL archivable requests first
- Adds ALL entries to the archive page entity
- Saves the archive page **ONCE** with all entries
- Updates the main page **ONCE** to remove all archived templates

**Benefits**:
- Reduces API calls from N+1 to 2
- Avoids triggering bot restrictions
- 50x faster for 50 requests

#### Constructor

```python
ArchiveCompletedRequests(wiki_repository: WikiRepository)
```

#### Methods

##### `execute()`

```python
def execute(
    self,
    requests: List[PhotoRequest],
    archive_page: ArchivePage
) -> dict
```

Execute batch archiving process.

**Parameters**:
- `requests` (`List[PhotoRequest]`): Requests to archive
- `archive_page` (`ArchivePage`): Archive page to use

**Returns**: Results dictionary:
```python
{
    'archived': List[str],  # Successfully archived page names
    'failed': List[str],    # Failed page names (all fail if save fails)
    'skipped': List[str]    # Skipped page names (not ready)
}
```

**Example**:
```python
# Archive 56 requests in 2 edits instead of 57
results = archive_use_case.execute(56_requests, archive_page)
# Results: {'archived': 56, 'failed': 0, 'skipped': 3}
```

---

## Controller

### PhotoLabController

**File**: `presentation/controllers/photo_lab_controller.py`

Orchestrates the entire workflow.

#### Constructor

```python
PhotoLabController(wiki_repository: WikiRepository)
```

#### Methods

##### `run()`

```python
def run(self) -> dict
```

Run complete workflow in production mode.

**Returns**: Results dictionary:
```python
{
    'success': bool,
    'total_requests': int,
    'archivable_requests': int,
    'archived': List[str],
    'failed': List[str],
    'skipped': List[str],
    'archive_page_number': int,
    'errors': List[str]
}
```

**Example**:
```python
controller = PhotoLabController(wiki_repo)
results = controller.run()
if results['success']:
    print(f"Archived {len(results['archived'])} requests")
```

##### `run_dry_mode()`

```python
def run_dry_mode(self) -> dict
```

Run workflow without making changes.

**Returns**: Results showing what would be archived

---

## Constants

### Page Titles

| Constant | Value | Description |
|----------|-------|-------------|
| `MAIN_PAGE_TITLE` | `"ويكيبيديا:ورشة الصور/طلبات"` | Main requests page |
| `ARCHIVE_PREFIX` | `"ويكيبيديا:ورشة الصور/أرشيف"` | Archive page prefix |

### Template Names

| Constant | Value | Description |
|----------|-------|-------------|
| `REQUEST_TEMPLATE_NAME` | `"طلب ورشة صور"` | Request template |
| `PERSPECTIVE_TEMPLATE` | `"منظور"` | Completion indicator |

### Configuration

| Constant | Value | Description |
|----------|-------|-------------|
| `MAX_ENTRIES_PER_ARCHIVE` | `10` | Max entries per archive page |

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture overview
- [WORKFLOW.md](WORKFLOW.md) - Workflow details
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
