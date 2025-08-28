# Parse Stage Documentation

## Overview

The Parse stage is responsible for extracting structured data from raw Wikipedia wikitext content. This critical stage transforms the fetched page content into usable data structures that can be processed by subsequent stages. It employs advanced wikitext parsing using the `wikitextparser` library and implements Strategy Pattern for different template types.

## Design Patterns Used

### 1. Strategy Pattern
- **Context**: `parse_data()` function
- **Abstract Strategy**: `InfoboxParser` (abstract base class)
- **Concrete Strategies**:
  - `FootballBiographyParser` - Specialized for football biography infoboxes
  - `GenericInfoboxParser` - Generic parser for any infobox template
- **Purpose**: Allows different parsing strategies for different Wikipedia template types

### 2. Factory Pattern
- **Factory Class**: `InfoboxParserFactory`
- **Products**: Various parser implementations
- **Purpose**: Centralized creation of appropriate parsers based on template type

### 3. Template Method Pattern
- **Base Class**: `InfoboxParser`
- **Hook Methods**:
  - `_find_template()` - Template discovery logic
  - `_extract_template_arguments()` - Argument extraction logic
- **Purpose**: Defines common parsing workflow with customizable steps

## Core Components

### Strategy Interface (InfoboxParser)

```python
class InfoboxParser(ABC):
    def __init__(self, template_name: str)
    @abstractmethod
    def parse_infobox(self, wikitext: str) -> Dict[str, Any]
    def _find_template(self, parsed_wikitext: wtp.WikiText) -> wtp.Template
    def _extract_template_arguments(self, template: wtp.Template) -> Dict[str, str]
```

**Key Features:**
- Abstract base class defining parser interface
- Template discovery using wikitextparser
- Argument extraction from template objects
- Common functionality shared by all parsers

### Concrete Strategy Implementations

#### FootballBiographyParser
- **Target Template**: `infobox football biography`
- **Purpose**: Specialized parser for football player biographies
- **Special Handling**: Optimized for common football biography fields
- **Use Case**: Processing athlete infoboxes with career data

#### GenericInfoboxParser
- **Target Template**: Any template name (configurable)
- **Purpose**: Generic parser for standard infobox templates
- **Special Handling**: Works with person, biography, and custom templates
- **Use Case**: Processing general Wikipedia infoboxes

### Factory Implementation

#### InfoboxParserFactory
```python
@staticmethod
def create_parser(template_type: str) -> InfoboxParser
@staticmethod  
def get_supported_types() -> list
```

**Supported Template Types:**
- `football_biography` → `FootballBiographyParser`
- `person` → `GenericInfoboxParser("infobox person")`
- `biography` → `GenericInfoboxParser("infobox biography")`
- Custom templates → `GenericInfoboxParser(template_type)`

## Parsing Flow

### 1. Template Discovery
```python
def _find_template(self, parsed_wikitext: wtp.WikiText) -> wtp.Template:
    """Find target template in parsed wikitext."""
    templates = parsed_wikitext.templates
    for template in templates:
        if template.name.strip().lower() == self.template_name:
            return template
    return None
```

**Process:**
1. Parse wikitext using wikitextparser
2. Iterate through all templates in the page
3. Match template name (case-insensitive)
4. Return first matching template

### 2. Argument Extraction
```python
def _extract_template_arguments(self, template: wtp.Template) -> Dict[str, str]:
    """Extract key-value pairs from template."""
    infobox_data = {}
    for argument in template.arguments:
        key = argument.name.strip()
        value = argument.value.strip()
        clean_value = wtp.parse(value).plain_text()
        if key and clean_value:
            infobox_data[key] = clean_value
    return infobox_data
```

**Features:**
- Extracts template arguments (key-value pairs)
- Cleans wikitext markup for plain text values
- Filters out empty keys and values
- Returns structured dictionary

### 3. Additional Content Extraction

#### Category Extraction
```python
def extract_categories_from_wikitext(wikitext: str) -> list:
    """Extract category links using regex pattern."""
    pattern = r'\[\[Category:([^\]]+)\]\]'
    matches = re.findall(pattern, wikitext, re.IGNORECASE)
    return [match.strip() for match in matches]
```

#### Link Extraction
```python
def extract_links_from_wikitext(wikitext: str) -> list:
    """Extract internal links using regex pattern."""
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    matches = re.findall(pattern, wikitext)
    # Filter out special links and return cleaned list
```

## API Usage

### Main Entry Point

#### parse_data()
```python
def parse_data(data: dict, template_type: str = 'football_biography') -> dict:
    """
    Parse Wikipedia data and extract infobox information.

    Args:
        data (dict): Raw Wikipedia data with content
        template_type (str): Template type to parse

    Returns:
        dict: Parsed data with infobox, categories, and links
    """
```

