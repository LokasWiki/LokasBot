# InfoboxSync Pipeline - Complete Technical Documentation

## Volume 1: Pipeline Architecture and Core Classes

### Chapter 1: Overview

The InfoboxSync pipeline is a comprehensive system for synchronizing Wikipedia infoboxes between English and Arabic Wikipedia sites. This document provides a complete book-style reference to all classes, their methods, and their interactions within the pipeline.

## Part I: Fetch Stage Architecture

### Chapter 2: Fetch Stage Location System Design

#### Section 2.1: Base Classes and Interfaces

**Class: `WikipediaFetcher` (Abstract Base Class)**
```python
class WikipediaFetcher(ABC):
    """Abstract base class for Wikipedia page fetchers using Template Method pattern."""
```

**Location**: `fetch/interfaces.py` and `fetch/fetch.py`
**Inheritance**: ABC (Abstract Base Class)
**Purpose**: Defines the skeletal structure for Wikipedia page fetching operations
**Design Pattern**: Template Method Pattern

**Key Abstract Methods**:
- `get_site_name() -> str`: Returns site identifier ('en', 'ar', etc.)
- `_check_page_exists(page_title: str) -> PageInfo`: Verifies page existence
- `_fetch_page_content(page_info: PageInfo) -> PageInfo`: Retrieves full content
- `_fetch_langlinks(page_info: PageInfo) -> PageInfo`: Gets language links

**Concrete Implementation Example**:
```python
class PywikibotFetcher(WikipediaFetcher):
    """Pywikibot implementation of Wikipedia fetcher."""
```

#### Section 2.2: Observer Pattern Implementation

**Class: `FetchObserver` (Abstract Interface)**
```python
class FetchObserver(ABC):
    """Observer pattern for monitoring fetch operations."""
```

**Location**: `fetch/observers.py`
**Referenced From**: `fetch/fetch.py`
**Purpose**: Enables monitoring of fetch operations without coupling

**Core Observer Methods**:
- `on_page_check_start(page_title: str, site: str)`: Called when page check begins
- `on_page_check_complete(page_info: PageInfo)`: Called when page check completes
- `on_error(error: str)`: Called when errors occur

**Concrete Implementations**:
```python
class LoggingFetchObserver(FetchObserver):
    """Logging implementation of fetch observer."""

class MetricsFetchObserver(FetchObserver):
    """Metrics collection implementation of fetch observer."""
    def __init__(self):
        self.metrics = {
            'pages_checked': 0,
            'pages_found': 0,
            'pages_not_found': 0,
            'errors': 0
        }

    def get_metrics() -> dict:
        """Returns current metrics snapshot."""
        return self.metrics.copy()
```

#### Section 2.3: Data Transfer Objects

**Class: `PageInfo` (Data Class)**
```python
@dataclass
class PageInfo:
    """Data class for page information."""
    title: str
    exists: bool
    content: Optional[str] = None
    langlinks: Optional[Dict[str, str]] = None
    error: Optional[str] = None
```

**Location**: `fetch/fetch.py`, `fetch/models.py`
**Purpose**: Immutable data container for Wikipedia page information
**Fields**:
- `title`: Page title
- `exists`: Boolean indicating page existence
- `content`: Raw wikitext content (when exists)
- `langlinks`: Dictionary of language links (e.g., `{'ar': 'Arabic Title', 'es': 'Spanish Title'}`)
- `error`: Error message if operation failed

**Usage Pattern**:
```python
# Creating a successful page info
success_page = PageInfo(
    title="Egypt",
    exists=True,
    content="{{Infobox country\n|name=Egypt\n...}}",
    langlinks={'ar': 'مصر', 'fr': 'Égypte'}
)

# Creating an error page info
error_page = PageInfo(
    title="NonExistentPage",
    exists=False,
    error="Page not found"
)
```

**Class: `SyncResult` (Data Class)**
```python
@dataclass
class SyncResult:
    """Data class for synchronization results."""
    arabic: PageInfo
    english: Optional[PageInfo]
    sync_possible: bool
    error: Optional[str] = None
```

**Location**: `fetch/models.py`
**Purpose**: Container for Arabic-English page synchronization results
**Fields**:
- `arabic`: Arabic Wikipedia page information
- `english`: English Wikipedia page information (may be None)
- `sync_possible`: Boolean indicating if synchronization can proceed
- `error`: Error message if sync determination failed

#### Section 2.4: Main Fetch Coordinator

