# Photo Lab - Architecture Documentation

## Overview

The Photo Lab task follows **Clean Architecture** principles, separating concerns into distinct layers: Domain, Infrastructure, and Presentation. This design ensures:

- **Testability**: Business logic is independent of external frameworks
- **Maintainability**: Changes to one layer don't affect others
- **Flexibility**: Easy to swap implementations (e.g., different wiki libraries)
- **Efficiency**: Batch operations minimize API calls
- **Robustness**: Handles bot restrictions and edge cases gracefully

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │            PhotoLabController                     │  │
│  │  - Orchestrates use cases                         │  │
│  │  - Handles workflow execution                     │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                      Domain Layer                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │                    Entities                        │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │PhotoRequest │  │ArchiveEntry │  │ArchivePage│  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │                  Use Cases                         │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐│  │
│  │  │Extract   │ │Check     │ │Manage    │ │Archive ││  │
│  │  │Pending   │ │Request   │ │Archives  │ │Complete││  │
│  │  │Requests  │ │Status    │ │          │ │Requests││  │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘│  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │               Repository Interface                 │  │
│  │           WikiRepository (Abstract)                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │              PywikibotWiki                        │  │
│  │  - Concrete implementation of WikiRepository      │  │
│  │  - Uses pywikibot for wiki operations             │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Domain Layer

### Entities

Entities are the core business objects that encapsulate the domain logic.

#### PhotoRequest

Represents a photo workshop request.

**Location**: `domain/entities/photo_request.py`

**Attributes**:
- `page_name`: The article page name being requested
- `template_text`: The full template text from the main page
- `has_perspective`: Boolean indicating if request has perspective template
- `request_page_title`: Full title of the request page (auto-generated)

**Key Methods**:
- `mark_as_archivable()`: Mark request as ready for archiving
- `is_ready_for_archive()`: Check if request can be archived

#### ArchiveEntry

Represents an archived request entry.

**Location**: `domain/entities/archive_entry.py`

**Attributes**:
- `page_name`: The page name that was requested
- `template_text`: The template text being archived
- `archived_at`: Timestamp of archiving
- `archive_page_number`: Which archive page this entry belongs to

#### ArchivePage

Represents an archive page that holds multiple entries.

**Attributes**:
- `page_number`: The archive page number
- `entries`: List of ArchiveEntry objects
- `base_prefix`: Prefix for archive page titles

**Key Methods**:
- `is_full(max_entries=10)`: Check if archive has reached capacity
- `add_entry(entry)`: Add an entry to the archive
- `get_content()`: Generate full page content with header and entries

### Use Cases

Use cases encapsulate the application business rules.

#### ExtractPendingRequests

**Purpose**: Extract all photo requests from the main page.

**Location**: `domain/use_cases/extract_pending_requests.py`

**Process**:
1. Read the main requests page content
2. Parse wikitext using `wikitextparser`
3. Find all `طلب ورشة صور` templates
4. Extract page name from the first (unnamed) argument
5. Create PhotoRequest entities

#### CheckRequestStatus

**Purpose**: Check which requests have the `منظور` template.

**Location**: `domain/use_cases/check_request_status.py`

**Process**:
1. For each PhotoRequest, check its request page
2. Look for `منظور` template
3. Mark requests that have it as archivable

#### ManageArchives

**Purpose**: Manage archive pages (find latest, create new, check capacity).

**Location**: `domain/use_cases/manage_archives.py`

**Process**:
1. Get all archive pages with prefix `ويكيبيديا:ورشة الصور/أرشيف`
2. Find the highest numbered archive
3. Check if it has room (less than 10 entries)
4. If full, create new archive with next number
5. Return ArchivePage entity for use

#### ArchiveCompletedRequests

**Purpose**: Archive completed requests and update main page.

**Location**: `domain/use_cases/archive_completed_requests.py`

**Process**:
1. For each archivable request:
   - Add entry to archive page
   - Remove template from main page content
