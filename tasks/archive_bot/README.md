# Archive Bot (tasks/archive_bot)

أرشفة آلية لنقاشات صفحات نقاش المستخدمين في ويكيبيديا العربية.

A Python migration of the legacy PHP **archivebot** (Peachy framework,
archived at https://github.com/LokasWiki/archivebot). The bot archives old
discussion threads from Arabic Wikipedia **user talk pages** (namespace 3)
that transclude `{{أرشفة آلية}}`.

## How it works

1. Finds every user-talk page that transcludes `{{أرشفة آلية}}`.
2. Skips subpages (titles containing `/`) and sysop-protected pages.
3. Parses the template parameters with `wikitextparser`:

   ```
   {{أرشفة آلية|<type>|<value>|<archive_prefix_with_counter>}}
   ```

   | Param | Meaning |
   |---|---|
   | `قسم` | archive by age — `value` = days |
   | `حجم` | archive by size — `value` = kilobytes |
   | prefix | e.g. `نقاش المستخدم:Example/أرشيف 6` (trailing digits = counter) |

4. Splits the page into level-2 sections and compares them against a
   snapshot from `age` hours/days ago.
5. Moves sections whose content is unchanged (i.e. had no activity for the
   threshold) to the archive page `<prefix> <counter>`.
6. Keeps sections marked `{{لا للأرشفة}}` and new/edited sections.
7. Writes the archive page first, then the talk page; on failure of the
   second write it rolls back the archive edit.
8. Updates the archive counter inside the template.

## Usage

```bash
# Preview without saving
uv run python -m tasks.archive_bot.main --dry-run

# Archive a single page (dry run)
uv run python -m tasks.archive_bot.main --page "نقاش المستخدم:Example" --dry-run

# Archive a single page for real
uv run python -m tasks.archive_bot.main --page "نقاش المستخدم:Example"

# Full run across all transcluding pages
uv run python -m tasks.archive_bot.main
```

Options: `--dry-run`, `--page`, `--namespace`, `--limit`, `--sleep`.

## Configuration

Defaults live in `config/config_loader.py`; override via
`config/settings.json` (same keys as `ArchiveBotConfig`). Notable values:

- `template_name` / `template_title` — the `{{أرشفة آلية}}` template.
- `namespace` — namespace to scan (3 = User talk).
- `max_archive_size` — archive page byte size above which a new archive is
  started (default `100000`).
- `max_history` — max revisions to walk when locating the age snapshot.

## Architecture

```
tasks/archive_bot/
├── config/            # ArchiveBotConfig + settings.json loader
├── domain/
│   ├── entities/      # ArchiveConfig, Section, ArchiveResult
│   ├── repositories/  # WikiRepository (abstract interface)
│   └── use_cases/     # split_sections, parse_archive_config,
│                      # decide_archive, archive_page
├── data/              # PywikibotWikiRepository (pywikibot implementation)
└── main.py            # entry point
```

Tests live in `tests/tasks/archive_bot/`:

```bash
uv run python -m unittest tests/tasks/archive_bot/test_*.py
```