**Class: `WikipediaSyncFetcher`**
```python
class WikipediaSyncFetcher:
    """Main fetcher class using Strategy pattern for different fetch strategies."""
```

**Location**: `fetch/fetch.py`
**Purpose**: Orchestrates fetching of both Arabic and corresponding English pages
**Composition**:
- `ar_fetcher`: PywikibotFetcher for Arabic Wikipedia
- `en_fetcher`: PywikibotFetcher for English Wikipedia

**Key Methods**:

**`__init__(self, observer: Optional[FetchObserver] = None)`**
```python
def __init__(self, observer: Optional[FetchObserver] = None):
    self.observer = observer or LoggingFetchObserver()
    self.ar_fetcher = PywikibotFetcher('ar', self.observer)
    self.en_fetcher = PywikibotFetcher('en', self.observer)
```

**`fetch_arabic_and_english_pages(self, ar_page_title: str) -> Dict[str, Any]`**
```python
def fetch_arabic_and_english_pages(self, ar_page_title: str) -> Dict[str, Any]:
    """
    Fetch Arabic page and corresponding English page if exists.

    Returns dict with:
    - 'arabic': PageInfo object
    - 'english': PageInfo object or None
    - 'sync_possible': bool
    - 'error': error message or None
    """
```

**`_find_english_page_title(self, ar_page_info: PageInfo) -> Optional[str]`**
```python
def _find_english_page_title(self, ar_page_info: PageInfo) -> Optional[str]:
    """
    Find corresponding English page title from Arabic page links.

    Strategy:
    1. Check langlinks from Arabic page ('en' key)
    2. Fallback: Use Arabic title as English title (for same-name pages)
    """
```

#### Section 2.5: Main Entry Point Function

**Function: `fetch_wikipedia_data(ar_page_title: str) -> Dict[str, Any]`**
```python
def fetch_wikipedia_data(ar_page_title: str) -> Dict[str, Any]:
    """
    Main function to fetch Wikipedia data for sync operation.

    Args:
        ar_page_title (str): Arabic page title to sync

    Returns:
        dict: Dictionary with Arabic and English page data
    """
    fetcher = WikipediaSyncFetcher()
    return fetcher.fetch_arabic_and_english_pages(ar_page_title)
```

**Location**: `fetch/fetch.py`
**Purpose**: Public API entry point for the fetch stage
**Return Format**:
```python
{
    'arabic': PageInfo(...),
    'english': PageInfo(...) or None,
    'sync_possible': True/False,
    'error': error_message or None
}
```

### Chapter 3: Fetch Stage Usage Examples

#### Section 3.1: Basic Usage

```python
from tasks.InfoboxSync.fetch.fetch import fetch_wikipedia_data

# Fetch page data
result = fetch_wikipedia_data("مصر")  # Egypt in Arabic

# Check if sync is possible
if result['sync_possible']:
    arabic_page = result['arabic']
    english_page = result['english']

    print(f"Arabic title: {arabic_page.title}")
    print(f"English title: {english_page.title}")
    print(f"Arabic content length: {len(arabic_page.content)}")
    print(f"English content length: {len(english_page.content)}")
else:
    print(f"Sync not possible: {result['error']}")
```

#### Section 3.2: Advanced Usage with Observers

```python
from tasks.InfoboxSync.fetch.observers import MetricsFetchObserver
from tasks.InfoboxSync.fetch.fetch import WikipediaSyncFetcher

# Create metrics observer
metrics_observer = MetricsFetchObserver()

# Create fetcher with observer
fetcher = WikipediaSyncFetcher(observer=metrics_observer)

# Fetch data
result = fetcher.fetch_arabic_and_english_pages("محمد بن سلمان")

# Get performance metrics
metrics = metrics_observer.get_metrics()
print(f"Pages checked: {metrics['pages_checked']}")
print(f"Pages found: {metrics['pages_found']}")
print(f"Success rate: {metrics['pages_found']/metrics['pages_checked']:.1%}")
```

## Part II: Parse Stage Architecture

### Chapter 4: Parser Class Hierarchy

#### Section 4.1: Abstract Parser Base Class

**Class: `InfoboxParser` (Abstract Base Class)**
```python
class InfoboxParser(ABC):
    """
    Abstract base class for infobox parsers using Strategy Pattern.
    Manages different template types and parsing strategies.
    """
```

