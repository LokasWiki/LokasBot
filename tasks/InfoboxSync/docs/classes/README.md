# Individual Class Documentation Index

This directory contains comprehensive API-style documentation for every major class in the InfoboxSync pipeline system.

## 📁 Class Documentation Files

### 🔍 Fetch Stage Classes

#### [**WikipediaFetcher**](WikipediaFetcher.md)
**Abstract Base Class**
- **Purpose**: Template Method pattern for Wikipedia page fetching
- **Methods**: `get_site_name()`, `fetch_page_info()`, `_check_page_exists()`, `_fetch_page_content()`, `_fetch_langlinks()`
- **Pattern**: Template Method with Strategy hooks
- **Status**: Abstract - must be subclassed

#### [**PywikibotFetcher**](PywikibotFetcher.md)
**Concrete Implementation**
- **Purpose**: pywikibot-powered Wikipedia data retrieval
- **Features**: Arabic & English wiki support, lazy site initialization, language link extraction
- **Methods**: Site management, page existence checking, content fetching
- **Dependencies**: `pywikibot`, `WikipediaFetcher` base class
- **Availability**: Production-ready for Arabic and English Wikipedia

### 🧩 Parse Stage Classes

#### [**InfoboxParser**](InfoboxParser.md)
**Abstract Strategy Class**
- **Purpose**: Parse different Wikipedia infobox template types
- **Implementations**: `FootballBiographyParser`, `GenericInfoboxParser`
- **Features**: Wikitextparser integration, template discovery, argument extraction
- **Factory**: `InfoboxParserFactory` for parser creation
- **Status**: Abstract base class with concrete implementations

### 🗺️ Map Stage Classes

#### [**FieldMapper**](FieldMapper.md)
**Abstract Strategy Base**
- **Purpose**: Transform individual fields according to data type
- **Field Types**: `TextFieldMapper`, `NumberFieldMapper`, `ImageFieldMapper`, `LinkFieldMapper`
- **Special Types**: `NumberedFieldMapper` (composite pattern), `MixedFieldMapper`
- **Factory**: `FieldMapperFactory` for creation based on type
- **Validation**: Built-in field validation for each type

#### [**TemplateMapper**](TemplateMapper.md)
**Template Strategy Class**
- **Purpose**: Orchestrate mapping for entire infobox templates
- **Implementations**: `FootballBiographyMapper`, `GenericTemplateMapper`
- **Features**: Field grouping, numbered field processing, metadata tracking
- **Field Integration**: Uses `FieldMapper` hierarchy internally
- **Statistics**: Provides mapping success rates and field counts

### 🌐 Translate Stage Classes

#### [**GeminiTranslator**](GeminiTranslator.md)
**AI Translation Strategy**
- **Purpose**: Google Gemini AI-powered translation service
- **Innovation**: Single-request translation (80% cost reduction)
- **Features**: Prompt engineering, content-type awareness, batch translation
- **Dependencies**: `litellm`, Google Gemini API
- **Performance**: Cost-optimized, fast, context-aware translations

### 🏗️ Construct Stage Classes

#### [**ArabicTemplateBuilder**](ArabicTemplateBuilder.md)
**Concrete Template Builder**
- **Purpose**: Construct proper Arabic Wikipedia templates
- **Features**: Field type formatting, template name mapping, wiki syntax compliance
- **Field Types**: Text, number, image, link, numbered fields
- **Unicode**: Full Arabic text support
- **Factory**: `TemplateBuilderFactory` for builder creation

## 🔗 Class Relationships & Architecture

### Strategy Pattern Hierarchy

```
🌳 Abstract Base Classes (ABC)
│
├── WikipediaFetcher (ABC) ── PywikibotFetcher
│
├── InfoboxParser (ABC) ───── FootballBiographyParser
│                             GenericInfoboxParser
│
├── FieldMapper (ABC) ─────── TextFieldMapper
│                             NumberFieldMapper
│                             ImageFieldMapper
│                             LinkFieldMapper
│                             NumberedFieldMapper
│                             MixedFieldMapper
│
├── TemplateMapper (ABC) ──── FootballBiographyMapper
│                             GenericTemplateMapper
│
└── TemplateBuilder (ABC) ─── ArabicTemplateBuilder
```

### Factory Pattern Implementation

```python
📋 Factory Classes:
├── TranslationServiceFactory ──── GeminiTranslator
├── InfoboxParserFactory ────────── FootballBiographyParser, GenericInfoboxParser
├── FieldMapperFactory ──────────── Text/Number/Image/Link/Mixed/NumberedFieldMapper
└── TemplateBuilderFactory ──────── ArabicTemplateBuilder
```

### Template Method Pattern

```python
🔄 Template Method Classes:
├── WikipediaFetcher ── fetch_page_info() [Main Algorithm]
├── InfoboxParser ────────────── Strategy Interface
├── TemplateMapper ─── map_infobox() [Field Orchestration]
└── ArabicTemplateBuilder ────── construct_template() [Build Process]
```

