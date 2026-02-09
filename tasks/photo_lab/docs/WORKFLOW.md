# Photo Lab - Workflow Documentation

## Overview

This document describes the complete workflow of the Photo Lab task, from reading the wiki pages to archiving completed requests.

## High-Level Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         START                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Read Main Requests Page                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Page: ويكيبيديا:ورشة الصور/طلبات                         │   │
│  │  Action: Get wikitext content                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Parse and Extract Requests                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Find: {{طلب ورشة صور|page_name}} templates               │   │
│  │  Extract: page_name parameter                              │   │
│  │  Create: PhotoRequest entities                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Check Each Request Page                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  For each PhotoRequest:                                    │   │
│  │    - Build: ويكيبيديا:ورشة الصور/طلبات/{page_name}        │   │
│  │    - Check: Does it have {{منظور}} template?              │   │
│  │    - Mark: has_perspective = True if found                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Filter Ready Requests                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Filter: Requests where has_perspective == True            │   │
│  │  Result: List of archivable requests                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Any requests    │
                    │ ready to archive?│
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                              │
              ▼ NO                           ▼ YES
┌─────────────────────────┐      ┌──────────────────────────────────┐
│ Log: No requests ready  │      │ STEP 5: Get/Create Archive Page  │
│ Exit                    │      └──────────────┬───────────────────┘
└─────────────────────────┘                     │
                                                ▼
                              ┌───────────────────────────────────────┐
                              │  Find all pages with prefix:          │
                              │  ويكيبيديا:ورشة الصور/أرشيف          │
                              │  Get highest number                   │
                              └───────────────┬───────────────────────┘
                                              │
                                              ▼
                              ┌───────────────────────────────────────┐
                              │  Check: Entry count in archive        │
                              │  If >= 10: Create archive N+1         │
                              │  If < 10: Use existing archive N      │
                              └───────────────┬───────────────────────┘
                                              │
                                              ▼
                              ┌───────────────────────────────────────┐
                              │ STEP 6: Archive Each Request          │
                              │ ┌───────────────────────────────────┐ │
                              │ │ For each archivable request:      │ │
                              │ │   1. Create ArchiveEntry          │ │
                              │ │   2. Add to archive page          │ │
                              │ │   3. Remove from main page        │ │
                              │ └───────────────────────────────────┘ │
                              └───────────────┬───────────────────────┘
                                              │
                                              ▼
                              ┌───────────────────────────────────────┐
                              │ STEP 7: Save Changes                  │
                              │ ┌───────────────────────────────────┐ │
                              │ │   1. Save archive page            │ │
                              │ │   2. Save main requests page      │ │
                              │ └───────────────────────────────────┘ │
                              └───────────────┬───────────────────────┘
                                              │
                                              ▼
                              ┌───────────────────────────────────────┐
                              │ Log results and exit                  │
                              └───────────────────────────────────────┘
```

## Detailed Step-by-Step Process

### Step 1: Read Main Requests Page

**File**: [`extract_pending_requests.py`](tasks/photo_lab/domain/use_cases/extract_pending_requests.py)

**Wiki Page**: `ويكيبيديا:ورشة الصور/طلبات`

**Example Content**:
```wikitext
== طلبات جديدة ==

{{طلب ورشة صور|تعريب مخطط قدود الميغالودون وصورة المقارنة بين الكواكب والنجوم}}

{{طلب ورشة صور|نهر النيل}}

{{طلب ورشة صور|هرم خوفو}}

== طلبات قديمة ==

{{طلب ورشة صور|أهرامات الجيزة}}
```

**Process**:
1. Use `pywikibot.Page` to get the page
2. Extract the `text` property
3. Return wikitext content

### Step 2: Parse and Extract Requests

**File**: [`extract_pending_requests.py`](tasks/photo_lab/domain/use_cases/extract_pending_requests.py)

**Parsing Method**:
```python
import wikitextparser as wtp

parsed = wtp.parse(content)

for template in parsed.templates:
    if template.name.strip() == "طلب ورشة صور":
        # Extract first argument (page name)
        page_name = template.arguments[0].value.strip()
        template_text = template.string
        # Create PhotoRequest entity
```

**Extraction Logic**:
- Template name must be exactly `طلب ورشة صور`
- Page name is the first unnamed argument
- Full template text is preserved for archiving

**Example Extraction**:
```
Input:  {{طلب ورشة صور|تعريب مخطط قدود الميغالودون وصورة المقارنة بين الكواكب والنجوم}}
Output: PhotoRequest(
            page_name="تعريب مخطط قدود الميغالودون وصورة المقارنة بين الكواكب والنجوم",
            template_text="{{طلب ورشة صور|تعريب مخطط قدود الميغالودون وصورة المقارنة بين الكواكب والنجوم}}"
        )
```

### Step 3: Check Request Status

**File**: [`check_request_status.py`](tasks/photo_lab/domain/use_cases/check_request_status.py)

**For Each PhotoRequest**:

1. **Build Request Page Title**:
   ```python
   request_page_title = f"ويكيبيديا:ورشة الصور/طلبات/{photo_request.page_name}"
   ```
   Example: `ويكيبيديا:ورشة الصور/طلبات/نهر النيل`

2. **Check for Perspective Template**:
   ```python
   has_perspective = wiki_repository.has_template(
       request_page_title,
       "منظور"
   )
   ```

3. **Mark Status**:
   - If `منظور` found: `photo_request.has_perspective = True`
   - If not found: `photo_request.has_perspective = False`

**Example Request Page**:
```wikitext
== تفاصيل الطلب ==