**Location**: `parse/base_parser.py`, `parse/parsers.py`
**Inheritance**: ABC (Abstract Base Class)
**Purpose**: Defines interface for parsing different Wikipedia infobox templates
**Design Pattern**: Strategy Pattern

**Key Attributes**:
- `template_name`: Lowercase string identifier for target template
- `wikitextparser`: Imported instance for advanced wikitext manipulation

**Abstract Methods**:
```python
@abstractmethod
def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
    """Parse the infobox from wikitext. Returns extracted field data."""
```

**Utility Methods**:

**`_find_template(self, parsed_wikitext: wtp.WikiText) -> wtp.Template`**
```python
def _find_template(self, parsed_wikitext: wtp.WikiText) -> wtp.Template:
    """
    Find the target template in parsed wikitext.
    Searches all templates and matches by name.

    Args:
        parsed_wikitext: Parsed wikitext object from wikitextparser

    Returns:
        wtp.Template: Matched template object or None
    """
```

**`_extract_template_arguments(self, template: wtp.Template) -> Dict[str, str]`**
```python
def _extract_template_arguments(self, template: wtp.Template) -> Dict[str, str]:
    """
    Extract key-value pairs from Wikipedia template object.
    Handles argument name and value extraction with wiki syntax cleanup.

    Args:
        template: wikitextparser Template object

    Returns:
        Dict[str, str]: Cleaned argument dictionary {key: value}
    """
```

#### Section 4.2: Concrete Parser Implementations

**Class: `FootballBiographyParser` (Concrete Strategy)**
```python
class FootballBiographyParser(InfoboxParser):
    """Parser for Infobox football biography template."""
```

**Location**: `parse/football_parser.py`, `parse/parsers.py`
**Purpose**: Specialized parser for football biography infoboxes
**Target Template**: `"infobox football biography"`

**Implementation**:
```python
def __init__(self):
    super().__init__("infobox football biography")

def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
    """Parse football biography infobox with specialized handling."""
    infobox_data = {}

    try:
        # Parse wikitext using wikitextparser
        parsed = wikitextparser.parse(wikitext)

        # Find football biography template
        football_bio_template = self._find_template(parsed)

        if football_bio_template:
            logger.info("Found Infobox football biography template")
            infobox_data = self._extract_template_arguments(football_bio_template)
            logger.info(f"Extracted {len(infobox_data)} fields")
        else:
            logger.warning("Football biography template not found")

    except Exception as e:
        logger.error(f"Error parsing football biography: {e}")

    return infobox_data
```

**Class: `GenericInfoboxParser` (Concrete Strategy)**
```python
class GenericInfoboxParser(InfoboxParser):
    """Generic parser for any infobox template type."""
```

**Location**: `parse/parsers.py`
**Purpose**: Fallback parser for any infobox template not having specialized parser
**Configuration**: Accepts template name in constructor

**Implementation**:
```python
def __init__(self, template_name: str):
    super().__init__(template_name)

def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
    """Parse generic infobox template."""
    infobox_data = {}

    try:
        parsed = wikitextparser.parse(wikitext)
        template = self._find_template(parsed)

        if template:
            logger.info(f"Found {self.template_name} template")
            infobox_data = self._extract_template_arguments(template)
        else:
            logger.warning(f"No {self.template_name} template found")

    except Exception as e:
        logger.error(f"Error parsing {self.template_name}: {e}")

    return infobox_data
```

#### Section 4.3: Parser Factory

**Class: `InfoboxParserFactory`**
```python
class InfoboxParserFactory:
    """Factory class to create appropriate parsers based on template type."""
```

**Location**: `parse/parser_factory.py`, `parse/parsers.py`
**Purpose**: Centralizes parser creation logic using Factory Pattern
**Design Pattern**: Factory Pattern

**Core Method**:
```python
@staticmethod
def create_parser(template_type: str) -> InfoboxParser:
    """
    Create appropriate parser instance for template type.

    Strategy:
    1. 'football_biography' → FootballBiographyParser()
    2. 'person' → GenericInfoboxParser('infobox person')
    3. 'biography' → GenericInfoboxParser('infobox biography')
    4. Everything else → GenericInfoboxParser(template_type)
    """
```

**Supported Template Types**:
```python
@staticmethod
def get_supported_types() -> list:
    """Return list of explicitly supported template types."""
    return ['football_biography', 'person', 'biography']
```

#### Section 4.4: Main Parse Functions

