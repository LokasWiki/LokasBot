# InfoboxParser Class

## Class Reference

**Namespace**: `tasks.InfoboxSync.parse.parsers`, `tasks.InfoboxSync.parse.base_parser`

**Inherits**: `ABC` (Abstract Base Class)

**Design Pattern**: Strategy Pattern

## Overview

Abstract base class for Wikipedia infobox parsers using the Strategy Pattern design. Defines the interface for parsing different types of Wikipedia infobox templates, enabling interchangeable parsing strategies for various template types (football biography, person, biography, etc.).

## Constructor

```python
def __init__(self, template_name: str):
    """
    Initialize the infobox parser.

    Args:
        template_name: Name of the template to parse (lowercase)
    """
```

### Attributes

- **`template_name`**: `str` - Target template name in lowercase
- **wikitextparser**: Imported library for advanced wikitext processing

## Abstract Methods

### `parse_infobox(wikitext: str) -> Dict[str, Any]`
**Must be implemented by subclasses**

Main parsing method that extracts field data from wikitext.
```python
@abstractmethod
def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
    """
    Parse infobox template from wikitext.

    Args:
        wikitext: Raw Wikipedia page content

    Returns:
        Dict mapping field names to values, or empty dict if template not found
    """
    pass
```

## Utility Methods

### `_find_template(parsed_wikitext: wtp.WikiText) -> wtp.Template`
Finds the target template in parsed wikitext.
```python
def _find_template(self, parsed_wikitext: wtp.WikiText) -> wtp.Template:
    """
    Find the target template in parsed wikitext objects.

    Args:
        parsed_wikitext: Wikitextparser WikiText object

    Returns:
        wikitextparser Template object or None if not found
    """
    templates = parsed_wikitext.templates

    for template in templates:
        template_name = template.name.strip().lower()
        if template_name == self.template_name:
            return template

    return None  # Template not found
```

### `_extract_template_arguments(template: wtp.Template) -> Dict[str, str]`
Extracts key-value pairs from a template object.
```python
def _extract_template_arguments(self, template: wtp.Template) -> Dict[str, str]:
    """
    Extract arguments from template object.

    Processing steps:
    1. Iterate through template.arguments
    2. Extract key (name) and value
    3. Clean whitespace
    4. Apply optional text cleaning using wtp.parse().plain_text()
    5. Filter out empty keys/values

    Args:
        template: wikitextparser Template object

    Returns:
        Dict[str, str]: Cleaned argument dictionary {key: value}
    """
    infobox_data = {}

    for argument in template.arguments:
        key = argument.name.strip()
        value = argument.value.strip()

        if key and value:
            # Optional text cleaning for wiki markup
            clean_value = value  # or wtp.parse(value).plain_text()
            infobox_data[key] = clean_value

    return infobox_data
```

## Concrete Implementations

### FootballBiographyParser

**Location**: `tasks/InfoboxSync/parse/football_parser.py`

```python
class FootballBiographyParser(InfoboxParser):
    """Parser for Infobox football biography template."""

    def __init__(self):
        super().__init__("infobox football biography")

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        """Specialized parsing for football biography infoboxes."""
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
            infobox_data = {}

        return infobox_data
```

### GenericInfoboxParser

**Location**: `tasks/InfoboxSync/parse/parsers.py`

```python
class GenericInfoboxParser(InfoboxParser):
    """Generic parser for any infobox template type."""

    def __init__(self, template_name: str):
        """Accepts any template name for parsing."""
        super().__init__(template_name)

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        """Generic template parsing implementation."""
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
            infobox_data = {}

        return infobox_data
```

## Usage Examples

### Basic Strategy Pattern Usage

```python
from tasks.InfoboxSync.parse.parsers import FootballBiographyParser

# Create specialized parser
football_parser = FootballBiographyParser()

# Parse football biography page
football_biography_data = football_parser.parse_infobox(wikitext)

# Result: {'name': 'Lionel Messi', 'position': 'Forward', ...}
```

### Factory Pattern Integration

```python
from tasks.InfoboxSync.parse.parser_factory import InfoboxParserFactory

# Factory creates appropriate parser
football_parser = InfoboxParserFactory.create_parser('football_biography')
person_parser = InfoboxParserFactory.create_parser('person')
generic_parser = InfoboxParserFactory.create_parser('custom_template')

# All parsers implement same interface
football_data = football_parser.parse_infobox(wikitext)
person_data = person_parser.parse_infobox(wikitext)
custom_data = generic_parser.parse_infobox(wikitext)
```

