# Map Stage Documentation

## Overview

The Map stage is a critical component of the InfoboxSync pipeline responsible for transforming parsed English Wikipedia infobox data into Arabic field mappings. This stage uses a sophisticated multi-layered Strategy Pattern approach, combining template-level and field-level mapping strategies to handle the complex requirements of Wikipedia infobox translation.

## Design Patterns Used

### 1. Strategy Pattern (Multi-layer)
- **Template Layer**: `TemplateMapper` abstract base class with concrete implementations
- **Field Layer**: `FieldMapper` abstract base class with multiple field-type strategies
- **Purpose**: Enable flexible mapping for different template types and field types

### 2. Factory Pattern (Dual Layer)
- **TemplateMapperFactory**: Creates appropriate template mappers
- **FieldMapperFactory**: Creates appropriate field mappers
- **Purpose**: Centralized creation logic for different mapper types

### 3. Composite Pattern
- **NumberedFieldMapper**: Handles numbered sequences (years1, clubs1, etc.)
- **Purpose**: Group related numbered fields into coherent data structures

### 4. Template Method Pattern
- **Base Classes**: `TemplateMapper` and `FieldMapper`
- **Hook Methods**: Field mapping, validation, and error handling
- **Purpose**: Define common workflow with customizable steps

## Multi-layer Architecture

### Layer 1: Template Mapping (High-level Strategy)
**TemplateMapper** handles the overall mapping coordination:
- Manages field mappings for specific template types
- Orchestrates numbered vs. regular field processing
- Provides template-specific business logic

### Layer 2: Field Mapping (Low-level Strategy)
**FieldMapper** handles individual field transformations:
- Type-specific value processing
- Field validation and cleaning
- Wiki markup handling

## Core Components

### Template Mapper Hierarchy

#### TemplateMapper (Abstract Base Class)
```python
class TemplateMapper(ABC):
    def __init__(self, template_name: str)
    @_abstractmethod
    def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]
    def map_infobox(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]
    def get_supported_fields(self) -> List[str]
    def get_field_info(self, english_key: str) -> Dict[str, Any]
```

**Field Mapping Configuration Format:**
```python
field_mappings = {
    "english_field_name": {
        "arabic_key": "الاسم_العربي",
        "field_type": "text|number|image|link|mixed|numbered|raw",
        "item_type": "text|number"  # For numbered fields only
    }
}
```

#### Concrete Template Mappers

**FootballBiographyMapper**
- Specialized for football biography infoboxes
- Handles personal info, club career, national teams, managerial roles
- Supports numbered field grouping (years1/clubs1/caps1 → سنوات/أندية/مباريات)

**GenericTemplateMapper**
- Fallback for templates without specific mappings
- All fields mapped as generic text/raw types

### Field Mapper Hierarchy

#### FieldMapper (Abstract Base Class)
```python
class FieldMapper(ABC):
    def __init__(self, english_key: str, arabic_key: str, field_type: str)
    @abstractmethod
    def map_field(self, value: str) -> Dict[str, Any]
    def _clean_value(self, value: str) -> str
```

#### Field Type Strategies

**TextFieldMapper**
- **Purpose**: Names, descriptions, plain text fields
- **Validation**: Length checks, special character detection
- **Output**: Clean text with metadata

**NumberFieldMapper**
- **Purpose**: Ages, years, counts, statistics
- **Features**: Numeric extraction, unit preservation
- **Validation**: Numeric value extraction and validation

**ImageFieldMapper**
- **Purpose**: Player photos, flags, media files
- **Features**: Wiki image syntax parsing (`[[File:img.jpg|caption]]`)
- **Validation**: Filename and caption extraction

**LinkFieldMapper**
- **Purpose**: Websites, cross-references, external links
- **Features**: Internal/external link detection
- **Validation**: URL format validation, display text extraction

**MixedFieldMapper**
- **Purpose**: Complex fields with multiple data types
- **Features**: Content type analysis (text + links + images)
- **Validation**: Component identification

**NumberedFieldMapper**
- **Purpose**: Career sequences (years1, clubs1, caps1...)
- **Features**: Automatic grouping and sorting by sequence number
- **Output**: Array of values in correct order

**RawFieldMapper**
- **Purpose**: Pass-through fields requiring no processing
- **Features**: Direct value preservation
- **Use Case**: Complex wiki markup, dates, locations

## Mapping Process Flow

### 1. Template Mapper Initialization
- Load template-specific field mappings
- Identify numbered field sequences
- Prepare field type mappings

### 2. Numbered Field Processing
```python
# Process numbered fields first (years1, clubs1, caps1...)
for base_key in numbered_mappings:
    numbered_mapper = NumberedFieldMapper(base_key, arabic_key, item_type)
    mapped_group = numbered_mapper.map_numbered_fields(infobox_data)
    result[arabic_key] = {
        "value": [val1, val2, val3...],  # Array of sequenced values
        "type": "numbered",
        "item_type": "text|number",
        "count": 15
    }
```