أحتاج صورة لنهر النيل في أسوان

== الصور المرفقة ==

{{منظور}}
[[ملف:Nile_River.jpg|تصغير|نهر النيل]]

== التعليقات ==

تم إرفاق الصورة بواسطة المستخدم:فلان
```

This page **HAS** the `منظور` template → Ready for archiving

### Step 4: Filter Archivable Requests

**Logic**:
```python
archivable_requests = [
    r for r in all_requests
    if r.has_perspective
]
```

**Example**:
```
All Requests:
1. تعريب مخطط قدود الميغالودون... - has_perspective: True ✓
2. نهر النيل - has_perspective: False ✗
3. هرم خوفو - has_perspective: True ✓
4. أهرامات الجيزة - has_perspective: False ✗

Archivable: [1, 3]
```

### Step 5: Get or Create Archive Page

**File**: [`manage_archives.py`](tasks/photo_lab/domain/use_cases/manage_archives.py)

**Find Existing Archives**:
```python
archive_pages = wiki_repository.get_all_archive_pages(
    "ويكيبيديا:ورشة الصور/أرشيف"
)
# Returns: [(1, "ويكيبيديا:ورشة الصور/أرشيف 1"), (2, "...")]
```

**Check Archive with Bot Restriction Handling**:
```python
# Find first usable archive (not full, not bot-restricted)
current_number = latest_number
while True:
    current_title = f"{base_prefix} {current_number}"
    
    if page_exists(current_title):
        # Check bot restrictions
        if has_template(current_title, "bots") or has_template(current_title, "nobots"):
            current_number += 1  # Skip restricted
            continue
        
        # Check capacity
        entry_count = count_templates_in_page(current_title, "طلب ورشة صور")
        if entry_count >= 10:
            current_number += 1  # Skip full
            continue
        
        # Use this archive
        return load_archive_page(current_number)
    else:
        # Create new archive
        return ArchivePage(page_number=current_number)
```

**Archive Selection Example**:
```
Archive 52: 10 entries (FULL) → Skip
Archive 53: {{bots}} restriction → Skip
Archive 54: Doesn't exist → CREATE & USE
```

**Archive Page Naming**:
- First archive: `ويكيبيديا:ورشة الصور/أرشيف 1`
- Second archive: `ويكيبيديا:ورشة الصور/أرشيف 2`
- And so on...

### Step 6: Archive Requests (Batch Mode)

**File**: [`archive_completed_requests.py`](tasks/photo_lab/domain/use_cases/archive_completed_requests.py)

**All Archivable Requests in ONE Operation**:

1. **Collect ALL Entries First**:
   ```python
   for request in archivable_requests:
       entry = ArchiveEntry(
           page_name=request.page_name,
           template_text=request.template_text
       )
       archive_page.add_entry(entry)
   ```

2. **Save Archive Page ONCE**:
   ```python
   # Single edit with all entries
   wiki_repository.update_archive_page(
       archive_page,
       summary="أرشفة 56 طلبات ورشة صور"
   )
   ```

3. **Remove All from Main Page**:
   ```python
   # Remove all templates in one operation
   updated_content = main_content
   for request in archivable_requests:
       updated_content = updated_content.replace(request.template_text, "")
   ```

**Why Batch Mode?**
- Reduces API calls from N+1 to 2
- Avoids triggering bot restrictions
- Much faster execution (56x faster for 56 requests)

### Step 7: Save Changes (2 Edits Total)

**Save Archive Page**:
```python
# Single edit with all entries
wiki_repository.update_archive_page(
    archive_page,
    summary="أرشفة طلبات ورشة صور"
)
```

**Save Main Page**:
```python
wiki_repository.update_main_requests_page(
    updated_content,
    summary="أرشفة طلبات منجزة"
)
```

## Archive Page Format

### Header

Every archive page starts with these templates:

```wikitext
{{تصفح أرشيف|42}}
{{تمت الأرشفة}}
```

Where `42` is the archive page number.

### Entries

After the header, each archived request is added:

```wikitext
{{طلب ورشة صور|تعريب مخطط قدود الميغالودون وصورة المقارنة بين الكواكب والنجوم}}

{{طلب ورشة صور|هرم خوفو}}
```

### Full Example

```wikitext
={{تصفح أرشيف|1}}
{{تمت الأرشفة}}

{{طلب ورشة صور|تعريب مخطط قدود الميغالودون وصورة المقارنة بين الكواكب والنجوم}}

{{طلب ورشة صور|هرم خوفو}}

{{طلب ورشة صور|مسجد الأقصى}}
```

## Error Handling

### Missing Pages

If a request page doesn't exist:
- Log warning
- Skip the request
- Continue with other requests

### Wiki API Errors

If wiki operations fail:
- Log error
- Mark request as failed
- Continue with other requests
- Report failures in final results

### Partial Failures

If some requests archive but others fail:
- Successfully archived requests remain archived
- Failed requests stay on main page
- Report partial success

## Logging

The workflow produces detailed logs:

```
INFO: Extracting requests from ويكيبيديا:ورشة الصور/طلبات
INFO: Found 5 pending requests
INFO: Found 2 requests ready for archiving
INFO: Using archive page: ويكيبيديا:ورشة الصور/أرشيف 3
INFO: Archived: 2 requests
INFO: Failed: 0 requests
```

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture overview
- [API.md](API.md) - API reference
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
