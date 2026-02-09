# Photo Lab Task

## Overview

The Photo Lab Task (`photo_lab`) is a Python automation bot designed for Arabic Wikipedia that archives completed photo workshop requests. It automates the process of identifying requests that have received perspective images and moving them from the active requests page to archive pages.

## What Problem Does It Solve?

On Arabic Wikipedia, the Photo Workshop (ورشة الصور) is a page where users can request images for articles. When a request is fulfilled (indicated by the presence of a `منظور` template on the request page), it should be archived to keep the main requests page clean and manageable.

**Manual Process (Before this bot):**
- Volunteers had to manually check each request page
- Manually copy completed requests to archive pages
- Remove completed requests from the main page
- Keep track of which archive page to use (max 10 entries per page)
- Handle bot-restricted pages manually

**Automated Process (With this bot):**
- Automatically scans the main requests page
- Checks each request page for the completion template
- **Batch archives** all completed requests in **ONE edit** (efficient!)
- Automatically finds the appropriate archive page (handles full and bot-restricted pages)
- Removes archived requests from the main page in **ONE edit**

## Key Features

| Feature | Description |
|---------|-------------|
| **Batch Archiving** | Archives all ready requests in a single edit to minimize API calls |
| **Bot Restriction Handling** | Automatically skips bot-restricted archives (`{{bots}}`, `{{nobots}}`) |
| **Smart Archive Selection** | Finds the first available archive (skips full/restricted ones) |
| **Archive Auto-Creation** | Creates new archives automatically when needed |

## Quick Start

### Prerequisites

- Python 3.10+
- pywikibot
- wikitextparser
- Access to Arabic Wikipedia (ar.wikipedia.org)

### Installation

```bash
# Install dependencies
pip install pywikibot wikitextparser

# Configure pywikibot (if not already configured)
# See: https://www.mediawiki.org/wiki/Manual:Pywikibot/
```

### Usage

```bash
# Run in production mode
python -m tasks.photo_lab.main

# Run in dry mode (test without making changes)
python -m tasks.photo_lab.main --dry-run

# Run with verbose logging
python -m tasks.photo_lab.main --verbose
```

## Directory Structure

```
tasks/photo_lab/
├── __init__.py              # Package initialization
├── main.py                  # Entry point
├── domain/                  # Domain layer (business logic)
│   ├── entities/            # Business entities
│   │   ├── photo_request.py
│   │   └── archive_entry.py
│   ├── repositories/        # Repository interfaces
│   │   └── wiki_repository.py
│   └── use_cases/           # Use cases
│       ├── extract_pending_requests.py
│       ├── check_request_status.py
│       ├── manage_archives.py
│       └── archive_completed_requests.py
├── infrastructure/          # Infrastructure layer
│   └── wiki/
│       └── pywikibot_wiki.py
├── presentation/            # Presentation layer
│   └── controllers/
│       └── photo_lab_controller.py
├── tests/                   # Unit tests
│   ├── mock_wiki_repository.py
│   ├── test_photo_request.py
│   ├── test_archive_entry.py
│   └── test_use_cases.py
└── docs/                    # Documentation
    ├── README.md            # This file
    ├── ARCHITECTURE.md      # Architecture overview
    ├── WORKFLOW.md          # Workflow details
    ├── API.md               # API reference
    ├── DEVELOPMENT.md       # Development guide
    └── TESTING.md           # Testing guide
```

## Wiki Pages Involved

| Page | Purpose | Action |
|------|---------|--------|
| `ويكيبيديا:ورشة الصور/طلبات` | Main requests page | Read, remove completed templates |
| `ويكيبيديا:ورشة الصور/طلبات/{page_name}` | Individual request pages | Check for `منظور` template |
| `ويكيبيديا:ورشة الصور/أرشيف N` | Archive pages | Create or update with completed requests |

## Configuration

### Constants

The task uses the following constants defined in the code:

- **Main Page**: `ويكيبيديا:ورشة الصور/طلبات`
- **Request Template**: `طلب ورشة صور`
- **Completion Template**: `منظور`
- **Archive Prefix**: `ويكيبيديا:ورشة الصور/أرشيف`
- **Max Entries per Archive**: 10

### Archive Header Format

```wikitext
{{تصفح أرشيف|N}}
{{تمت الأرشفة}}
```

Where `N` is the archive page number.

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for architecture details
- Read [WORKFLOW.md](WORKFLOW.md) for workflow explanation
- Read [API.md](API.md) for API reference
- Read [DEVELOPMENT.md](DEVELOPMENT.md) to extend the task
- Read [TESTING.md](TESTING.md) for testing information

## License

This project is part of the LokasBot system. See the main project LICENSE file.
