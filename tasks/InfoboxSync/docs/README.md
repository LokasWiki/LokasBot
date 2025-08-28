# InfoboxSync Pipeline Documentation

## Overview

The InfoboxSync pipeline is a sophisticated system for synchronizing Wikipedia infoboxes between English and Arabic Wikipedia sites. It employs advanced design patterns, AI translation, and direct Wikipedia integration to automate the creation and maintenance of Arabic Wikipedia infobox templates.

## Pipeline Architecture

The pipeline consists of eight distinct stages, each handling a specific aspect of the infobox synchronization process:

```
1. Fetch       → Retrieve English and Arabic Wikipedia pages
2. Parse       → Extract infobox data from wikitext
3. Map         → Transform fields to Arabic field names
4. Translate   → Translate content using AI services
5. Construct   → Build Arabic Wikipedia templates
6. Localize    → Convert to Arabic Wikipedia format
7. Publish     → Upload to Arabic Wikipedia
8. Save        → Persist results for analysis
```

## Design Patterns Used

### Core Patterns
- **Strategy Pattern**: Translation services, infobox parsers, field mappers, template builders
- **Factory Pattern**: Creation of translators, parsers, mappers, and builders
- **Observer Pattern**: Fetch operations monitoring
- **Template Method Pattern**: Wikipedia operations workflow
- **Builder Pattern**: Template construction
- **Composite Pattern**: Numbered field grouping

### Benefits
- **Extensibility**: Easy addition of new translation services or parsers
- **Maintainability**: Clean separation of concerns
- **Testability**: Individual components can be tested independently
- **Flexibility**: Components can be swapped without affecting others

## Stage Documentation

### [1. Fetch Stage](fetch_stage.md)
- **Purpose**: Retrieve Wikipedia page data from both English and Arabic sites
- **Technology**: pywikibot integration with observer pattern
- **Key Features**: Cross-language page linking, existence verification
- **Output**: PageInfo objects with content and metadata

### [2. Parse Stage](parse_stage.md)
- **Purpose**: Extract structured data from raw wikitext
- **Technology**: wikitextparser with Strategy Pattern
- **Key Features**: Template-specific parsers, category/link extraction
- **Output**: Structured infobox data, categories, internal links

### [3. Map Stage](map_stage.md)
- **Purpose**: Transform English fields to Arabic equivalents
- **Technology**: Multi-layered Strategy Pattern with field type handlers
- **Key Features**: Numbered field grouping, validation, type-specific formatting
- **Output**: Arabic field names with validation metadata

### [4. Translate Stage](translate_stage.md)
- **Purpose**: Translate English content to Arabic using AI
- **Technology**: Google Gemini AI via LiteLLM with prompt engineering
- **Key Features**: Single-request optimization, content-type intelligence
- **Output**: Translated data with confidence scores

### [5. Construct Stage](construct_stage.md)
- **Purpose**: Build properly formatted Arabic Wikipedia templates
- **Technology**: Builder Pattern with template type strategies
- **Key Features**: Field type formatting, template name mapping, unicode support
- **Output**: Valid MediaWiki template syntax

### [6. Wiki Localization Stage](wiki_localization_stage.md)
- **Purpose**: Convert English wiki markup to Arabic equivalents
- **Technology**: Wiki API integration with error resilience
- **Key Features**: Link localization, "واو" template system, fallback mechanisms
- **Output**: Fully localized Arabic Wikipedia content

### [7. Publish Stage](publish_stage.md)
- **Purpose**: Upload templates directly to Arabic Wikipedia
- **Technology**: pywikibot with smart template replacement
- **Key Features**: Revision tracking, edit summaries, validation
- **Output**: Published templates with revision metadata

### [8. Save Stage](save_stage.md)
- **Purpose**: Persist pipeline results for future use
- **Technology**: JSON serialization with unicode support
- **Key Features**: Intelligent file naming, complete data preservation
- **Output**: Structured JSON files with full pipeline history

## Key Technologies

### AI and Translation
- **Google Gemini AI**: Advanced AI translation with content-type awareness
- **LiteLLM**: Unified interface for multiple AI providers
- **Single-Request Optimization**: Cost-effective batch translation

### Wikipedia Integration
- **pywikibot**: Official MediaWiki bot framework
- **wikitextparser**: Advanced wikitext parsing and manipulation
- **Arabic Wikipedia API**: Direct integration with ar.wikipedia.org