2. Save updated archive page
3. Save updated main page

## Repository Pattern

The Repository pattern abstracts data access, allowing the domain layer to remain independent of data storage details.

### WikiRepository Interface

**Location**: `domain/repositories/wiki_repository.py`

**Methods**:
- `get_main_requests_page_content()`: Get main page content
- `update_main_requests_page(content, summary)`: Update main page
- `has_template(page_title, template_name)`: Check for template
- `get_all_archive_pages(prefix)`: List all archives
- `create_archive_page(archive_page, summary)`: Create new archive
- `update_archive_page(archive_page, summary)`: Update existing archive
- `page_exists(page_title)`: Check page existence
- `count_templates_in_page(page_title, template_name)`: Count templates

### Implementation

**PywikibotWiki** implements `WikiRepository` using the pywikibot library.

**Location**: `infrastructure/wiki/pywikibot_wiki.py`

## Presentation Layer

### PhotoLabController

**Location**: `presentation/controllers/photo_lab_controller.py`

The controller orchestrates the entire workflow by coordinating use cases:

1. **Extract**: Get pending requests
2. **Check Status**: Identify which are ready
3. **Manage Archives**: Get/create appropriate archive
4. **Archive**: Move completed requests

**Methods**:
- `run()`: Execute full workflow in production
- `run_dry_mode()`: Execute workflow without making changes

## Dependency Flow

```
Presentation ──uses──► Use Cases ──use──► Entities
    │                       │
    │                       uses
    │                       ▼
    └─────────────► Repository Interface
                          ▲
                          │
                    implements
                          │
                    Infrastructure
```

## Data Flow

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   Main Page    │────▶│  Extract Use   │────▶│ PhotoRequest   │
│  (Wiki Page)   │     │     Case       │     │   Entities     │
└────────────────┘     └────────────────┘     └───────┬────────┘
                                                      │
                                                      ▼
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Request Pages  │────▶│   Check Use    │────▶│ Marked Ready   │
│  (Wiki Pages)  │     │     Case       │     │   for Archive  │
└────────────────┘     └────────────────┘     └───────┬────────┘
                                                      │
                                                      ▼
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Archive Pages  │◄────│  Manage Use    │◄────│ ArchivePage    │
│  (Wiki Pages)  │     │     Case       │     │   Entity       │
└────────────────┘     └────────────────┘     └────────────────┘
        ▲
        │
        │     ┌────────────────┐     ┌────────────────┐
        └─────│  Archive Use   │◄────│ ArchiveEntry   │
              │     Case       │     │   Entities     │
              └────────────────┘     └────────────────┘
```

## Design Principles

### Single Responsibility Principle

Each class has one reason to change:
- `PhotoRequest`: Represents a request
- `ExtractPendingRequests`: Extracts requests from page
- `PywikibotWiki`: Handles wiki operations
- `PhotoLabController`: Orchestrates workflow

### Dependency Inversion Principle

High-level modules depend on abstractions:
- Use cases depend on `WikiRepository` interface, not concrete implementation
- Easy to mock for testing
- Easy to swap implementations

### Open/Closed Principle

Open for extension, closed for modification:
- New use cases can be added without modifying existing ones
- New entity types can be added following the same patterns

## Extending the Architecture

### Adding a New Use Case

1. Create new file in `domain/use_cases/`
2. Inject `WikiRepository` in constructor
3. Implement `execute()` method
4. Add to controller if needed

### Adding a New Entity

1. Create new file in `domain/entities/`
2. Define attributes and business logic
3. Use dataclasses for simplicity
4. Add to `domain/__init__.py`

### Adding a New Repository Method

1. Add abstract method to `WikiRepository` interface
2. Implement in `PywikibotWiki`
3. Implement in `MockWikiRepository` for tests
4. Use in use cases

## See Also

- [WORKFLOW.md](WORKFLOW.md) - Detailed workflow explanation
- [API.md](API.md) - API reference for all classes
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guide for developers