### Complex Multi-Template Pages

```python
def parse_multi_template_page(wikitext: str) -> Dict[str, Dict]:
    """Parse page with multiple infobox templates."""
    results = {}

    # Create multiple parsers
    parsers = {
        'football_biography': FootballBiographyParser(),
        'person': GenericInfoboxParser('infobox person'),
        'biography': GenericInfoboxParser('infobox biography')
    }

    # Try each parser
    for template_type, parser in parsers.items():
        data = parser.parse_infobox(wikitext)
        if data:  # If template was found
            results[template_type] = data

    return results

# Usage
multi_data = parse_multi_template_page(wikitext)
# Result: {'football_biography': {...fields...}}
```

## Advanced Features

### Error Handling and Resilience

```python
def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
    """Robust parsing with comprehensive error handling."""
    infobox_data = {}

    try:
        if not wikitext or not wikitext.strip():
            logger.warning("Empty wikitext provided")
            return {}

        # Parse with wikitextparser (may raise exceptions)
        parsed = wikitextparser.parse(wikitext)

        # Find target template
        template = self._find_template(parsed)

        if template:
            logger.info(f"Found {self.template_name} template")

            # Extract arguments with error handling
            infobox_data = self._extract_template_arguments(template)

            # Log results
            logger.info(f"Extracted {len(infobox_data)} fields from {self.template_name}")
        else:
            logger.warning(f"No {self.template_name} template found in page")

    except Exception as e:
        logger.error(f"Error parsing {self.template_name}: {e}")
        # Return empty dict on error for graceful failure
        infobox_data = {}

    return infobox_data
```

### Template Name Flexibility

```python
# Case-insensitive matching
def _find_template(self, parsed_wikitext: wtp.WikiText) -> wtp.Template:
    for template in parsed_wikitext.templates:
        template_name = template.name.strip().lower()
        if template_name == self.template_name:
            return template
    return None

# Handles variations:
# "Infobox football biography" -> "infobox football biography"
# "FOOTBALL BIOGRAPHY" -> "football biography"
# " infobox football biography " -> "infobox football biography"
```

## Template Parsing Patterns

### Person Infobox Template

**Wikitext**:
``` Wikitext
{{Infobox person
| name = John Doe
| birth_date = {{Birth date|1980|5|15}}
| occupation = Scientist
}}
```

**Parsed Output**:
```python
{
    "name": "John Doe",
    "birth_date": "{{Birth date|1980|5|15}}",
    "occupation": "Scientist"
}
```

### Football Biography Template

**Wikitext**:
``` Wikitext
{{Infobox football biography
| name = Cristiano Ronaldo
| position = Forward
| clubs1 = Manchester United
| clubs2 = Real Madrid
}}
```

**Parsed Output**:
```python
{
    "name": "Cristiano Ronaldo",
    "position": "Forward",
    "clubs1": "Manchester United",
    "clubs2": "Real Madrid"
}
```

## Extension Points

### Custom Parser Implementation

```python
from tasks.InfoboxSync.parse.base_parser import InfoboxParser

class CustomMovieParser(InfoboxParser):
    """Custom parser for movie infoboxes."""

    def __init__(self):
        super().__init__("infobox film")

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        """Custom movie parsing logic."""
        infobox_data = {}

        try:
            parsed = wikitextparser.parse(wikitext)
            template = self._find_template(parsed)

            if template:
                # Custom processing for movie-specific fields
                infobox_data = self._extract_template_arguments(template)

                # Custom post-processing
                infobox_data = self._post_process_movie_data(infobox_data)

                logger.info(f"Parsed movie infobox with {len(infobox_data)} fields")
        except Exception as e:
            logger.error(f"Error parsing movie infobox: {e}")

        return infobox_data

    def _post_process_movie_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Custom post-processing for movie data."""
        # Add custom processing logic
        if 'released' in data:
            # Extract year from release date
            data['release_year'] = self._extract_year(data['released'])
        return data
```

### Factory Extension