### 3. Regular Field Processing
```python
# Process individual fields
for english_key, value in infobox_data.items():
    if mapping_config = field_mappings.get(normalized_key):
        mapper = FieldMapperFactory.create_mapper(
            english_key, arabic_key, mapping_config["field_type"]
        )
        result[arabic_key] = mapper.map_field(value)
```

## Factory Pattern Implementation

### TemplateMapperFactory
```python
@staticmethod
def create_mapper(template_type: str) -> TemplateMapper:
    if template_type == 'football_biography':
        return FootballBiographyMapper()
    elif template_type == 'person':
        return GenericTemplateMapper("person")
    else:
        return GenericTemplateMapper(template_type)
```

### FieldMapperFactory
```python
@staticmethod
def create_mapper(english_key: str, arabic_key: str, field_type: str) -> FieldMapper:
    if field_type == "text":
        return TextFieldMapper(english_key, arabic_key)
    elif field_type == "number":
        return NumberFieldMapper(english_key, arabic_key)
    # ... more field types
```

## API Usage

### Main Entry Point

#### map_data()
```python
def map_data(parsed_data: dict,
             template_type: str = 'football_biography') -> dict:
    """
    Map parsed infobox data to Arabic field mappings.

    Args:
        parsed_data (dict): Parsed data from parse stage
        template_type (str): Template type for mapping strategy

    Returns:
        dict: Mapped data with Arabic field names
    """
```

**Input Format:**
```python
parsed_data = {
    'title': 'Lionel Messi',
    'infobox': {
        'name': 'Lionel Messi',
        'height': '1.70 m',
        'years1': '2000–2004',
        'clubs1': 'Barcelona B',
        'caps1': '35',
        'image': '[[File:Messi_vs_Nigeria.jpg|Messi playing]]'
    },
    'categories': ['Football players'],
    'links': ['Argentina national football team']
}
```

**Output Format:**
```python
{
    'page_title': 'Lionel Messi',
    'template_type': 'football_biography',
    'arabic_fields': {
        'اسم': {
            'value': 'Lionel Messi',
            'type': 'text',
            'validation': {'is_valid': True, 'length': 12}
        },
        'الطول': {
            'value': 1.70,
            'type': 'number',
            'validation': {'is_valid': True, 'numeric_value': 1.7}
        },
        'سنوات': {
            'value': ['2000–2004', '2004–present'],
            'type': 'numbered',
            'count': 2
        },
        'أندية': {
            'value': ['Barcelona B', 'FC Barcelona'],
            'type': 'numbered',
            'count': 2
        },
        'صورة': {
            'value': 'Messi_vs_Nigeria.jpg',
            'type': 'image',
            'validation': {'is_valid': True, 'has_caption': True}
        }
    },
    'metadata': {
        'categories': ['Football players'],
        'links': ['Argentina national football team'],
        'template_name': 'football_biography',
        'total_mapped_fields': 5,
        'original_field_count': 8
    }
}
```

### Field Type Examples

**Text Field Mapping:**
```python
{
    'الاسم': {
        'value': 'Lionel Messi',
        'type': 'text',
        'original_key': 'name',
        'validation': {
            'is_valid': True,
            'length': 12,
            'has_special_chars': False
        }
    }
}
```

**Number Field Mapping:**
```python
{
    'الطول': {
        'value': 1.70,
        'type': 'number',
        'original_key': 'height',
        'validation': {
            'is_valid': True,
            'numeric_value': 1.7,
            'has_units': True
        }
    }
}
```

**Numbered Field Mapping:**
```python
{
    'سنوات': {
        'value': ['2000–2004', '2004–present'],
        'type': 'numbered',
        'item_type': 'raw',
        'count': 2,
        'original_keys': ['years1', 'years2']
    }
}
```

**Image Field Mapping:**
```python
{
    'صورة': {
        'value': 'Messi_vs_Nigeria.jpg',
        'type': 'image',
        'original_key': 'image',
        'validation': {
            'is_valid': True,
            'has_caption': True,
            'filename': 'Messi_vs_Nigeria.jpg'
        },
        'image_info': {
            'filename': 'Messi_vs_Nigeria.jpg',
            'caption': 'Messi playing'
        }
    }
}
```

## Football Biography Field Mappings

### Personal Information Fields
| English Key | Arabic Key | Field Type |
|------------|-----------|-----------|
| name | اسم | text |
| fullname | الاسم الكامل | text |
| image | صورة | image |
| caption | تعليق الصورة | raw |
| birth_date | تاريخ الولادة | raw |
| birth_place | مكان الولادة | raw |
| height | الطول | number |
| position | المركز | raw |

