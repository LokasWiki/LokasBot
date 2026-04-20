# Construct Stage - Arabic Wikipedia Template Construction

This directory contains the construct stage implementation for constructing Arabic Wikipedia templates from translated infobox data.

## Overview

The build stage takes translated data from the translate stage and constructs properly formatted Arabic Wikipedia templates. It follows the Strategy Pattern to support different template types and formats.

## Architecture

### Core Components

1. **`base_builder.py`** - Abstract base classes and factory pattern
2. **`arabic_builder.py`** - Arabic Wikipedia template builder implementation
3. **`build.py`** - Main construct stage interface and utilities

### Design Patterns Used

- **Strategy Pattern**: Different template builders for various Wikipedia template types
- **Factory Pattern**: Creation of appropriate builders via `TemplateBuilderFactory`
- **Template Method**: Consistent template construction workflow

## Features

### Template Construction
- Constructs properly formatted Arabic Wikipedia templates
- Handles different field types (text, numbers, links, images, numbered arrays)
- Supports multiple template types (football biography, person, country, etc.)
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

## Usage

### Basic Usage

```python
from tasks.InfoboxSync.construct.build import construct_arabic_template

# Your translated data from translate stage
translated_data = {
    'translated_fields': {
        'الاسم': {'value': 'Paul Abasolo', 'translated_value': 'بول أباسولو', 'type': 'text'},
        'الطول': {'value': '1.84 m', 'translated_value': '1.84 م', 'type': 'number'},
        # ... more translated fields
    }
}

# Construct Arabic template
result = construct_arabic_template(translated_data, template_type='football_biography')

if result.success:
    arabic_template = result.template_text
    print(f"Constructed template with {result.field_count} fields")
    print(arabic_template)
else:
    print(f"Construction failed: {result.errors}")
```

### Advanced Usage

```python
from tasks.InfoboxSync.construct.build import construct_template, TemplateBuilderFactory

# Create specific builder
builder = TemplateBuilderFactory.create_builder('arabic', template_type='person')

# Construct template
result = builder.construct_template(translated_data)

# Access build metadata
print(f"Template type: {result.template_type}")
print(f"Fields included: {result.field_count}")
print(f"Builder used: {result.metadata['builder_name']}")
```

### Template Validation

```python
from tasks.InfoboxSync.construct.build import validate_arabic_template, estimate_template_quality

# Validate template
validation = validate_arabic_template(template_text)
print(f"Valid: {validation['valid']}")
print(f"Errors: {validation['errors']}")

# Estimate quality
quality = estimate_template_quality(template_text)
print(f"Quality score: {quality['quality_score']}/100")
```

## Data Flow

### Input Data Structure
```python
{
    'translated_fields': {
        'arabic_field_name': {
            'value': 'original_value',
            'translated_value': 'arabic_translation',
            'type': 'text|number|link|image|numbered',
            'translation_confidence': 0.9
        }
    },
    'translation_metadata': {...},
    'page_title': 'English Title',
    'arabic_title': 'Arabic Title'
}
```

### Output Data Structure
```python
{
    'template_text': '{{صندوق سيرة لاعب كرة قدم\n| الاسم = بول أباسولو\n| الطول = 1.84 م\n...}}',
    'template_type': 'football_biography',
    'field_count': 8,
    'success': True,
    'metadata': {
        'template_name': 'سيرة لاعب كرة قدم',
        'builder_name': 'Arabic Football Biography Builder',
        'total_input_fields': 10
    },
    'errors': []
}
```

## Template Construction Process

1. **Extract Translated Fields** - Get translated data from translate stage
2. **Select Template Type** - Choose appropriate Arabic template name
3. **Format Each Field** - Apply proper Arabic Wikipedia syntax
4. **Handle Field Types** - Special formatting for numbers, links, arrays
5. **Construct Template** - Construct complete template with all fields
6. **Validate Output** - Check for syntax errors and formatting issues

## Field Type Handling

### Text Fields
```
Input:  {'value': 'Paul Abasolo', 'translated_value': 'بول أباسولو'}
Output: | الاسم = بول أباسولو
```

### Number Fields
```
Input:  {'value': '1.84 m', 'translated_value': '1.84 م'}
Output: | الطول = 1.84 م
```

### Numbered Fields (Arrays)
```
Input:  {'value': ['Club A', 'Club B'], 'translated_value': ['النادي أ', 'النادي ب']}
Output:
| الأندية1 = النادي أ
| الأندية2 = النادي ب
```

### Link Fields
```
Input:  {'value': 'Argentina', 'translated_value': 'الأرجنتين'}
Output: | الجنسية = [[الأرجنتين]]
```

## Extending the Build Stage

### Adding New Template Types

```python
from tasks.InfoboxSync.construct.arabic_builder import ArabicTemplateBuilder

class CustomArabicBuilder(ArabicTemplateBuilder):
    def __init__(self):
        super().__init__('custom_type')

    def get_template_name(self) -> str:
        return 'صندوق مخصص'

    def format_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        # Custom formatting logic
        return f"| {arabic_key} = {field_data['translated_value']}"

# Register the builder
from tasks.InfoboxSync.construct.base_builder import TemplateBuilderFactory
TemplateBuilderFactory.register_builder("custom_arabic", CustomArabicBuilder)
```

### Custom Field Formatters

```python
class AdvancedArabicBuilder(ArabicTemplateBuilder):
    def _format_custom_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        # Advanced custom formatting
        value = field_data.get('translated_value', '')
        return f"| {arabic_key} = '''{value}'''"

    def format_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
        field_type = field_data.get('type', 'text')

        if field_type == 'custom':
            return self._format_custom_field(arabic_key, field_data)
        else:
            return super().format_field(arabic_key, field_data)
```

## Integration with Pipeline

The construct stage seamlessly integrates with the InfoboxSync pipeline:

1. **Receives** translated data from translate stage
2. **Constructs** Arabic Wikipedia template
3. **Passes** template text to save stage
4. **Provides** metadata for logging and debugging

## Quality Assurance

### Template Validation
- Syntax checking for Arabic Wikipedia format
- Field count verification
- Error and warning reporting

### Quality Estimation
- Quality scoring algorithm (0-100)
- Issue detection (escaped characters, formatting problems)
- Template complexity analysis

## Performance Considerations

- **Efficient Processing**: Single-pass field formatting
- **Memory Optimized**: Streaming template construction
- **Error Resilient**: Continues processing despite individual field errors

## Troubleshooting

### Common Issues

1. **Empty Template Output**
   - Check if translated_fields contains valid data
   - Verify field types are supported
   - Check for translation stage errors

2. **Malformed Template Syntax**
   - Ensure proper Arabic Wikipedia template names
   - Check for special character escaping
   - Validate field formatting

3. **Unsupported Template Type**
   - Add new template type mapping in `get_template_name()`
   - Extend field formatters if needed
   - Register new builder class

### Debug Information

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

The construct stage provides comprehensive logging for:
- Template construction process
- Field formatting details
- Error conditions and recovery
- Performance metrics

## Future Enhancements

- Support for additional Arabic template types
- Advanced template customization options
- Integration with Arabic Wikipedia bot frameworks
- Template quality improvement suggestions
- Multi-language template support
- Template validation against Arabic Wikipedia standards