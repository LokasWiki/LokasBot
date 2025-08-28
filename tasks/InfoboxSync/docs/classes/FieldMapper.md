# FieldMapper Class

## Class Reference

**Namespace**: `tasks.InfoboxSync.map.field_mappers`

**Inherits**: `ABC` (Abstract Base Class)

**Design Pattern**: Strategy Pattern (for field types)

## Overview

Abstract base class for field mapping strategies in the Map stage. Handles different types of Wikipedia infobox fields (text, numbers, images, links, etc.) with specialized validation and transformation logic.

## Constructor

```python
def __init__(self, english_key: str, arabic_key: str, field_type: str):
    """
    Initialize field mapper.

    Args:
        english_key: Original English field name from infobox
        arabic_key: Target Arabic field name for mapping
        field_type: Type identifier for mapping strategy
    """
```

### Attributes

- **`english_key`**: `str` - Original English field name
- **`arabic_key`**: `str` - Target Arabic field name
- **`field_type`**: `str` - Field type identifier

## Abstract Methods

### `map_field(value: str) -> Dict[str, Any]`
**Must be implemented by subclasses**

Main mapping method that transforms field values with validation.
```python
@abstractmethod
def map_field(self, value: str) -> Dict[str, Any]:
    """
    Map field value to standardized format with validation.

    Args:
        value: Raw field value from infobox

    Returns:
        Dict containing mapped field data and validation info
    """
    pass
```

## Utility Methods

### `_clean_value(value: str) -> str`
Standardizes field value cleaning.
```python
def _clean_value(self, value: str) -> str:
    """Clean and normalize field value."""
    return value.strip() if value else ""
```

## Concrete Implementations

### TextFieldMapper

**Location**: `tasks.InfoboxSync.map.field_mappers`

Handles plain text fields like names, descriptions, titles.

```python
class TextFieldMapper(FieldMapper):
    """Mapper for text fields."""

    def __init__(self, english_key: str, arabic_key: str):
        super().__init__(english_key, arabic_key, "text")

    def map_field(self, value: str) -> Dict[str, Any]:
        clean_value = self._clean_value(value)

        return {
            self.arabic_key: {
                "value": clean_value,
                "type": "text",
                "original_key": self.english_key,
                "validation": self._validate_text(clean_value)
            }
        }

    def _validate_text(self, value: str) -> Dict[str, Any]:
        return {
            "is_valid": len(value) > 0,
            "length": len(value),
            "has_special_chars": bool(re.search(r'[^\w\s]', value))
        }
```

### NumberFieldMapper

Handles numeric fields with unit extraction and validation.

```python
class NumberFieldMapper(FieldMapper):
    """Mapper for numeric fields."""

    def map_field(self, value: str) -> Dict[str, Any]:
        clean_value = self._clean_value(value)
        numeric_value = self._extract_number(clean_value)

        return {
            self.arabic_key: {
                "value": numeric_value,
                "type": "number",
                "original_key": self.english_key,
                "validation": self._validate_number(clean_value),
                "numeric_value": numeric_value
            }
        }
```

### Usage Examples

#### Basic Field Mapping

```python
from tasks.InfoboxSync.map.field_mappers import TextFieldMapper

# Create text field mapper
name_mapper = TextFieldMapper("name", "الاسم")

# Map field value
result = name_mapper.map_field("Lionel Messi")

# Result
{
    "الاسم": {
        "value": "Lionel Messi",
        "type": "text",
        "original_key": "name",
        "validation": {
            "is_valid": True,
            "length": 12,
            "has_special_chars": False
        }
    }
}
```

#### Factory Integration

```python
from tasks.InfoboxSync.map.field_mappers import FieldMapperFactory

# Factory creates appropriate mapper
text_mapper = FieldMapperFactory.create_mapper("name", "الاسم", "text")
number_mapper = FieldMapperFactory.create_mapper("height", "الطول", "number")

# All mappers have same interface
name_result = text_mapper.map_field("Messi")
height_result = number_mapper.map_field("1.70 m")
```

---

**File Location**: `tasks/InfoboxSync/map/field_mappers.py`
**Status**: Abstract base class with concrete implementations
**Since**: v1.0