### Club Career Fields (Numbered)
| English Key | Arabic Key | Field Type |
|------------|-----------|-----------|
| clubs | أندية | numbered |
| years | سنوات | numbered |
| caps | مباريات | numbered (number) |
| goals | أهداف | numbered (number) |

### National Team Fields (Numbered)
| English Key | Arabic Key | Field Type |
|------------|-----------|-----------|
| nationalteam | منتخب_وطني | numbered |
| nationalyears | سنوات_وطنية | numbered |
| nationalcaps | مباريات_وطنية | numbered (number) |
| nationalgoals | أهداف_وطنية | numbered (number) |

### Managerial Career Fields (Numbered)
| English Key | Arabic Key | Field Type |
|------------|-----------|-----------|
| managerclubs | أندية_مدرب | numbered |
| manageryears | سنوات_مدرب | numbered |

### Honors and Statistics
| English Key | Arabic Key | Field Type |
|------------|-----------|-----------|
| medaltemplates | ميداليات | mixed |
| totalcaps | مجموع_مباريات | number |
| totalgoals | إجمالي الأهداف | number |

## Advanced Features

### Numbered Field Processing
Wikipedia infoboxes often use numbered fields to represent career progression:
```
years1 = 2000–2004 | clubs1 = Barcelona B | caps1 = 35 | goals1 = 5
years2 = 2004–present | clubs2 = FC Barcelona | caps2 = 520 | goals2 = 474
```

**Mapped to Arabic sequenced arrays:**
```python
{
    "سنوات": ["2000–2004", "2004–present"],
    "أندية": ["Barcelona B", "FC Barcelona"],
    "مباريات": [35, 520],
    "أهداف": [5, 474]
}
```

### Validation and Error Handling
Each field type includes comprehensive validation:
- **Text Fields**: Length, special character presence
- **Number Fields**: Numeric value extraction, unit detection
- **Image Fields**: Filename parsing, caption detection
- **Link Fields**: URL validation, internal/external distinction
- **Mixed Fields**: Component type detection

### Key Normalization
Field keys are normalized for flexible matching:
```python
# Original: "birth_date"
# Normalized: "birth_date"
# Alternative: "birth-date" → "birth_date"
# Alternative: "Birth Date" → "birth_date"
```

## Integration with Pipeline

### Data Flow Connection Points

**Input → From Parse Stage:**
```python
parsed_data = {
    'title': 'Page Title',
    'infobox': parsed_infobox_dict,
    'categories': category_list,
    'links': link_list
}
```

**Output → To Translate Stage:**
```python
mapped_data = {
    'page_title': title,
    'aric_fields': arabic_mapped_dict,  # ← This becomes translation input
    'metadata': mapping_metadata
}
```

### Error Propagation and Recovery
- **Missing Mappings**: Logged as warning, field skipped
- **Invalid Field Types**: Fallback to text mapping with warning
- **Parse Errors**: Individual field failures don't stop entire mapping
- **Template Failures**: Return empty mapping with error metadata

## Performance Considerations

### Optimization Strategies
1. **Mapping Compilation**: Field mappings pre-compiled at initialization
2. **Batch Processing**: Sequence processing for numbered fields
3. **Validation Caching**: Field validation results cached
4. **Memory Efficiency**: On-demand field mapper creation

### Scalability Features
- **Template Expansion**: New template types easily added via factory
- **Field Type Extension**: New field mappers supportable via factory
- **Configuration-Driven**: Mappings defined in code, easily modified

## Testing and Validation

### Test Coverage Areas
- Field type detection and mapping accuracy
- Numbered field sequence and ordering
- Validation logic and error handling
- Template mapper factory integration
- Performance with large infobox datasets

### Quality Assurance
- **Mapping Accuracy**: Field-by-field validation against expected outputs
- **Type Consistency**: Validation that field types match expected patterns
- **Sequence Integrity**: Numbered field grouping correctness
- **Metadata Accuracy**: Mapping statistics and error reporting

## Extension Points

### Adding New Template Types
```python
class NewTemplateMapper(TemplateMapper):
    def _get_field_mappings(self):
        return {
            "field1": {"arabic_key": "الحقل_الأول", "field_type": "text"},
            "field2": {"arabic_key": "الحقل_الثاني", "field_type": "number"}
        }
```

### Adding New Field Types
```python
class CustomFieldMapper(FieldMapper):
    def map_field(self, value: str) -> Dict[str, Any]:
        # Custom mapping logic
        pass
```

This comprehensive mapping stage provides a robust, extensible foundation for transforming English Wikipedia infoboxes into structurally equivalent Arabic field representations, supporting the complex requirements of cross-language information synchronization.