**Input Format:**
```python
data = {
    'title': 'Page Title',
    'content': '{{Infobox football biography\n|name=Lionel Messi...}}',
    'arabic_title': 'العنوان العربي',
    'langlinks': {'en': 'Title', 'es': 'Título'}
}
```

**Output Format:**
```python
{
    'title': 'Page Title',
    'arabic_title': 'العنوان العربي',
    'infobox': {
        'name': 'Lionel Messi',
        'birth_date': '24 June 1987',
        'height': '1.70 m'
    },
    'categories': ['Argentine footballers', 'FC Barcelona players'],
    'links': ['La Liga', 'Argentina national football team'],
    'raw_content': 'Original wikitext content...'
}
```

### Template Type Selection

```python
from parse.parse import parse_data

# Football biography parsing
football_data = parse_data(raw_data, 'football_biography')

# Person infobox parsing  
person_data = parse_data(raw_data, 'person')

# Custom template parsing
custom_data = parse_data(raw_data, 'infobox custom_template')
```

### Factory Usage

```python
from parse.parser_factory import InfoboxParserFactory

# Get supported template types
supported = InfoboxParserFactory.get_supported_types()
print(supported)  # ['football_biography', 'person', 'biography']

# Create specific parser
parser = InfoboxParserFactory.create_parser('football_biography')

# Parse directly
result = parser.parse_infobox(wikitext)
```

## Advanced Features

### WikitextParser Integration

**Benefits over Regex-based Parsing:**
1. **Accurate Template Structure**: Understands nested templates and complex syntax
2. **Context Awareness**: Maintains template relationships and hierarchies
3. **Markup Preservation**: Can preserve or strip wikitext based on needs
4. **Error Resilience**: Handles malformed wikitext gracefully

**Usage Pattern:**
```python
import wikitextparser as wtp

# Parse entire page
parsed = wtp.parse(wikitext)
templates = parsed.templates

# Parse individual values for cleaning
clean_value = wtp.parse(raw_value).plain_text()
```

### Content Type Detection

The parse stage automatically detects and extracts:
- **Infobox Templates**: Structured data templates
- **Categories**: Page categorization information
- **Internal Links**: Wikipedia article cross-references
- **Special Links**: File, Template, Category references (filtered out)

### Error Handling

**Robust Error Management:**
- Missing templates → Empty infobox data (logged as warning)
- Malformed wikitext → Graceful degradation
- Parsing exceptions → Detailed error logging
- Category/link extraction failures → Continue with empty arrays

## Performance Considerations

### Optimization Strategies:
1. **Single Wikitext Parse**: Parse once, extract multiple data types
2. **Template Caching**: Cache discovered templates for reuse
3. **Selective Extraction**: Only extract needed content types
4. **Regex Optimization**: Compiled patterns for category/link extraction

### Memory Management:
- **Streaming Processing**: Handle large pages efficiently
- **Resource Cleanup**: Proper wikitextparser resource management
- **Incremental Processing**: Process templates as they're discovered

## Testing and Validation

### Test Scenarios:
- Well-formed infobox templates → Correct extraction
- Missing templates → Empty but valid results
- Malformed templates → Graceful error handling
- Multiple templates → Correct template selection
- Nested templates → Proper hierarchy handling

### Validation Checks:
- Template existence verification
- Argument extraction accuracy
- Category parsing correctness
- Link extraction validity
- Memory usage monitoring

## Extension Points

### Adding New Parsers:
```python
from parse.base_parser import InfoboxParser

class CustomTemplateParser(InfoboxParser):
    def __init__(self):
        super().__init__("infobox custom")
    
    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        # Custom parsing logic
        parsed = wtp.parse(wikitext)
        template = self._find_template(parsed)
        if template:
            # Custom extraction logic
            return self._custom_extract_arguments(template)
        return {}
```

### Registering New Template Types:
```python
from parse.parser_factory import InfoboxParserFactory

# Extend factory method
@staticmethod
def create_parser(template_type: str) -> InfoboxParser:
    if template_type == 'custom_type':
        return CustomTemplateParser()
    # ... existing logic
```

### Alternative Parsing Strategies:
```python
class RegexBasedParser(InfoboxParser):
    """Alternative regex-based parser for performance-critical scenarios."""
    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        # Regex-based extraction
        pass
```

## Integration with Pipeline

### Data Flow:
1. **Input**: Wikitext from Fetch stage
2. **Processing**: Template discovery and argument extraction
3. **Output**: Structured data for Map stage
4. **Metadata**: Categories and links for additional processing

### Error Propagation:
- Parse failures → Pipeline stops with detailed error
- Partial parsing → Continue with available data
- Missing templates → Warning logged, continue processing

### Configuration:
- Template type selection based on pipeline requirements
- Parser selection through factory pattern
- Error handling configuration

This parse stage provides a flexible, extensible foundation for extracting structured data from Wikipedia pages, leveraging advanced wikitext parsing capabilities while maintaining clean architecture through well-applied design patterns.