**Function: `parse_data(data: dict, template_type: str) -> dict`**
```python
def parse_data(data: dict, template_type: str = 'football_biography') -> dict:
    """
    Parse Wikipedia page data to extract structured information.

    Data Flow:
    1. Extract page content and metadata
    2. Create appropriate parser via factory
    3. Parse infobox template
    4. Extract categories and links
    5. Return structured data dictionary

    Args:
        data: Dictionary containing 'content', 'title', etc.
        template_type: Template type identifier

    Returns:
        dict: Parsed data with infobox, categories, links
    """
```

**Return Format**:
```python
{
    'title': page_title,                    # Original page title
    'arabic_title': arabic_page_title,     # Arabic equivalent title
    'infobox': {...},                      # Extracted infobox fields
    'categories': [...],                   # List of categories
    'links': [...],                       # List of internal links
    'raw_content': original_wikitext       # Original page content
}
```

**Helper Functions**:

**`extract_categories_from_wikitext(wikitext: str) -> list`**
```python
def extract_categories_from_wikitext(wikitext: str) -> list:
    """
    Extract category links using regex pattern.
    Pattern: [[Category:CategoryName]]
    Returns: List of category names
    """
```

**`extract_links_from_wikitext(wikitext: str) -> list`**
```python
def extract_links_from_wikitext(wikitext: str) -> list:
    """
    Extract internal links using regex pattern.
    Pattern: [[LinkName|DisplayText]]
    Filters out special links (File:, Category:, Template:)
    Returns: List of article titles
    """
```

## Part III: Map Stage Architecture

### Chapter 5: Field Mapping Class System

#### Section 5.1: Abstract Field Mapper

**Class: `FieldMapper` (Abstract Base Class)**
```python
class FieldMapper(ABC):
    """Abstract base class for field mapping strategies."""
```

**Location**: `map/field_mappers.py`
**Purpose**: Defines interface for different field type mapping strategies
**Design Pattern**: Strategy Pattern (for field types)

**Key Attributes**:
- `english_key`: Original English field name
- `arabic_key`: Target Arabic field name
- `field_type`: Identifier for field mapping strategy

**Abstract Methods**:
```python
@abstractmethod
def map_field(self, value: str) -> Dict[str, Any]:
    """Map field value to standardized format with validation."""
```

**Utility Methods**:
```python
def _clean_value(self, value: str) -> str:
    """Clean and normalize field value."""
    return value.strip() if value else ""
```

#### Section 5.2: Field Type Strategies

**Class: `TextFieldMapper` (Concrete Strategy)**
```python
class TextFieldMapper(FieldMapper):
    """Mapper for text fields (names, descriptions, etc.)."""
```

**Purpose**: Handles plain text fields like names, descriptions
**Validation**: Length checks, special character detection
**Output Format**:
```python
{
    arabic_key: {
        "value": clean_text_value,
        "type": "text",
        "original_key": english_key,
        "validation": {
            "is_valid": True/False,
            "length": character_count,
            "has_special_chars": True/False
        }
    }
}
```

**Class: `NumberFieldMapper` (Concrete Strategy)**
```python
class NumberFieldMapper(FieldMapper):
    """Mapper for numeric fields (ages, years, counts, etc.)."""
```

**Purpose**: Handles numerical data with unit extraction
**Features**:
- Numeric value extraction from text
- Unit preservation (m, kg, years, etc.)
- Range validation
**Validation Checks**:
- Non-null numeric value
- Unit format validity
- Reasonable value ranges

**Class: `ImageFieldMapper` (Concrete Strategy)**
```python
class ImageFieldMapper(FieldMapper):
    """Mapper for image fields with wiki syntax parsing."""
```

**Purpose**: Handles image links and captions
**Wiki Syntax Processing**: `[[File:image.jpg|caption text]]`
**Validation Features**:
- Filename extraction
- Caption detection
- Image format validation

**Class: `LinkFieldMapper` (Concrete Strategy)**
```python
class LinkFieldMapper(FieldMapper):
    """Mapper for link fields (internal/external links)."""
```

**Purpose**: Processes wiki links and URLs
**Link Type Detection**:
- Internal wiki links: `[[Page|Display]]`
- External links: `[http://example.com Text]`
**Validation**: URL format, display text presence

**Class: `NumberedFieldMapper` (Composite Strategy)**
```python
class NumberedFieldMapper(FieldMapper):
    """Mapper for numbered fields following pattern: field1, field2, field3..."""
```

**Purpose**: Groups numbered sequences into arrays
**Example Transformation**:
```
Input:  years1="2000", years2="2001", years3="2002"
Output: "سنوات": ["2000", "2001", "2002"]
```

