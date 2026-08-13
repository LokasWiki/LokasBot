# Archive Bot — PHP → Python Migration Plan

Migrate the legacy PHP **archivebot** (Peachy framework, archived at
https://github.com/LokasWiki/archivebot) into a Python task inside LokasBot:
`tasks/archive_bot/`, following the project's clean-architecture conventions
and running on pywikibot + Python 3.13.

The bot archives old discussion threads from **Arabic Wikipedia user talk pages**
(namespace 3) that transclude `{{أرشفة آلية}}` (Template:Auto archiving).

---

## 1. Source analysis (what the PHP bot does)

Two files contain the whole logic:

| PHP file | Python target |
|---|---|
| `script/MyScripts.php` | entry point + template scanning |
| `script/Lib2.php` | `splitintosections()` + `doarchive()` core |

### `MyScripts.php` flow
1. `embeddedin("قالب:أرشفة آلية", 3, null)` → list user-talk pages (namespace 3)
   that transclude the template.
2. Skip pages whose title contains `/` (subpages).
3. Skip pages with sysop-level `edit` protection.
4. For each page: `readtemp($page, $name)`:
   - parse `{{أرشفة آلية|...}}` params,
   - if mode is `قسم` (by age) → `age = value * 24` hours,
   - else (by size) → archive only when `page_length >= value * 1000` bytes,
   - call `doarchive(...)`.
5. `sleep(3)` between pages.

### `Lib2.php` — `doarchive()` core
1. Get latest revision + its text.
2. Split text into level-2 sections (`splitintosections`).
3. Walk history backward until a revision older than `age` hours is found;
   that revision's text is the "old" snapshot.
4. Split old snapshot into sections; drop old sections no longer present.
5. Classify each current section:
   - keep if it contains `{{لا للأرشفة}}` (do-not-archive),
   - keep if it is new (not in old snapshot),
   - archive if unchanged since the old snapshot (older than `age`),
   - keep if `minkeep` would be violated,
   - optional: enforce `maxsects` / `maxbytes`.
6. Build archive page name: `archiveprefix + " " + counter` (e.g.
   `نقاش المستخدم:لوقا/أرشيف 3`), using `prefixindex` to find the current max counter.
7. Archive page header default:
   ```
   {{تصفح أرشيف|N}}
   {{تمت الأرشفة}}
   {{أرشيف صفحة رئيسية}}
   ```
8. Save the archive page first (`أرشفة … من [[page]]`), then the main page
   (`أرشفة … إلى [[archive]]`); roll back the archive edit if the main-page edit fails.
9. Update the trailing counter inside the `{{أرشفة آلية|...}}` template on the main page.

### `{{أرشفة آلية}}` template contract (Arabic Wikipedia)

Invocation format:

```
{{أرشفة آلية|<type>|<value>|<archive_prefix>|<counter>}}
```

| Param | Meaning |
|---|---|
| `1` (`type`) | `قسم` = archive by age, or `حجم` = archive by size |
| `2` (`value`) | days (for `قسم`) or KB threshold (for `حجم`) |
| `3` (`archive_prefix`) | archive page name prefix, e.g. `نقاش المستخدم:لوقا/أرشيف` |
| `4` (`counter`) | current archive number (trailing digits); auto-updated by the bot |

- Optional legacy flag `|عددي` / `|عددى` is stripped before parsing.
- `{{لا للأرشفة}}` inside a section = do not archive that section.

---

## 2. Target architecture (clean architecture, matches existing tasks)

```
tasks/archive_bot/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── config_loader.py          # template name, edit summaries, headers, site
│   └── settings.json             # externalized config
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── archive_config.py     # parsed {{أرشفة آلية}} params
│   │   ├── section.py            # wiki section (header + content)
│   │   └── archive_result.py     # outcome of one page archiving
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── wiki_repository.py    # abstract interface (ABC)
│   └── use_cases/
│       ├── __init__.py
│       ├── parse_archive_config.py   # template parser use case
│       ├── split_sections.py         # wikitext → sections
│       ├── decide_archive.py         # classify keep vs archive
│       └── archive_page.py           # orchestrate the archiving
├── data/
│   ├── __init__.py
│   └── pywikibot_wiki_repository.py  # pywikibot implementation
├── presentation/
│   ├── __init__.py
│   └── wiki_operations.py        # wiring + site bootstrap
└── main.py                       # entry point (main + argparse)
```

Tests mirror this under `tests/tasks/archive_bot/`.

---

## 3. PHP → Python mapping (key pywikibot equivalents)

| PHP (Peachy) | Python (pywikibot) |
|---|---|
| `Peachy::newWiki("arwiki")` | `pywikibot.Site("ar", "wikipedia")` |
| `$MyWiki->embeddedin($tpl, 3, null)` | `pywikibot.Page(site, tpl).embeddedin(namespace=3)` |
| `$MyWiki->initPage($t)` | `pywikibot.Page(site, t)` |
| `$page->get_text()` | `page.text` |
| `$page->get_length()` | `len(page.text)` |
| `$page->history(2000,'older',...)` | `page.revisions(total=..., reverse=False)` |
| `$page->get_protection()` | `page.protection()` |
| `$page->edit($text, $summary, true)` | `page.text = ...; page.save(summary)` |
| `$MyWiki->prefixindex($prefix, 3, null)` | `site.allpages(prefix=..., namespace=3)` |

---

## 4. TODO checklist

### Phase A — Scaffolding
- [x] A1. Create `tasks/archive_bot/` package skeleton (`__init__.py` files, subpackages per §2).
- [x] A2. Add `tests/tasks/archive_bot/` skeleton with a first smoke test.

### Phase B — Pure domain logic (unit-testable, no network)
- [x] B1. `split_sections.py` — port `splitintosections()` to split wikitext into header + level-2 sections (handle `===`/`====` correctly, duplicate headers).
- [x] B2. `parse_archive_config.py` — parse `{{أرشفة آلية|...}}` (type/value/prefix/counter, strip `|عددي`), with validation and error reporting.
- [x] B3. `decide_archive.py` — port keep-vs-archive classification: `{{لا للأرشفة}}`, new-vs-unchanged, `minkeep`, `maxsects`/`maxbytes`, header transform.
- [x] B4. Entities: `ArchiveConfig`, `Section`, `ArchiveResult` dataclasses.

### Phase C — Infrastructure (pywikibot)
- [x] C1. `pywikibot_wiki_repository.py` implementing `WikiRepository` (embeddedin, text, length, revisions, protection, prefixindex, save).
- [x] C2. `wiki_operations.py` presentation wiring + site bootstrap + logging.

### Phase D — Orchestration
- [x] D1. `archive_page.py` use case — full `doarchive` flow: history walk, section diff, archive-page naming/counter, header injection, save order + rollback, counter update.
- [x] D2. `main.py` — scan namespace-3 pages, skip `/` subpages + sysop-protected, `sleep` throttle, `--dry-run` and `--page` flags, logging to file.

### Phase E — Tests
- [x] E1. Unit tests for B1–B3 with real Arabic wikitext fixtures (37 tests).
- [x] E2. Repository fake (in-memory) for D1 use-case tests (no network).
- [ ] E3. Integration smoke test: `--page` + `--dry-run` against a sandbox page.

### Phase F — Configuration & docs
- [x] F1. `config_loader.py` + `settings.json` (template name, summaries, header templates, site, throttle, limits).
- [x] F2. `README.md` for the task (usage, config, how it maps to the old PHP bot).

### Phase G — Toolforge deployment (after local validation)
- [ ] G1. `toolforge/jobs/archive_bot.sh` wrapper.
- [ ] G2. Add cronjob entry (cronjobs YAML) with `python3.13` image.
- [ ] G3. Switch the live job from the PHP tool to this Python task.

---

## 5. Migration notes / gotchas

- **Use pywikibot's battle-tested algorithm** (`scripts/archivebot.py` upstream,
  see `/tmp/archivebot_pywiki_reference.py`) as the reference; the PHP `doarchive`
  is itself an old port of it. Prefer the correct behavior over replicating PHP quirks.
- **`embeddedin` namespace is 3** (User talk) — keep that default, but make it
  configurable so other talk namespaces can be added later.
- **Archive page naming** uses a space + counter: `<prefix> <N>` (not a subpage `/N`).
- **Save order matters**: write archive page first, then main page; on failure of
  the second save, restore the archive page (the PHP bot does this).
- **Counter update**: rewrite the trailing number inside the template via regex,
  matching the old behavior.
- **Don't break anything**: the new task is additive (`tasks/archive_bot/`) and
  does not touch existing tasks; keep dependencies unchanged.
