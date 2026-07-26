# Wiki Localization Stage

This stage processes Arabic Wikipedia templates to localize English wiki links and template names to their Arabic equivalents.

## Purpose

- **Wiki Link Localization**: Converts `[[English Page]]` to `[[Arabic Page]]` when Arabic equivalent exists
- **Template Localization**: Converts template names like `{{Infobox}}` to Arabic equivalents like `{{صندوق}}`
- **Fallback Handling**: Uses `{{واو}}` template for English links that don't have Arabic equivalents
- **Interlanguage Link Support**: Uses Wikipedia API to find Arabic versions via langlinks

## Features

✅ **Wiki Link Processing**: Extract and replace `[[link|text]]` patterns
✅ **Template Processing**: Extract and replace `{{template|params}}` patterns
✅ **Arabic Wikipedia API**: Check page existence on Arabic Wikipedia
✅ **Interlanguage Retrieval**: Get Arabic equivalents from English wiki langlinks
✅ **واو Template Fallback**: Automatically insert `{{واو}}` for untranslated links
✅ **Error Handling**: Comprehensive error reporting and logging

## Usage

```python
from wikilocalize import localize_arabic_content

# Process Arabic content with English links
result = localize_arabic_content(arabic_template_text)
print(f"Replaced {result.original_links_replaced} links")
print(f"Inserted {result.waou_templates_inserted} واو templates")
```

## Pipeline Integration

This stage sits between **construct** (template building) and **publish** (publish to Wikipedia):

1. **Construct** builds Arabic template from translated data
2. **WikiLocalize** processes links/templates to Arabic equivalents
3. **Publish** sends the localized template to Arabic Wikipedia

## API Integration

- Uses Arabic Wikipedia REST API for existence checking
- Uses English Wikipedia Action API for langlink retrieval
- Handles API errors gracefully with fallback behavior
- Caches results to minimize API calls