**Key Method**:
```python
def map_numbered_fields(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
    """Group numbered fields into sequenced array."""
```

#### Section 5.3: Field Mapper Factory

**Class: `FieldMapperFactory`**
```python
class FieldMapperFactory:
    """Factory for creating appropriate field mappers."""
```

**Location**: `map/field_mappers.py`
**Purpose**: Creates field mappers based on field type
**Factory Strategy**:
```python
field_type_map = {
    "text": lambda ek, ak: TextFieldMapper(ek, ak),
    "number": lambda ek, ak: NumberFieldMapper(ek, ak),
    "image": lambda ek, ak: ImageFieldMapper(ek, ak),
    "link": lambda ek, ak: LinkFieldMapper(ek, ak),
    "numbered": lambda ek, ak: NumberedFieldMapper(ek, ak, "text"),
    "mixed": lambda ek, ak: MixedFieldMapper(ek, ak)
}
```

#### Section 5.4: Template Mapper Hierarchy

**Class: `TemplateMapper` (Abstract Base Class)**
```python
class TemplateMapper(ABC):
    """Abstract base class for template-specific field mapping."""
```

**Location**: `map/template_mapper.py`
**Purpose**: Orchestrates template-level field mappings
**Composition**: Uses FieldMapperFactory for individual field processing

**Key Methods**:
```python
@abstractmethod
def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]:
    """Return field mapping configuration for this template type."""

def map_infobox(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
    """Map entire infobox using configured field mappers."""
```

**Field Mapping Format**:
```python
field_mappings = {
    "english_field_name": {
        "arabic_key": "الاسم_العربي",
        "field_type": "text|number|image|link|numbered|mixed|raw",
        "item_type": "text|number"  # For numbered fields
    }
}
```

**Class: `FootballBiographyMapper` (Concrete Implementation)**
```python
class FootballBiographyMapper(TemplateMapper):
    """Mapper for football biography infobox templates."""
```

**Purpose**: Specialized mapper for football player infoboxes
**Features**:
- Personal information mapping
- Club career numbered fields (clubs1, years1, caps1, goals1...)
- National team numbered fields
- Managerial role fields
- Honors and achievements

**Field Mappings Include**:
```python
{
    # Personal Info
    "name": {"arabic_key": "اسم", "field_type": "text"},
    "fullname": {"arabic_key": "الاسم الكامل", "field_type": "text"},
    "image": {"arabic_key": "صورة", "field_type": "image"},
    "height": {"arabic_key": "الطول", "field_type": "number"},
    
    # Numbered Club Career Fields
    "clubs": {"arabic_key": "أندية", "field_type": "numbered", "item_type": "raw"},
    "years": {"arabic_key": "سنوات", "field_type": "numbered", "item_type": "raw"},
    "caps": {"arabic_key": "مباريات", "field_type": "numbered", "item_type": "number"},
    "goals": {"arabic_key": "أهداف", "field_type": "numbered", "item_type": "number"}
}
```

#### Section 5.5: Template Mapper Factory

**Class: `TemplateMapperFactory`**
```python
class TemplateMapperFactory:
    """Factory for creating appropriate template mappers."""
```

**Mapper Registration**:
```python
@staticmethod
def create_mapper(template_type: str) -> TemplateMapper:
    """Create appropriate template mapper based on type."""
    template_type = template_type.lower()
    
    mapper_registry = {
        'football_biography': FootballBiographyMapper,
        'person': GenericTemplateMapper,
        'biography': GenericTemplateMapper
    }
    
    mapper_class = mapper_registry.get(template_type, GenericTemplateMapper)
    return mapper_class()
```

#### Section 5.6: Main Map Function

**Function: `map_data(parsed_data: dict, template_type: str) -> dict`**
```python
def map_data(parsed_data: dict, template_type: str = 'football_biography') -> dict:
    """
    Map parsed infobox data to Arabic field mappings.

    Processing Steps:
    1. Extract infobox data and metadata
    2. Create appropriate template mapper
    3. Process numbered fields first (grouping)
    4. Process regular fields with type-specific mappers
    5. Return structured Arabic field data
    """
```

**Data Flow**:
1. **Input**: Parsed data from Parse stage
2. **Processing**: 
   - Template mapper selection
   - Numbered field grouping
   - Individual field mapping with validation
3. **Output**: Arabic field dictionary with metadata