### Design Pattern Implementation
- **Strategy Pattern**: Service abstraction for translators, parsers, mappers
- **Factory Pattern**: Centralized creation and registration
- **Observer Pattern**: Monitoring and logging capabilities
- **Template Method Pattern**: Common workflows with custom steps

## Configuration and Setup

### Required Dependencies
```bash
pip install pywikibot wikitextparser litellm
```

### Configuration Files
```bash
# Pywikibot setup
pywikibot generate_user_files

# Configure Arabic Wikipedia bot account
# Set GEMINI_API_KEY environment variable
export GEMINI_API_KEY="your-google-ai-api-key"
```

### Environment Variables
```bash
GEMINI_API_KEY="your-api-key"
GOOGLE_AI_API_KEY="your-api-key"
TRANSLATION_DEFAULT_SERVICE="gemini"
TRANSLATION_ENABLE_CACHING="true"
```

## Usage Examples

### Complete Pipeline Execution
```python
from tasks.InfoboxSync.test import run_wikipedia_pipeline

# Sync Arabic Wikipedia page
result_path = run_wikipedia_pipeline(
    ar_page_title="مصر",  # Egypt in Arabic
    target_lang='ar',
    output_dir='output',
    template_type='country'
)
```

### Individual Stage Usage
```python
# Fetch stage
from fetch.fetch import fetch_wikipedia_data
wiki_data = fetch_wikipedia_data("egypt")

# Parse stage
from parse.parse import parse_data
parsed = parse_data(wiki_data, 'country')

# Map stage
from map.map import map_data
mapped = map_data(parsed, 'country')

# Translate stage
from translate.translate import translate_data
translated = translate_data(mapped, 'ar')

# Construct stage
from construct.build import construct_arabic_template
template = construct_arabic_template(translated, 'country')

# And so on...
```

## Data Flow and Integration

Each stage produces structured data that seamlessly flows to the next stage:

1. **Fetch** → `PageInfo` objects with content and metadata
2. **Parse** → Structured infobox dicts with categories and links
3. **Map** → Arabic field mappings with validation
4. **Translate** → Translated content with confidence scores
5. **Construct** → Valid MediaWiki template strings
6. **Localize** → Arabic Wikipedia compatible content
7. **Publish** → Revision results with edit metadata
8. **Save** → Comprehensive JSON archive of entire pipeline

## Quality Assurance

### Validation and Error Handling
- **Comprehensive Logging**: Detailed logs at each stage
- **Graceful Degradation**: Pipeline continues despite partial failures
- **Data Validation**: Input/output validation at each stage
- **Error Recovery**: Retry mechanisms and fallback strategies

### Testing and Monitoring
- **Unit Tests**: Individual stage testing
- **Integration Tests**: End-to-end pipeline testing
- **Performance Monitoring**: Timing and resource usage tracking
- **Quality Metrics**: Translation accuracy and template validation scores

## Performance Characteristics

### Efficiency Features
- **Single-Request Translation**: ~80% cost reduction vs individual calls
- **Lazy Loading**: Components initialized only when needed
- **Caching**: Translation and API response caching
- **Batch Processing**: Optimized for multiple pages

### Scalability
- **Modular Design**: Stages can be scaled independently
- **Memory Efficient**: Streaming processing for large datasets
- **Rate Limiting**: Respects Wikipedia API limits
- **Parallel Processing**: Support for concurrent page processing

## Future Enhancements

### Planned Improvements
- **Additional Translation Services**: OpenAI, DeepL, Microsoft Translator
- **Template Recognition**: ML-powered infobox template detection
- **Community Integration**: "واو" template system expansion
- **Quality Assessment**: Automated translation quality scoring
- **Real-time Processing**: Event-driven pipeline execution
- **Web Interface**: GUI for pipeline management and monitoring

## Contributing

The pipeline is designed with extensibility in mind:
- **New Translation Services**: Implement `TranslationService` interface
- **Custom Parsers**: Extend `InfoboxParser` base class
- **Additional Template Types**: Register new factories and mappers
- **Validation Rules**: Add custom field validation logic

## Support and Documentation

Each stage includes comprehensive documentation covering:
- Technical architecture and design decisions
- API usage examples and code patterns
- Configuration options and best practices
- Error handling and troubleshooting guides
- Performance optimization recommendations
- Extension points and customization options

This documentation provides a complete reference for understanding, using, and extending the InfoboxSync pipeline system.

---

**Version**: 1.0
**Last Updated**: January 2025
**Authors**: InfoboxSync Development Team