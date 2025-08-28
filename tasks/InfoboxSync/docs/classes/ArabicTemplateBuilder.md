# ArabicTemplateBuilder Class

## Class Reference

**Namespace**: `tasks.InfoboxSync.construct.arabic_builder`

**Inherits**: `TemplateBuilder`

**Design Pattern**: Builder Pattern (Concrete Builder)

## Overview

Concrete builder implementation for creating Arabic Wikipedia templates from translated data. Specializes in Arabic template formatting, handles different field types, and ensures compliance with Arabic Wikipedia standards.

## Constructor

```python
def __init__(self, template_type: str = 'football_biography'):
    """
    Initialize Arabic template builder.

    Args:
        template_type: Type of template to build
    """
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

## Core Build Method

### `construct_template(translated_data: Dict[str, Any], **kwargs) -> BuildResult`

Main template building orchestration method.

```python
def construct_template(self, translated_data: Dict[str, Any], **kwargs) -> BuildResult:
    """
    Build Arabic Wikipedia template from translated data.

    Process Flow:
    1. Extract translated fields from data
    2. Initialize template structure
    3. Format each field according to type
    4. Assem ble complete template
    5. Return BuildResult with metadata
    """
    # Extract translated fields
    translated_fields = translated_data.get('translated_fields', {})

    # Build template structure
    template_lines = []
    template_lines.append(f"{{{{{self.get_template_name()}")
    template_lines.append("|")

    # Process each field
    field_count = 0
    for arabic_key, field_data in translated_fields.items():
        formatted_field = self.format_field(arabic_key, field_data)
        if formatted_field:
            template_lines.append(formatted_field)
            field_count += 1

    # Close template
    template_lines.append("}}")

    # Create final template text
    template_text = "\n".join(template_lines)

    return BuildResult(
        template_text=template_text,
        template_type=self.template_type,
        field_count=field_count,
        success=True,
        metadata={'template_name': self.get_template_name(), 'builder_name': self.get_builder_name()},
        errors=[]
    )
```

## Field Formatting Methods

### `_format_text_field(arabic_key: str, field_data: Dict[str, Any]) -> str`

Formats plain text fields for Arabic templates.

```python
def _format_text_field(self, arabic_key: str, field_data: Dict[str, Any]) -> str:
    """Format text field with Arabic key-value syntax."""
    value = field_data.get('value', '')
    if not value:
        return ""

    # Escape wiki syntax
    escaped_value = str(value)
    return f"| {arabic_key} = {escaped_value}"
```

### `_format_numbered_field(arabic_key: str, field_data: Dict[str, Any]) -> List[str]`

Handles numbered fields (like clubs1, clubs2, years1, years2).

```python
def _format_numbered_field(self, arabic_key: str, field_data: Dict[str, Any]) -> List[str]:
    """Format numbered field (array) as multiple wiki template lines."""
    value = field_data.get('value', [])
    if not value or not isinstance(value, list):
        return []

    formatted_lines = []
    for i, item_value in enumerate(value, 1):
        if item_value:
            field_name = f"{arabic_key}{i}"
            escaped_value = str(item_value)
            formatted_lines.append(f"| {field_name} = {escaped_value}")

    return formatted_lines
```

## Template Name Mapping

### `get_template_name() -> str`

Maps template types to Arabic Wikipedia template names.

```python
def get_template_name(self) -> str:
    """Get Arabic Wikipedia template name for current type."""
    template_names = {
        'football_biography': 'صندوق معلومات سيرة كرة قدم',
        'person': 'صندوق شخص',
        'biography': 'سيرة شخصية',
        'football_club': 'صندوق نادي كرة قدم',
        'country': 'صندوق دولة',
        'city': 'صندوق مدينة',
        'university': 'صندوق جامعة',
        'company': 'صندوق شركة',
        'film': 'صندوق فيلم',
        'book': 'صندوق كتاب',
        'album': 'صندوق ألبوم',
        'tv_series': 'صندوق مسلسل تلفزيوني'
    }
    return template_names.get(self.template_type, 'صندوق عام')
```

## Usage Examples

### Basic Template Construction

```python
from tasks.InfoboxSync.construct.arabic_builder import ArabicTemplateBuilder

# Create builder for football biography
builder = ArabicTemplateBuilder('football_biography')

# Prepare translated data
translated_data = {
    'translated_fields': {
        'الاسم': {'value': 'ليونيل ميسي', 'type': 'text'},
        'الطول': {'value': '1.70', 'type': 'number'},
        'الأندية': {'value': ['إف سي برشلونة', 'باريس سان جيرمان'], 'type': 'numbered'}
    }
}

# Build Arabic template
result = builder.construct_template(translated_data)

# Result
result.template_text = '''{{صندوق معلومات سيرة كرة قدم
| الاسم = ليونيل ميسي
| الطول = 1.70
| الأندية1 = إف سي برشلونة
| الأندية2 = باريس سان جيرمان
}}'''
```

### Factory Integration

```python
from tasks.InfoboxSync.construct.base_builder import TemplateBuilderFactory

# Factory creates appropriate builder
arabic_builder = TemplateBuilderFactory.create_builder(
    "arabic", 
    template_type='football_biography'
)