## Part IV: Translate Stage Architecture

### Chapter 6: Translation Service Hierarchy

#### Section 6.1: Translation Service Interface

**Class: `TranslationService` (Abstract Base Class)**
```python
class TranslationService(ABC):
    """Abstract base class for translation services."""
```

**Location**: `translate/base_translator.py`
**Purpose**: Defines translation service interface
**Design Pattern**: Strategy Pattern

**Key Attributes**:
- `source_lang`: Source language code ('en')
- `target_lang`: Target language code ('ar')

**Abstract Methods**:
```python
@abstractmethod
def translate_text(self, text: str, **kwargs) -> TranslationResult
@abstractmethod
def translate_field(self, field_name: str, field_value: Any, **kwargs) -> TranslationResult
@abstractmethod
def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]
@abstractmethod
def is_available(self) -> bool
@abstractmethod
def get_service_name(self) -> str
```

#### Section 6.2: Translation Result Data Structure

**Class: `TranslationResult`**
```python
class TranslationResult:
    """Result of a translation operation."""
    def __init__(self, translated_text: str, original_text: str,
                 confidence: float = 1.0, metadata: Optional[Dict[str, Any]] = None):
        self.translated_text = translated_text
        self.original_text = original_text
        self.confidence = confidence
        self.metadata = metadata or {}
```

**Fields**:
- `translated_text`: The translated text
- `original_text`: Original text (for verification)
- `confidence`: Translation confidence score (0.0-1.0)
- `metadata`: Additional translation metadata

#### Section 6.3: Translation Service Factory

**Class: `TranslationServiceFactory`**
```python
class TranslationServiceFactory:
    """Factory for creating translation services."""
    _services = {}  # Registry of available services
```

**Core Methods**:
```python
@classmethod
def register_service(cls, service_name: str, service_class):
    """Register a new translation service."""

@classmethod
def create_service(cls, service_name: str, **kwargs) -> TranslationService:
    """Create translation service instance."""

@classmethod
def get_available_services(cls) -> List[str]:
    """Return list of available service names."""
```

#### Section 6.4: Gemini Translation Implementation

**Class: `GeminiTranslator` (Concrete Implementation)**
```python
class GeminiTranslator(TranslationService):
    """Google Gemini AI translation service using LiteLLM."""
```

**Key Features**:
- **Single-Request Optimization**: Translates ALL fields in one API call
- **Prompt Engineering**: Customizable prompt templates
- **Content-Type Awareness**: Different translation rules for different data types
- **Cost Optimization**: ~80% reduction in API costs vs individual calls

**Configuration Attributes**:
```python
def __init__(self, api_key: Optional[str] = None, model: str = "gemini/gemini-2.0-flash",
             source_lang: str = 'en', target_lang: str = 'ar', temperature: float = 0.3,
             max_tokens: int = 5000):
    # API and model configuration
    self.api_key = api_key or os.getenv('GEMINI_API_KEY')
    self.model = model
    self.temperature = temperature
    self.max_tokens = max_tokens
```

**Key Methods**:

**`translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]`**
```python
def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Translate entire infobox in SINGLE API request.

    Process:
    1. Prepare single-request prompt with all fields
    2. Call Gemini API once
    3. Parse single response back into field structure
    4. Return translated infobox with metadata
    """
```

**`_get_infobox_translation_prompt(self, infobox_data: Dict[str, Any]) -> tuple[str, dict]`**
```python
def _get_infobox_translation_prompt(self, infobox_data: Dict[str, Any]) -> tuple[str, dict]:
    """
    Generate prompt for single-request infobox translation.
    
    Returns:
        tuple: (formatted_prompt, field_mapping_dict)
    """
```

**`_parse_single_request_response(self, response_text: str, field_mapping: dict) -> Dict[str, Any]`**
```python
def _parse_single_request_response(self, response_text: str, field_mapping: dict) -> Dict[str, Any]:
    """Parse single-request response back into field dictionary."""
```

#### Section 6.5: Configuration Management

**Class: `TranslationConfig`**
```python
class TranslationConfig:
    """Configuration manager for translation services."""
```

**Configuration Sources** (in priority order):
1. Constructor parameter
2. Environment variables
3. File configuration (JSON)
4. Default configuration

**Environment Variables**:
- `GEMINI_API_KEY` or `GOOGLE_AI_API_KEY`
- `TRANSLATION_DEFAULT_SERVICE`
- `TRANSLATION_ENABLE_CACHING`
- `TRANSLATION_CACHE_MAX_SIZE`

