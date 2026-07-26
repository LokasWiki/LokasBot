# InfoboxSync Pipeline

A sophisticated Wikipedia infobox synchronization pipeline using advanced design patterns and pywikibot integration.

## Overview

This pipeline fetches Arabic Wikipedia pages, finds their corresponding English pages, extracts infobox data, and processes it through multiple stages for synchronization purposes.

## Architecture & Design Patterns

### 1. **Template Method Pattern**
- Used in `WikipediaFetcher` abstract base class
- Defines the skeleton of the page fetching algorithm
- Allows subclasses to customize specific steps

### 2. **Observer Pattern**
- `FetchObserver` interface for monitoring fetch operations
- `LoggingFetchObserver` implementation for logging
- Allows multiple observers to monitor the same fetch operation

### 3. **Strategy Pattern**
- `WikipediaSyncFetcher` uses different fetch strategies
- Separate fetchers for Arabic and English Wikipedia
- Easy to extend with new language-specific strategies

### 4. **Factory Pattern**
- Creation of appropriate fetchers based on site/language
- Centralized fetcher creation in `WikipediaSyncFetcher`

### 5. **Data Class Pattern**
- `PageInfo` dataclass for structured page information
- Clean data transfer between pipeline stages

### 6. **Strategy Pattern (Parse Stage)**
- `InfoboxParser` abstract base class for different template parsers
- `FootballBiographyParser` for football biography templates
- `GenericInfoboxParser` for other template types
- `InfoboxParserFactory` creates appropriate parsers based on template type
- Allows pipeline to specify which template parser to use

### 7. **Strategy Pattern (Map Stage)**
- `FieldMapper` abstract base class for different field type mappers
- `TextFieldMapper`, `NumberFieldMapper`, `ImageFieldMapper`, `LinkFieldMapper`, `MixedFieldMapper` implementations
- `NumberedFieldMapper` for handling numbered sequences (years1, clubs1, caps1, etc.)
- `TemplateMapper` abstract base class for template-specific field mapping
- `FootballBiographyMapper` with English to Arabic field mappings
- `TemplateMapperFactory` and `FieldMapperFactory` for creating appropriate mappers
- Supports field type validation and numbered field grouping

### 8. **Strategy Pattern (Translate Stage)**
- `TranslationService` abstract base class for different translation services
- `GeminiTranslator` implementation using Google Gemini AI via LiteLLM
- `TranslationServiceFactory` for creating appropriate translation services
- Template-based prompt system with external prompt files
- Single-request translation for optimal efficiency
- Supports field-by-field and template-level translation strategies

### 9. **Strategy Pattern (Construct Stage)**
- `TemplateBuilder` abstract base class for different template builders
- `ArabicTemplateBuilder` implementation for Arabic Wikipedia templates
- `TemplateBuilderFactory` for creating appropriate builders
- Smart field formatting for different data types
- Template validation and quality estimation
- Support for multiple Arabic Wikipedia template types

## Pipeline Stages

1. **Fetch**: Uses pywikibot to check Arabic page existence and find English equivalent
2. **Parse**: Extracts infobox data from Wikipedia wikitext using wikitextparser and Strategy Pattern
3. **Map**: Maps English field names to Arabic equivalents using Strategy Pattern with field type validation
4. **Translate**: Translates English infobox data to Arabic using Google Gemini AI with single-request optimization
5. **Construct**: Constructs Arabic Wikipedia templates from translated data using Strategy Pattern
6. **Publish**: Publishes the Arabic template directly to Arabic Wikipedia using pywikibot
7. **Save**: Saves processed data as JSON files

## Usage

### Basic Usage

```python
from tasks.InfoboxSync.test import run_wikipedia_pipeline

# Sync an Arabic Wikipedia page
result_path = run_wikipedia_pipeline("مصر")  # Egypt in Arabic
print(f"Data saved to: {result_path}")
```

### Advanced Usage

```python
from tasks.InfoboxSync.fetch.fetch import fetch_wikipedia_data

# Direct access to fetch stage
wiki_data = fetch_wikipedia_data("محمد بن سلمان")
if wiki_data['sync_possible']:
    arabic_page = wiki_data['arabic']
    english_page = wiki_data['english']
    print(f"Arabic title: {arabic_page.title}")
    print(f"English title: {english_page.title}")
```

