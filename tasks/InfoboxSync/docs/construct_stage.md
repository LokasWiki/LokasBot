# Construct Stage Documentation

## Overview

The Construct stage is responsible for building properly formatted Arabic Wikipedia templates from translated data. It transforms the structured Arabic field data into valid MediaWiki template syntax suitable for publication on Arabic Wikipedia.

## Design Patterns Used

### 1. Strategy Pattern
- **Context**: `construct_template()` and `TemplateBuilder`
- **Abstract Strategy**: `TemplateBuilder` (abstract base class)
- **Concrete Strategies**:
  - `ArabicTemplateBuilder` - Specialized for Arabic Wikipedia templates
  - Extensible for other language variants
- **Purpose**: Enable different template construction strategies and formats

### 2. Factory Pattern
- **Factory Class**: `TemplateBuilderFactory`
- **Purpose**: Centralized creation of appropriate builders based on template type
- **Features**: Builder registration, discovery, and instantiation

### 3. Builder Pattern
- **Product**: Arabic Wikipedia templates
- **Director**: `construct_template()` function
- **Builders**: Specific template builders (ArabicTemplateBuilder)
- **Purpose**: Separate the construction of complex templates from their representation

## Core Components

### Builder Interface (TemplateBuilder)

```python
class TemplateBuilder(ABC):
    def construct_template(self, translated_data: Dict[str, Any], **kwargs) -> BuildResult
    def format_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str
    def get_template_name(self) -> str
    def is_available(self) -> bool
    def get_builder_name(self) -> str
```

### Build Result Model

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

## Arabic Template Builder

### Core Features
- **Template Name Mapping**: Maps template types to Arabic Wikipedia template names
- **Field Type Formatting**: Different formatting strategies for different field types
- **Unicode Support**: Full Arabic text and symbol support
- **Wiki Syntax Compliance**: Proper MediaWiki template formatting

### Template Name Mappings

```python
template_names = {
    'football_biography': 'صندوق معلومات سيرة كرة قدم',
    'person': 'صندوق شخص',
    'biography': 'سيرة شخصية',
    'football_club': 'صندوق نادي كرة قدم',
    'country': 'صندوق دولة',
    'city': 'صندوق مدينة'
}
```

### Field Formatting Strategies

#### Text Fields
```python
def _format_text_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
    value = field_data.get('value', '')
    escaped_value = str(value).replace('|', '{{!}}').replace('=', '{{=}}')
    return f"| {arabic_key} = {escaped_value}"
```

#### Number Fields
```python
def _format_number_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
    value = field_data.get('value', '')
    # Numbers remain unchanged
    return f"| {arabic_key} = {value}"
```

#### Numbered Fields
```python
def _format_numbered_field(self, arabic_key: str, field_data: Dict[str, Any]) -> List[str]:
    value = field_data.get('value', [])
    formatted_lines = []
    for i, item_value in enumerate(value, 1):
        field_name = f"{arabic_key}{i}"
        escaped_value = str(item_value)
        formatted_lines.append(f"| {field_name} = {escaped_value}")
    return formatted_lines
```

### Template Construction Process

1. **Extract Translated Fields**: Get translated_fields from input data
2. **Initialize Template Structure**: Start with template name and opening braces
3. **Format Each Field**: Apply appropriate formatting based on field type
4. **Handle Line Breaks**: Ensure proper MediaWiki line formatting
5. **Close Template**: Add closing braces
6. **Validation**: Basic template structure validation

## API Usage

### Main Entry Points

#### construct_template()
```python
def construct_template(translated_data: dict, builder_name: str = 'arabic',
                      template_type: str = 'football_biography') -> BuildResult:
    """
    Build an Arabic Wikipedia template from translated data.

    Args:
        translated_data (dict): Data from translate stage with translated_fields
        builder_name (str): Name of the builder to use
        template_type (str): Type of template to build

    Returns:
        BuildResult: Template building result with Arabic template text
    """
```

#### construct_arabic_template()
```python
def construct_arabic_template(translated_data: dict,
                             template_type: str = 'football_biography') -> BuildResult:
    """Convenience function for Arabic template construction."""
    return construct_template(translated_data, 'arabic', template_type)
```

### Input/Output Format

**Input Format:**
```python
{
    'translated_fields': {
        'اسم': {'value': 'ليونيل ميسي', 'type': 'text'},
        'الطول': {'value': 1.70, 'type': 'number'},
        'الأندية': {'value': ['FC Barcelona', 'PSG'], 'type': 'numbered'}
    },
    'translation_metadata': {...}
}
```

**Output Format:**
```python
BuildResult(
    template_text="{{صندوق معلومات سيرة كرة قدم\n| اسم = ليونيل ميسي\n| الطول = 1.70\n| الأندية1 = FC Barcelona\n| الأندية2 = PSG\n}}",
    template_type='football_biography',
    field_count=4,
    success=True,
    metadata={
        'template_name': 'صندوق معلومات سيرة كرة قدم',
        'builder_name': 'Arabic Football Biography Builder',
        'total_input_fields': 3
    },
    errors=[]
)
```

## Template Quality Features

### Validation Functions

#### validate_arabic_template()
```python
def validate_arabic_template(template_text: str) -> Dict[str, Any]:
    """Validate basic template structure."""
    return {
        'valid': True/False,
        'errors': [...],
        'warnings': [...],
        'field_count': 5,
        'template_length': 256
    }
```

#### estimate_template_quality()
```python
def estimate_template_quality(template_text: str) -> Dict[str, Any]:
    """Estimate template quality based on various metrics."""
    return {
        'quality_score': 85,
        'field_count': 8,
        'escaped_characters': 2,
        'issues': ['Contains escaped pipes'],
        'template_length': 450
    }
```

### Formatting Utilities

#### format_template_for_display()
```python
def format_template_for_display(template_text: str) -> str:
    """Format template with line numbers for debugging."""
```

## Integration with Pipeline

### Data Flow Connection Points

**Input → From Translate Stage:**
```python
translated_data = {
    'translated_fields': arabic_translated_fields,  # ← Construction input
    'translation_metadata': translation_info
}
```

**Output → To Wiki Localization Stage:**
```python
build_result = BuildResult(
    template_text=arabic_wiki_template,  # ← Localization input
    template_type=template_type,
    ...
)
```

### Error Handling and Recovery
- **Field Formatting Failures**: Individual field errors don't stop template construction
- **Missing Fields**: Empty values handled gracefully
- **Encoding Issues**: Unicode handling for Arabic text
- **Invalid Field Types**: Fallback to text formatting

### Pipeline Integration Benefits
- **Template Standardization**: Consistent Arabic Wikipedia template format
- **Quality Assurance**: Validation and error checking
- **Extensibility**: Easy addition of new template types
- **Metadata Propagation**: Build information carries through pipeline

This construct stage provides a robust, extensible foundation for transforming translated data into publication-ready Arabic Wikipedia templates, ensuring proper formatting and Wiki syntax compliance.