#### Section 6.6: Prompt Template System

The translation stage uses external prompt templates loaded from file:

**File Location**: `translate/prompt_template.txt`
**Purpose**: Customizable prompt engineering for AI translation

**Features**:
- Template variable replacement (`{{FIELDS_TEXT}}`, `{{START_INDEX}}`)
- Content-type specific instructions
- Football terminology translations
- Wiki syntax preservation rules

## Part V: Construct Stage Architecture

### Chapter 7: Template Builder Hierarchy

#### Section 7.1: Builder Interface

**Class: `TemplateBuilder` (Abstract Base Class)**
```python
class TemplateBuilder(ABC):
    """Abstract base class for template builders."""
```

**Location**: `construct/base_builder.py`
**Purpose**: Defines template construction interface
**Design Pattern**: Builder Pattern

**Abstract Methods**:
```python
@abstractmethod
def construct_template(self, translated_data: Dict[str, Any], **kwargs) -> BuildResult
@abstractmethod
def format_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str
@abstractmethod
def get_template_name(self) -> str
@abstractmethod
def is_available(self) -> bool
@abstractmethod
def get_builder_name(self) -> str
```

**Build Result Structure**:
```python
@dataclass
class BuildResult:
    template_text: str
    template_type: str
    field_count: int
    success: bool
    metadata: Dict[str, Any]
    errors: List[str]
```

#### Section 7.2: Arabic Template Builder

**Class: `ArabicTemplateBuilder` (Concrete Builder)**
```python
class ArabicTemplateBuilder(TemplateBuilder):
    """Builder for Arabic Wikipedia templates using translated data."""
```

**Key Features**:
- **Template Name Mapping**: Maps template types to Arabic names
- **Field Type Formatting**: Different formatters for different field types
- **Unicode Support**: Full Arabic text and character set handling
- **Wiki Syntax Compliance**: Proper MediaWiki template formatting

**Field Formatters Configuration**:
```python
def __init__(self, template_type: str = 'football_biography'):
    super().__init__(template_type)
    self.field_formatters = {
        'text': self._format_text_field,
        'number': self._format_number_field,
        'image': self._format_image_field,
        'link': self._format_link_field,
        'numbered': self._format_numbered_field,
        'mixed': self._format_mixed_field
    }
```

**Template Name Mappings**:
```python
def get_template_name(self) -> str:
    template_names = {
        'football_biography': 'صندوق معلومات سيرة كرة قدم',
        'person': 'صندوق شخص',
        'biography': 'سيرة شخصية',
        'football_club': 'صندوق نادي كرة قدم',
        # ... more mappings
    }
    return template_names.get(self.template_type, 'صندوق عام')
```

#### Section 7.3: Builder Factory

**Class: `TemplateBuilderFactory`**
```python
class TemplateBuilderFactory:
    """Factory for creating template builders."""
    _builders = {}  # Builder registry
```

**Builder Registration**:
```python
arabic_builder_registered = TemplateBuilderFactory.register_builder(
    "arabic", ArabicTemplateBuilder
)
```

**Factory Methods**:
```python
@classmethod
def create_builder(cls, builder_name: str, **kwargs) -> TemplateBuilder:
    """Create template builder instance."""
    
@classmethod
def get_available_builders(cls) -> List[str]:
    """Get list of available builder names."""
    
@classmethod  
def get_supported_template_types(cls) -> List[str]:
    """Get supported template types across all builders."""
```

## Part VI: Integration and Usage

### Chapter 8: Pipeline Integration

#### Section 8.1: Complete Pipeline Flow

**Complete Pipeline Function**:
```python
from tasks.InfoboxSync.test import run_wikipedia_pipeline

def run_wikipedia_pipeline(ar_page_title: str, target_lang: str = 'ar',
                          output_dir: str = 'output',
                          template_type: str = 'football_biography') -> str:

    # Stage 1: Fetch
    wiki_data = fetch_wikipedia_data(ar_page_title)
    
    # Stage 2: Parse  
    parsed_data = parse_data(wiki_data, template_type)
    
    # Stage 3: Map
    mapped_data = map_data(parsed_data, template_type)
    
    # Stage 4: Translate
    translated_data = translate_data(mapped_data, target_lang)
    
    # Stage 5: Build Arabic Template
    build_result = construct_arabic_template(translated_data, template_type)
    
    # Stage 6: Wiki Localization
    localization_result = process_construct_to_publish(build_result)
    
    # Stage 7: Publish to Arabic Wikipedia
    publish_result = publish_data(localization_result.localized_data, ar_page_title)
    
    # Stage 8: Save Results
    saved_path = save_data(processed_data, output_dir)
    
    return saved_path
```