## 📊 Class Documentation Features

### 🔍 Consistent Documentation Structure

Each class documentation includes:

1. **🎯 Class Reference**: Namespace, inheritance, design pattern
2. **📝 Overview**: Purpose, scope, and key features
3. **🏗️ Constructor**: Parameters, initialization details
4. **📋 Attributes**: Class member variables and their purposes
5. **⚡️ Methods**: Complete method signatures and descriptions
6. **🚀 Usage Examples**: Practical code examples
7. **🛡️ Error Handling**: Exception handling strategies
8. **⚡ Performance**: Optimization features and considerations
9. **🔗 Integration**: How class works with others
10. **🧪 Testing**: Testing patterns and unit test examples

### 📖 API Reference Coverage

**Complete Method Documentation**:
- Abstract method contracts (what subclasses must implement)
- Public method APIs (what clients can call)
- Protected method behaviors (internal coordination)
- Static utility methods (helper functions)
- Factory method patterns (creation mechanisms)

**Parameter Documentation**:
- Required vs. optional parameters
- Parameter types and constraints
- Default values and their significance
- Special parameter handling cases

**Return Value Documentation**:
- Return types and data structures
- Success vs. error response patterns
- Metadata inclusion strategies
- Validation result formats

## 🎨 Real-World Usage Patterns

### Complete Pipeline Integration

```python
# 1. Factory Creation Pattern
fetcher = PywikibotFetcher('ar')
parser = InfoboxParserFactory.create_parser('football_biography')
mapper = TemplateMapperFactory.create_mapper('football_biography')
translator = TranslationServiceFactory.create_service('gemini')
builder = TemplateBuilderFactory.create_builder('arabic', template_type='football_biography')

# 2. Template Method Execution
page_data = fetcher.fetch_page_info("مصر")
infobox_data = parser.parse_infobox(page_data.content)
mapped_fields = mapper.map_infobox(infobox_data)
translated = translator.translate_infobox(mapped_fields)
template = builder.construct_template(translated)

# 3. Strategy Pattern Flexibility
# Easily swap implementations:
parser = InfoboxParserFactory.create_parser('person')  # Different strategy
translator = TranslationServiceFactory.create_service('custom_ai')  # Different strategy
```

### Error Handling Cascade

```python
# Robust pipeline with error containment
try:
    page_info = fetcher.fetch_page_info(title)
    if not page_info.exists:
        # Page not found - return appropriate error
        return {"error": "Page not found", "title": title}

    parsed = parser.parse_infobox(page_info.content)
    if not parsed:
        # Template not found - return fallback
        return {"fallback": True, "raw_content": page_info.content}

    mapped = template_mapper.map_infobox(parsed)
    if mapped['total_mapped_fields'] == 0:
        # No fields mapped - log but continue
        log.warning("No fields mapped successfully")
        # Still have basic structure from parsed data

    translated = translator.translate_infobox(mapped)
    if not translated.get('success', False):
        # Translation failed - return with original
        return {"partial_translate": True, "data": mapped}

    template = builder.construct_template(translated)
    return {"success": True, "template": template.template_text}

except Exception as e:
    logger.error(f"Pipeline stage failed: {e}")
    # Comprehensive error handling maintains pipeline integrity
    return {"error": str(e), "stage": "unknown"}
```

## 📈 Design Pattern Implementation

### 🏭 Factory Pattern Usage

**Service Discovery**:
```python
# Translation services
available = TranslationServiceFactory.get_available_services()
['gemini', 'openai', 'deepl']  # Extensible registry

# Parser strategies
parser = InfoboxParserFactory.create_parser('football_biography')
# Returns: FootballBiographyParser vs GenericInfoboxParser

# Field mappers
field_mapper = FieldMapperFactory.create_mapper("height", "الطول", "number")
# Returns: NumberFieldMapper instance
```

**Factory Benefits**:
- **Extensibility**: New services easily added to registry
- **Centralization**: Service creation logic in one place
- **Consistency**: Standardized creation patterns
- **Testing**: Easy mocking of services in unit tests

### 🎭 Strategy Pattern Implementation

**Multiple Translation Strategies**:
```python
# Strategy interface
class TranslationService(ABC):
    def translate_infobox(self, data: dict) -> dict:
        pass  # Strategy contract

# Concrete strategies
class GeminiTranslator(TranslationService):
    def translate_infobox(self, data: dict) -> dict:
        return self._single_request_translation(data)

class OpenAITranslator(TranslationService):
    def translate_infobox(self, data: dict) -> dict:
        return self._multi_request_translation(data)

class CustomTranslator(TranslationService):
    def translate_infobox(self, data: dict) -> dict:
        return self._custom_translation_logic(data)

# Usage - same interface, different implementations
translators = {
    'cost_effective': GeminiTranslator(),
    'high_quality': OpenAITranslator(),
    'specialized': CustomTranslator()
}

for name, translator in translators.items():
    result = translator.translate_infobox(fb_data)
    # Same interface, different results based on strategy
```