### Using Different Template Types

```python
from tasks.InfoboxSync.parse.parse import parse_data

# Parse football biography infobox
data = {'title': 'Player Name', 'content': wikitext_content}
football_data = parse_data(data, 'football_biography')

# Parse person infobox
person_data = parse_data(data, 'person')

# Parse custom template
custom_data = parse_data(data, 'infobox custom_template')
```

### Field Mapping with Different Types

```python
from tasks.InfoboxSync.map.field_mappers import TextFieldMapper, NumberFieldMapper

# Text field mapping
text_mapper = TextFieldMapper("name", "الاسم")
mapped = text_mapper.map_field("Lionel Messi")

# Number field mapping
number_mapper = NumberFieldMapper("height", "الطول")
mapped = number_mapper.map_field("1.70 m")

# Numbered field mapping (groups years1, years2, etc.)
from tasks.InfoboxSync.map.template_mapper import FootballBiographyMapper
mapper = FootballBiographyMapper()
mapped_data = mapper.map_infobox(infobox_data)
```

### Translation with AI

```python
from tasks.InfoboxSync.translate.translate import translate_data

# Translate mapped data to Arabic using Gemini AI
result = translate_data(mapped_data, target_lang='ar')

if result['translation_metadata']['success']:
    translated_fields = result['translated_fields']
    print(f"Translated {result['translation_metadata']['translated_fields']} fields")
else:
    print(f"Translation failed: {result['translation_metadata']['error']}")
```

### Template Building

```python
from tasks.InfoboxSync.construct.build import construct_arabic_template

# Construct Arabic Wikipedia template from translated data
result = construct_arabic_template(translated_data, template_type='football_biography')

if build_result.success:
    arabic_template = build_result.template_text
    print(f"Constructed template with {build_result.field_count} fields")
    print(arabic_template)
else:
    print(f"Construction failed: {build_result.errors}")
```

## Dependencies

- `pywikibot`: For Wikipedia API interactions
- `wikitextparser`: For advanced wikitext parsing
- `litellm`: For Google Gemini AI integration
- Install with: `pip install pywikibot wikitextparser litellm`

## Configuration

Before using, configure pywikibot:
```bash
pywikibot generate_user_files
```

Or set up your user configuration file as needed for your Wikipedia bot account.

For translation, set your Google AI API key:
```bash
export GEMINI_API_KEY="your-google-ai-api-key"
```

## Error Handling

The pipeline includes comprehensive error handling for:
- Missing Arabic pages
- Missing corresponding English pages
- Network/API errors
- Parsing errors
- Field mapping errors
- Translation service errors
- Template construction errors
- File I/O errors

## Data Flow

1. **Input**: Arabic page title
2. **Arabic Check**: Verify page exists on ar.wikipedia.org
3. **English Lookup**: Find corresponding English page via langlinks
4. **Content Fetch**: Retrieve English page content
5. **Parse**: Extract infobox data using wikitextparser and Strategy Pattern
6. **Map**: Map English fields to Arabic using Strategy Pattern with field type validation
7. **Translate**: Translate English infobox data to Arabic using Google Gemini AI with single-request optimization
9. **Construct**: Construct Arabic Wikipedia template from translated data
9. **Publish**: Publish the Arabic template directly to Arabic Wikipedia using pywikibot
10. **Save**: Store results as JSON

## Extension Points

### Adding New Languages
```python
class GermanFetcher(WikipediaFetcher):
    def get_site_name(self) -> str:
        return 'de'
```

### Custom Observers
```python
class MetricsObserver(FetchObserver):
    def on_page_check_complete(self, page_info: PageInfo):
        # Send metrics to monitoring system
        pass
```

### Adding New Template Parsers
```python
from tasks.InfoboxSync.parse.base_parser import InfoboxParser

class CustomTemplateParser(InfoboxParser):
    def __init__(self):
        super().__init__("infobox custom")

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        # Custom parsing logic here
        pass
```

### Adding New Field Mappers
```python
from tasks.InfoboxSync.map.field_mappers import FieldMapper

class CustomFieldMapper(FieldMapper):
    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "custom")

    def map_field(self, value: str) -> Dict[str, Any]:
        # Custom field mapping logic
        return {
            self.arabic_key: {
                "value": value,
                "type": "custom",
                "validation": {"is_valid": True}
            }
        }
```