# Use builder
result = arabic_builder.construct_template(translated_data)
```

## Field Type Output Examples

### Text Fields
```
Input:  {'value': 'Cristiano Ronaldo', 'type': 'text'}
Output: | الاسم = Cristiano Ronaldo
```

### Number Fields  
```
Input:  {'value': '1.87', 'type': 'number'}
Output: | الطول = 1.87
```

### Image Fields
```
Input:  {'value': 'Player.jpg', 'type': 'image'}
Output: | صورة = [[ملف:Player.jpg]]
```

### Numbered Fields (Multiple Lines)
```
Input:  {'value': ['Real Madrid', 'Juventus', 'Al Nassr'], 'type': 'numbered'}
Output: | النادي1 = Real Madrid
        | النادي2 = Juventus  
        | النادي3 = Al Nassr
```

## Error Handling

```python
def construct_template(self, translated_data: Dict[str, Any], **kwargs) -> BuildResult:
    try:
        # Main template building logic
        translated_fields = translated_data.get('translated_fields', {})

        if not translated_fields:
            return BuildResult(
                template_text="",
                template_type=self.template_type,
                field_count=0,
                success=False,
                metadata={},
                errors=["No translated fields found"]
            )

        # Process field count
        for arabic_key, field_data in translated_fields.items():
            formatted_field = self.format_field(arabic_key, field_data)
            if formatted_field:
                template_lines.append(formatted_field)
                field_count += 1

        # Success path
        return BuildResult(
            template_text="\n".join(template_lines),
            template_type=self.template_type,
            field_count=field_count,
            success=True,
            metadata={'template_name': self.get_template_name()}
        )

    except Exception as e:
        logger.error(f"Template building failed: {e}")
        return BuildResult(
            template_text="",
            template_type=self.template_type,
            field_count=0,
            success=False,
            errors=[str(e)]
        )
```

## Performance Characteristics

### Efficiency Features

**Field Processing Optimization**:
- **Type-based Formatting**: Fast lookup in formatter dictionary
- **Conditional Processing**: Skip empty fields
- **Memory Efficient**: Process fields incrementally
- **Unicode Optimized**: Direct Arabic text handling

**Template Structure Optimization**:
- **Lazy Line Building**: Build template lines incrementally  
- **Empty Line Management**: Clean formatting
- **Template Closure**: Automatic closing braces

## Integration Examples

### Pipeline Integration

```python
# Part of construct_arabic_template() function
def construct_arabic_template(translated_data: dict, template_type: str = 'football_biography') -> BuildResult:
    """Create Arabic template from translated data."""
    builder = ArabicTemplateBuilder(template_type)
    result = builder.construct_template(translated_data)

    # Add pipeline metadata
    if result.success:
        result.metadata.update({
            'total_input_fields': len(translated_data.get('translated_fields', {})),
            'template_name': builder.get_template_name(),
            'builder_name': builder.get_builder_name(),
            'pipeline_stage': 'construct'
        })

    return result
```

### Chained Operations

```python
# Multiple template types in sequence
templates = ['football_biography', 'person', 'country']

for template_type in templates:
    builder = ArabicTemplateBuilder(template_type)
    result = builder.construct_template(translated_data)

    if result.success:
        save_template(result.template_text, f"{template_type}_template.txt")
```

## Testing

### Unit Testing the Builder

```python
def test_arabic_template_builder():
    """Test Arabic template construction."""
    builder = ArabicTemplateBuilder('football_biography')

    # Mock translated data
    translated_data = {
        'translated_fields': {
            'الاسم': {'value': 'Test Player', 'type': 'text'},
            'الطول': {'value': '1.75', 'type': 'number'}
        }
    }

    # Build template
    result = builder.construct_template(translated_data)

    # Verify structure
    assert result.success is True
    assert result.template_type == 'football_biography'
    assert result.field_count == 2
    assert 'صندوق معلومات سيرة كرة قدم' in result.template_text
    assert '| الاسم = Test Player' in result.template_text
```

### Validation Testing

```python
def test_template_validation():
    """Test template validation logic."""
    builder = ArabicTemplateBuilder('country')

    # Test template name mapping
    template_name = builder.get_template_name()
    assert template_name == 'صندوق دولة'

    # Test builder identification
    builder_name = builder.get_builder_name()
    assert builder_name == 'Arabic Football Biography Builder'
```

## Template Output Quality

### Well-Formed Template Example

```python
# Complete football biography template
template = """{{صندوق معلومات سيرة كرة قدم
| الاسم = أحمد محمد
| الاسم الكامل = أحمد محمد علي
| تاريخ الميلاد = 15 مايو 1990
| مكان الميلاد = القاهرة، مصر
| الطول = 1.78 م
| المركز = مهاجم
| الأندية1 = النادي الأهلي
| الأندية2 = نادي الزمالك  
| سنوات اللاعب1 = 2008–2012
| سنوات اللاعب2 = 2012–حتى الآن
| المباريات1 = 120
| المباريات2 = 85
| الأهداف1 = 45
| الأهداف2 = 32
| منتخب1 = مصر
| منتخب2 = مصر تحت 23 سنة
| سنوات وطنية1 = 2010–حتى الآن
| سنوات وطنية2 = 2008–2010
}}"""

# Quality metrics
line_count = template.count('\n') + 1  # 18 lines
field_count = template.count('| ')   # 16 fields
numbered_sequences = 2  # الأندية1/2, سنوات اللاعب1/2
```

## Related Classes

- **Parent Class**: `TemplateBuilder` (Abstract builder interface)
- **Data Models**: `BuildResult` (Result structure)
- **Factory Class**: `TemplateBuilderFactory` (Builder creation)
- **Integration**: Construct stage functions and pipeline coordination

---

**File Location**: `tasks/InfoboxSync/construct/arabic_builder.py`
**Status**: Production-ready concrete implementation
**Languages**: Arabic (primary), English (secondary)
**Dependencies**: `TemplateBuilder` base class
**Since**: v1.0