### 🔧 Template Method Pattern

**Consistent Processing Framework**:
```python
# Template Method in WikipediaFetcher
def fetch_page_info(self, page_title: str) -> PageInfo:
    """Template method with consistent structure."""

    # 1. Pre-fetch setup (hook point)
    self.observer.on_page_check_start(page_title, self.get_site_name())

    # 2. Core algorithm steps (implemented in subclasses)
    page_info = self._check_page_exists(page_title)  # Subclass implements

    if page_info.exists:
        page_info = self._fetch_page_content(page_info)   # Subclass implements
        page_info = self._fetch_langlinks(page_info)      # Subclass implements

    # 3. Post-fetch cleanup (hook point)
    self.observer.on_page_check_complete(page_info)

    return page_info  # Consistent return format
```

## 🧪 Testing Patterns

### Unit Test Coverage

**Mock-Based Testing**:
```python
# Mock external dependencies
@patch('pywikibot.Page')
def test_pywikibot_fetcher(mock_page_class):
    # Mock pywikibot behavior
    mock_page = mock.Mock()
    mock_page.exists.return_value = True
    mock_page.text = "Page content"
    mock_page_class.return_value = mock_page

    fetcher = PywikibotFetcher('test')
    result = fetcher._check_page_exists("Test")

    assert result.exists is True
    assert result.content == "Page content"
```

**Factory Testing**:
```python
def test_factory_creation():
    # Test factory returns correct type
    parser = InfoboxParserFactory.create_parser('football_biography')
    assert isinstance(parser, FootballBiographyParser)

    # Test unknown type defaults
    generic = InfoboxParserFactory.create_parser('unknown_type')
    assert isinstance(generic, GenericInfoboxParser)
```

**Integration Testing**:
```python
def test_full_pipeline_integration():
    # Integration test with real data flow
    fetcher = PywikibotFetcher('test')
    parser = FootballBiographyMapper()
    # ... full pipeline test
    # Verify end-to-end data transformation
```

## 📋 Extension Guide

### Adding New Translation Service

1. **Implement TranslationService Interface**:
```python
class DeepLTranslator(TranslationService):
    def translate_infobox(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement DeepL-specific logic
        pass
```

2. **Register with Factory**:
```python
# In factory registration
TranslationServiceFactory.register_service("deepl", DeepLTranslator)
```

3. **Add Configuration**:
```python
# In config
"deepl": {
    "model": "deepl:translate",
    "api_key_env_vars": ["DEEPL_API_KEY"]
}
```

4. **Update Documentation**:
```python
# Add to available services list
available_services = ['gemini', 'deepl']  # Now includes DeepL
```

### Adding New Parser Strategy

1. **Implement InfoboxParser**:
```python
class MovieParser(InfoboxParser):
    def __init__(self):
        super().__init__("infobox film")

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        # Movie-specific parsing logic
        pass
```

2. **Add to Factory**:
```python
# Extend factory method
def create_parser(template_type: str) -> InfoboxParser:
    if template_type == 'movie':
        return MovieParser()
    # existing mappings...
```

## 🔍 Troubleshooting Guide

### Common Issues and Solutions

**🚫 pywikibot Not Found**:
```python
ImportError: pywikibot is required
# Solution: pip install pywikibot
```

**⚠️ API Key Missing**:
```python
KeyError: API key for gemini not found
# Solution: export GEMINI_API_KEY="your-key"
```

**🔍 Template Not Found**:
```python
Warning: No football biography template found
# Solution: Verify page has correct template name
```

**🌍 Translation Timeout**:
```python
Exception: Translation request timed out
# Solution: Check API quotas and network connectivity
```

## 📚 Additional Resources

### 📄 Related Documentation
- **[Main Pipeline Documentation](../README.md)**: Overall pipeline overview
- **[Complete Guide](../InfoboxSync_Complete_Guide.md)**: Comprehensive technical reference
- **[Stage Documentations](../fetch_stage.md, ../parse_stage.md, etc.)**: Stage-specific details

### 🎯 Quick Class References
- **Data Classes**: `PageInfo`, `TranslationResult`, `BuildResult`
- **Factory Classes**: Service creation and management
- **Abstract Classes**: Extension points and interfaces
- **Concrete Classes**: Production-ready implementations

### 🛠️ Development Tools
- **Design Patterns**: Strategy, Factory, Template Method implementations
- **Testing Frameworks**: Unit test patterns and integration testing
- **Configuration**: Environment variables and config management
- **Logging**: Structured logging and monitoring

---

**📁 Classes Directory**: `tasks/InfoboxSync/docs/classes/`
**📖 Documentation Format**: API Reference Style with Examples
**🎯 Coverage**: All Major Pipeline Classes Documented
**🔄 Updates**: Keep in sync with code changes