### Adding New Translation Services
```python
from tasks.InfoboxSync.translate.base_translator import TranslationService

class CustomTranslator(TranslationService):
    def __init__(self, api_key: str):
        super().__init__('en', 'ar')
        self.api_key = api_key

    def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        # Custom translation logic
        pass

    def translate_text(self, text: str, **kwargs) -> TranslationResult:
        # Custom text translation
        pass

    def translate_field(self, field_name: str, field_value: Any, **kwargs) -> TranslationResult:
        # Custom field translation
        pass

    def is_available(self) -> bool:
        # Check service availability
        pass

    def get_service_name(self) -> str:
        return "Custom Translator"

# Register the service
from tasks.InfoboxSync.translate.base_translator import TranslationServiceFactory
TranslationServiceFactory.register_service("custom", CustomTranslator)
```

### Adding New Template Builders
```python
from tasks.InfoboxSync.construct.base_builder import TemplateBuilder

class CustomTemplateBuilder(TemplateBuilder):
    def __init__(self, template_type: str = 'custom'):
        super().__init__(template_type)

    def build_template(self, translated_data: Dict[str, Any], **kwargs) -> BuildResult:
        # Custom template building logic
        pass

    def format_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        # Custom field formatting
        pass

    def get_template_name(self) -> str:
        return 'صندوق مخصص'

    def is_available(self) -> bool:
        return True

    def get_builder_name(self) -> str:
        return "Custom Template Builder"

# Register the builder
from tasks.InfoboxSync.construct.base_builder import TemplateBuilderFactory
TemplateBuilderFactory.register_builder("custom_builder", CustomTemplateBuilder)
```

### Enhanced Parsing
The parse stage uses `wikitextparser` for more accurate infobox extraction compared to regex-based approaches.

## File Structure

```
tasks/InfoboxSync/
├── README.md                     # This documentation
├── test.py                      # Main pipeline orchestrator
├── demo_real_wikipedia.py       # Demo with real Wikipedia data
├── fetch/
│   ├── __init__.py
│   └── fetch.py                 # Fetch stage with design patterns
├── parse/
│   ├── __init__.py
│   ├── base_parser.py          # Abstract parser base class
│   ├── football_parser.py      # Football biography parser
│   ├── parser_factory.py       # Factory for creating parsers
│   └── parse.py                # Parse stage using Strategy Pattern
├── map/
│   ├── __init__.py
│   ├── field_mappers.py        # Field type strategy mappers
│   ├── template_mapper.py      # Template field mapping coordinators
│   └── map.py                  # Map stage using Strategy Pattern
├── translate/
│   ├── __init__.py
│   ├── base_translator.py      # Abstract translation service base class
│   ├── gemini_translator.py    # Google Gemini AI implementation
│   ├── config.py               # Translation configuration management
│   ├── prompt_template.txt     # External prompt template file
│   ├── translate.py            # Main translation interface
│   └── README.md               # Translation stage documentation
├── construct/
│   ├── __init__.py
│   ├── base_builder.py         # Abstract template builder base class
│   ├── arabic_builder.py       # Arabic Wikipedia template builder
│   ├── build.py                # Main construct stage interface
│   └── README.md               # Construct stage documentation
├── publish/
│   ├── __init__.py
│   └── publish.py               # Publish stage for Wikipedia publishing
└── save/
    ├── __init__.py
    └── save.py                 # Save stage for data persistence
```

## Logging

The pipeline uses Python's logging module with configurable levels. All stages include detailed logging for debugging and monitoring.

## Future Enhancements

- Support for additional translation services (OpenAI, DeepL, Microsoft Translator)
- Support for additional Wikipedia languages
- Database storage instead of JSON files
- Web interface for pipeline management
- Batch processing capabilities
- Additional template parser implementations
- Enhanced field type detection and validation
- Translation quality scoring and confidence metrics
- Additional Arabic Wikipedia template builders
- Template validation against Arabic Wikipedia standards
- Integration with Arabic Wikipedia bot frameworks

## Translation Features

### Single-Request Optimization
- Translates ALL fields in ONE API call instead of multiple requests
- Significant cost savings and performance improvement
- Maintains field relationships and context

### Template-Based Prompts
- Prompt text stored in external `prompt_template.txt` file
- Easy customization without touching Python code
- Placeholder replacement system (`{{FIELDS_TEXT}}`, `{{START_INDEX}}`)