```python
# Extend factory for custom parsers
class ExtendedInfoboxParserFactory(InfoboxParserFactory):
    """Extended factory with additional parsers."""

    @staticmethod
    def create_parser(template_type: str) -> InfoboxParser:
        """Create parser with extended support."""
        if template_type.lower() == 'movie':
            return CustomMovieParser()
        elif template_type.lower() == 'company':
            return GenericInfoboxParser('infobox company')
        else:
            # Fall back to base factory
            return super().create_parser(template_type)
```

## Testing

### Unit Testing Strategy

```python
import unittest.mock as mock

def test_abstract_parser():
    """Test abstract parser cannot be instantiated directly."""
    with pytest.raises(TypeError):
        InfoboxParser("test_template")  # Should raise TypeError

def test_concrete_parser():
    """Test concrete parser implementation."""
    parser = FootballBiographyParser()

    # Mock wikitextparser
    with mock.patch('wikitextparser.parse') as mock_parse:
        # Mock template
        mock_template = mock.Mock()
        mock_template.name = "infobox football biography"
        mock_template.arguments = [
            mock.Mock(name="name", value="Test Player"),
            mock.Mock(name="position", value="Forward")
        ]

        # Mock parsed wikitext
        mock_wikitext = mock.Mock()
        mock_wikitext.templates = [mock_template]
        mock_parse.return_value = mock_wikitext

        # Test parsing
        wikitext = "{{Infobox football biography\n|name=Test Player\n|position=Forward\n}}"
        result = parser.parse_infobox(wikitext)

        assert result == {"name": "Test Player", "position": "Forward"}
```

## Performance Considerations

### Memory Efficiency

```python
def parse_infobox_streaming(self, wikitext: str) -> Dict[str, Any]:
    """Memory-efficient parsing for large pages."""
    try:
        # Use streaming parser if available
        # Process templates incrementally
        # Avoid loading entire page into memory at once
        pass
    except Exception as e:
        logger.error(f"Streaming parse failed: {e}")
        # Fall back to standard parsing
        return self.parse_infobox(wikitext)
```

### Caching Strategies

```python
class CachedInfoboxParser(InfoboxParser):
    """Parser with result caching."""

    def __init__(self, template_name: str, max_cache_size: int = 100):
        super().__init__(template_name)
        self.cache = {}
        self.max_cache_size = max_cache_size

    def parse_infobox(self, wikitext: str) -> Dict[str, Any]:
        # Use content hash for caching
        content_hash = hash(wikitext)

        if content_hash in self.cache:
            return self.cache[content_hash]

        # Parse and cache result
        result = super().parse_infobox(wikitext)

        if len(self.cache) < self.max_cache_size:
            self.cache[content_hash] = result

        return result
```

## Integration with Pipeline

### Parse Stage Integration

```python
# Part of main parse function
def parse_data(data: dict, template_type: str = 'football_biography') -> dict:
    """
    Main parse stage function.

    1. Create appropriate parser via strategy pattern
    2. Parse infobox template
    3. Extract additional metadata (categories, links)
    4. Return structured data
    """
    page_content = data.get('content', '')
    page_title = data.get('title', '')

    # Strategy pattern: Create appropriate parser
    parser = InfoboxParserFactory.create_parser(template_type)

    # Parse infobox template
    infobox_data = parser.parse_infobox(page_content)

    # Extract additional metadata
    categories = extract_categories_from_wikitext(page_content)
    links = extract_links_from_wikitext(page_content)

    # Return structured data for next stage
    return {
        'title': page_title,
        'arabic_title': data.get('arabic_title', ''),
        'infobox': infobox_data,
        'categories': categories,
        'links': links,
        'raw_content': page_content
    }
```

## Related Classes

- **Concrete Implementations**: `FootballBiographyParser`, `GenericInfoboxParser`, `CustomMovieParser`
- **Factory Class**: `InfoboxParserFactory`
- **Integration Classes**: Parse stage functions (`parse_data`, `extract_categories_from_wikitext`)

---

**File Location**: `tasks/InfoboxSync/parse/base_parser.py` (abstract base), `tasks/InfoboxSync/parse/parsers.py` (concrete implementations)
**Status**: Abstract base class with production-ready concrete implementations
**Dependencies**: `wikitextparser`, `ABC`
**Since**: v1.0