#### Section 8.2: Stage-by-Stage Data Flow

Each stage transforms and enriches the data:

1. **Fetch Stage**: ʺRawʺ → PageInfo objects
2. **Parse Stage**: PageInfo → Structured fields + categories + links  
3. **Map Stage**: English fields → Arabic field mappings + validation
4. **Translate Stage**: English text → Arabic translations + confidence
5. **Construct Stage**: Arabic mappings → Valid wiki template syntax
6. **Wiki Localization**: Template → Localized links and formats
7. **Publish Stage**: Template → Live on Arabic Wikipedia
8. **Save Stage**: Complete pipeline data → JSON archive

#### Section 8.3: Error Propagation and Handling

**Error Handling Strategy**:
- Each stage handles its own errors gracefully
- Partial failures don't stop entire pipeline  
- Error metadata preserved for debugging
- Fallback mechanisms for critical failures

**Pipeline Error Recovery**:
```python
try:
    # Each stage operation
    result = stage_function(data)
    if not result.success:
        logger.error(f"Stage failed: {result.errors}")
        # Implement recovery or graceful degradation
except Exception as e:
    logger.error(f"Stage exception: {e}")
    # Handle critical errors
```

## Part VII: Configuration and Deployment

### Chapter 9: Configuration Management

#### Section 9.1: Environment Configuration

**Required Environment Variables**:
```bash
# Pywikibot Configuration
export PYWIKIBOT2_DIR=/path/to/pywikibot/config

# Google Gemini API
export GEMINI_API_KEY="your-gemini-api-key"
export GOOGLE_AI_API_KEY="your-api-key"

# Translation Settings
export TRANSLATION_DEFAULT_SERVICE="gemini"
export TRANSLATION_ENABLE_CACHING="true"

# Optional settings
export TRANSLATION_CACHE_MAX_SIZE="1000"
export TRANSLATION_REQUEST_TIMEOUT="30"
```

#### Section 9.2: Pywikibot Setup

**Bot Account Setup**:
1. Create Arabic Wikipedia bot account
2. Configure user-config.py with credentials
3. Set appropriate user agent
4. Configure edit rate limits

**File Structure**:
```
pywikibot-config/
├── user-config.py          # Bot credentials and settings
├── family-wikipedia.py     # Wiki family definitions
├── pywikibot.lwp           # Login credentials (encrypted)
└── logs/                   # Operation logs
```

## Part VIII: Monitoring and Maintenance

### Chapter 10: Monitoring and Analytics

#### Section 10.1: Pipeline Metrics

**Performance Tracking**:
- Translation success rates
- API call latency and costs
- Template validation quality scores
- Publish operation success rates

#### Section 10.2: Logging Architecture

**Comprehensive Logging**:
```python
# Each stage includes detailed logging
logger = logging.getLogger('infoboxsync')

# Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('infoboxsync.log'),
        logging.StreamHandler()
    ]
)
```

---

## Conclusion

The InfoboxSync pipeline represents a comprehensive, production-ready system for automated Wikipedia infobox synchronization. Its modular, pattern-based architecture ensures maintainability, extensibility, and robust error handling while delivering high-quality Arabic Wikipedia content through advanced AI translation and direct wiki integration.

### Key Architecture Strengths

1. **Modular Design**: Each stage is independently testable and replaceable
2. **Rich Error Handling**: Comprehensive validation and recovery mechanisms
3. **Performance Optimization**: Single-request translation, smart caching
4. **Extensibility**: Factory patterns enable easy addition of new components
5. **Quality Assurance**: Validation, monitoring, and comprehensive logging
6. **Production Ready**: Handles real-world Wikipedia operations reliably

### Technology Integration

The system successfully integrates multiple complex technologies:
- **Wikipedia API**: Pywikibot for seamless wiki interaction
- **AI Translation**: Google's Gemini AI via LiteLLM
- **Text Processing**: Wikitextparser for advanced wiki markup handling
- **Data Persistence**: JSON serialization with Unicode support
- **Error Recovery**: Graceful degradation and fallback mechanisms

This comprehensive book-style documentation serves as the complete technical reference for understanding, implementing, and extending the InfoboxSync pipeline system.