### Smart Field Handling
- **Text Fields**: Naturally translated (names, descriptions)
- **Number Fields**: Preserved as-is (heights, statistics)
- **Link Fields**: Maintained with proper formatting
- **Numbered Fields**: Translated individually while maintaining sequence

### AI Integration
- Google Gemini AI via LiteLLM for high-quality translations
- Configurable models and parameters
- Environment variable configuration for API keys

## Construct Stage Features

### Arabic Template Construction
- Builds properly formatted Arabic Wikipedia templates
- Handles different field types (text, numbers, links, images, numbered arrays)
- Supports multiple template types with proper Arabic names
- Proper Arabic Wikipedia syntax and formatting

### Smart Field Formatting
- **Text Fields**: Properly escaped for wiki syntax
- **Number Fields**: Preserved with units and formatting
- **Link Fields**: Correct wiki link syntax
- **Image Fields**: Proper Arabic image syntax
- **Numbered Fields**: Expanded into sequential fields (الأندية1, الأندية2, etc.)

### Template Types Supported
- `football_biography` → `سيرة لاعب كرة قدم`
- `person` → `صندوق شخص`
- `biography` → `سيرة شخصية`
- `football_club` → `صندوق نادي كرة قدم`
- `country` → `صندوق دولة`
- And many more...

## Publish Stage Features

### Direct Wikipedia Publishing
- Publishes Arabic templates directly to Arabic Wikipedia using pywikibot
- Automated edit summaries in Arabic for transparency
- Revision tracking and metadata collection
- Comprehensive error handling for publish failures

### Template Validation
- Validates template content before publishing
- Checks for required fields and proper formatting
- Ensures compatibility with Arabic Wikipedia standards
- Prevents publishing of malformed templates

### Publishing Results
After publishing, detailed results are provided:
```python
{
  "success": true,
  "page_title": "بول أباسولو",
  "edit_summary": "تحديث قالب السيرة الذاتية باستخدام InfoboxSync - football_biography",
  "revision_id": 12345678,
  "metadata": {
    "template_length": 450,
    "site": "ar.wikipedia.org",
    "published_at": "2024-01-15T10:30:00Z"
  },
  "errors": []
}
```

### Safety Features
- Verifies page existence before publishing
- Requires proper pywikibot configuration
- Includes edit summaries for accountability
- Supports dry-run mode for testing (future enhancement)

## Field Mapping Examples

### Numbered Fields (Most Common in Football)
Wikipedia often uses numbered fields for career history:
```
years1 = 2002–2003 | clubs1 = Basconia | caps1 = 35 | goals1 = 5
years2 = 2003–2004 | clubs2 = Barakaldo | caps2 = 24 | goals2 = 1
```

Mapped to Arabic arrays:
```json
{
  "سنوات_اللعب": {
    "value": ["2002–2003", "2003–2004", ...],
    "type": "numbered",
    "count": 15
  },
  "الأندية": {
    "value": ["Basconia", "Barakaldo", ...],
    "type": "numbered",
    "count": 15
  }
}
```

### Field Type Validation
Each field type includes validation:
```json
{
  "الطول": {
    "value": 1.70,
    "type": "number",
    "validation": {
      "is_valid": true,
      "numeric_value": 1.7,
      "has_units": true
    }
  }
}
```

### Translation Results
After translation, fields include translated values:
```json
{
  "الاسم": {
    "value": "Paul Abasolo",
    "translated_value": "بول أباسولو",
    "translation_confidence": 0.9,
    "type": "text"
  },
  "الأندية": {
    "value": ["Club A", "Club B"],
    "translated_value": ["النادي أ", "النادي ب"],
    "translation_confidence": 0.9,
    "type": "numbered"
  }
}
```

### Construction Results
After construction, the template is ready for Arabic Wikipedia:
```python
{
  "template_text": "{{صندوق سيرة لاعب كرة قدم\n| الاسم = بول أباسولو\n| الطول = 1.84 م\n...}}",
  "template_type": "football_biography",
  "field_count": 8,
  "success": true,
  "metadata": {
    "template_name": "سيرة لاعب كرة قدم",
    "builder_name": "Arabic Football Biography Builder",
    "total_input_fields": 10
  },
  "errors": []
}