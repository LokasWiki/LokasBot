# TemplateMapper Class

## Class Reference

**Namespace**: `tasks.InfoboxSync.map.template_mapper`

**Inherits**: `ABC` (Abstract Base Class)

**Design Pattern**: Strategy Pattern (Template-Level Mapping)

## Overview

Abstract base class for template-specific field mapping strategies. Coordinates the mapping of infobox fields from English to Arabic according to specific template requirements (football biography, person, biography, etc.).

## Constructor

```python
def __init__(self, template_name: str):
    """
    Initialize template mapper.

    Args:
        template_name: Name of the template being mapped
    """
    self.template_name = template_name
    self.field_mappings = self._get_field_mappings()
```

### Attributes

- **`template_name`**: `str` - Template type identifier
- **`field_mappings`**: `Dict[str, Dict[str, Any]]` - Pre-configured field mapping dictionary

## Abstract Methods

### `_get_field_mappings() -> Dict[str, Dict[str, Any]]`

**Must be implemented by subclasses**

Returns field mapping configuration for the specific template type.

```python
@abstractmethod  
def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]:
    """
    Return field mapping configuration.

    Format:
    {
        "english_field_name": {
            "arabic_key": "الاسم_العربي",
            "field_type": "text|number|image|link|numbered|mixed|raw",
            "item_type": "text|number"  # For numbered fields only
        }
    }
    """
```

## Core Methods

### `map_infobox(infobox_data: Dict[str, Any]) -> Dict[str, Any]`

Main infobox mapping orchestration method.

```python
def map_infobox(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map entire infobox using configured field mappers.

    Processing Strategy:
    1. Process numbered fields first (grouping)
    2. Process regular fields
    3. Return mapped data with metadata

    Returns:
        Dict containing 'mapped_fields' and mapping statistics
    """
```

### `get_supported_fields() -> List[str]`

Returns list of supported English field names.

```python
def get_supported_fields(self) -> List[str]:
    """Get list of supported English field names."""
    return list(self.field_mappings.keys())
```

### `get_field_info(english_key: str) -> Dict[str, Any]`

Get mapping information for a specific field.

```python
def get_field_info(self, english_key: str) -> Dict[str, Any]:
    """Get mapping information for English field."""
    normalized_key = english_key.lower().replace(' ', '_').replace('-', '_')
    return self.field_mappings.get(normalized_key, {})
```

## Concrete Implementations

### FootballBiographyMapper

**Location**: `tasks.InfoboxSync.map.template_mapper`

Specialized mapper for football biography infoboxes.

```python
class FootballBiographyMapper(TemplateMapper):
    """Mapper for football biography infobox templates."""

    def __init__(self):
        super().__init__("football_biography")

    def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Get comprehensive football biography field mappings."""
        return {
            # Personal Information
            "name": {"arabic_key": "اسم", "field_type": "text"},
            "fullname": {"arabic_key": "الاسم الكامل", "field_type": "text"},
            "image": {"arabic_key": "صورة", "field_type": "image"},
            "birth_date": {"arabic_key": "تاريخ الميلاد", "field_type": "raw"},
            "birth_place": {"arabic_key": "مكان الميلاد", "field_type": "raw"},
            "height": {"arabic_key": "الطول", "field_type": "number"},

            # Numbered Club Career Fields
            "clubs": {"arabic_key": "الأندية", "field_type": "numbered", "item_type": "raw"},
            "years": {"arabic_key": "سنوات اللاعب", "field_type": "numbered", "item_type": "raw"},
            "caps": {"arabic_key": "المباريات", "field_type": "numbered", "item_type": "number"},
            "goals": {"arabic_key": "الأهداف", "field_type": "numbered", "item_type": "number"},

            # Numbered National Team Fields  
            "nationalteam": {"arabic_key": "المنتخبات الوطنية", "field_type": "numbered", "item_type": "raw"},
            "nationalyears": {"arabic_key": "سنوات وطنية", "field_type": "numbered", "item_type": "raw"},
            "nationalcaps": {"arabic_key": "المباريات الوطنية", "field_type": "numbered", "item_type": "number"},
            "nationalgoals": {"arabic_key": "الأهداف الوطنية", "field_type": "numbered", "item_type": "number"}
        }
```

## Usage Examples

### Basic Template Mapping

```python
from tasks.InfoboxSync.map.template_mapper import FootballBiographyMapper

# Create football biography mapper
football_mapper = FootballBiographyMapper()

# Sample infobox data from parse stage
infobox_data = {
    "name": "Lionel Messi",
    "height": "1.70 m",
    "clubs1": "FC Barcelona",
    "clubs2": "Paris Saint-Germain",
    "years1": "2000–present",
    "caps1": "520",
    "goals1": "474"
}

# Map entire infobox
result = football_mapper.map_infobox(infobox_data)

# Result structure
{
    "mapped_fields": {
        "الاسم": {"value": "Lionel Messi", "type": "text", ...},
        "الطول": {"value": "1.70", "type": "number", ...},
        "الأندية": {"value": ["FC Barcelona", "Paris Saint-Germain"], "type": "numbered", ...},
        "سنوات اللاعب": {"value": ["2000–present"], "type": "numbered", ...},
        "المباريات": {"value": [520], "type": "numbered", "item_type": "number", ...}
    },
    "template_name": "football_biography",
    "total_mapped_fields": 20,
    "original_field_count": 15
}
```

### Factory Integration

```python
from tasks.InfoboxSync.map.template_mapper import TemplateMapperFactory

# Create mapper via factory
mapper = TemplateMapperFactory.create_mapper('football_biography')

# Use same interface
result = mapper.map_infobox(infobox_data)

# Check what fields are supported
supported_fields = mapper.get_supported_fields()
# Returns: ['name', 'fullname', 'image', 'birth_date', ...]
```

### Field-Specific Queries

```python
# Get mapping info for specific field
height_info = mapper.get_field_info('height')
# Returns: {"arabic_key": "الطول", "field_type": "number"}

# Check if field is supported
is_supported = mapper.get_field_info('unknown_field')
# Returns: {} (empty dict means not supported)
```

## Field Mapping Process

### Numbered Field Processing

```python
def map_infobox(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
    # Step 1: Handle numbered fields first
    numbered_field_processors = {}
    for english_key, mapping_config in self.field_mappings.items():
        if mapping_config["field_type"] == "numbered":
            base_key = english_key
            arabic_key = mapping_config["arabic_key"]
            item_type = mapping_config.get("item_type", "text")

            # Create numbered field processor
            numbered_mapper = NumberedFieldMapper(base_key, arabic_key, item_type)
            result = numbered_mapper.map_numbered_fields(infobox_data)

            # Add to results if processing succeeded
            if result:
                numbered_field_processors[base_key] = result

    # Step 2: Process regular fields (skip already processed numbered fields)
    regular_field_results = {}
    for english_key, value in infobox_data.items():
        # Skip if this field was part of numbered processing
        is_numbered_field = any(english_key.startswith(base_key) 
                               for base_key in numbered_field_processors.keys())

        if not is_numbered_field and english_key in self.field_mappings:
            # Map regular field using FieldMapperFactory
            mapping_config = self.field_mappings[english_key]
            field_mapper = FieldMapperFactory.create_mapper(
                english_key, 
                mapping_config["arabic_key"],
                mapping_config["field_type"]
            )
            regular_field_results.update(field_mapper.map_field(str(value)))

    # Step 3: Combine results and return
    all_results = {**numbered_field_processors, **regular_field_results}
    return {
        "mapped_fields": all_results,
        "template_name": self.template_name,
        "total_mapped_fields": len(all_results),
        "original_field_count": len(infobox_data)
    }
```

### Field Type Integration

Template mappers work with field mappers through the factory pattern:

```python
# Integration with FieldMapperFactory
field_mapper = FieldMapperFactory.create_mapper(
    english_key="name",
    arabic_key="الاسم", 
    field_type="text"
)

# Apply field mapping
result = field_mapper.map_field("Cristiano Ronaldo")
# Returns: {"الاسم": {"value": "Cristiano Ronaldo", "type": "text", ...}}
```

## Extension Patterns

### Custom Template Mapper

```python
class CustomMovieMapper(TemplateMapper):
    """Custom mapper for movie infoboxes."""

    def __init__(self):
        super().__init__("movie")

    def _get_field_mappings(self):
        return {
            "title": {"arabic_key": "العنوان", "field_type": "text"},
            "director": {"arabic_key": "المخرج", "field_type": "text"},
            "released": {"arabic_key": "تاريخ الإصدار", "field_type": "raw"},
            "budget": {"arabic_key": "الميزانية", "field_type": "number"},
            "gross": {"arabic_key": "الإيرادات", "field_type": "number"}
        }
```

### Dynamic Field Registration

```python
class DynamicTemplateMapper(TemplateMapper):
    """Mapper that can register fields dynamically."""

    def __init__(self, template_name: str, field_definitions: dict = None):
        super().__init__(template_name)
        self.custom_field_definitions = field_definitions or {}

    def register_field(self, english_key: str, arabic_key: str, field_type: str):
        """Register new field mapping dynamically."""
        self.field_mappings[english_key] = {
            "arabic_key": arabic_key,
            "field_type": field_type
        }

    def _get_field_mappings(self):
        # Combine default mappings with custom ones
        return {**self._get_default_mappings(), **self.custom_field_definitions}
```

## Error Handling and Validation

### Robust Mapping Process

```python
def map_infobox(self, infobox_data: Dict[str, Any]) -> Dict[str, Any]:
    """Error-resilient infobox mapping."""

    try:
        logger.info(f"Mapping infobox for template: {self.template_name}")

        # Validate input
        if not infobox_data:
            logger.warning("Empty infobox data provided")
            return {
                "mapped_fields": {},
                "template_name": self.template_name,
                "total_mapped_fields": 0,
                "original_field_count": 0
            }

        # Process mappings with error isolation
        for english_key in infobox_data.keys():
            try:
                if english_key in self.field_mappings:
                    # Process this field with error handling
                    mapping_config = self.field_mappings[english_key]
                    field_mapper = FieldMapperFactory.create_mapper(
                        english_key,
                        mapping_config["arabic_key"], 
                        mapping_config["field_type"]
                    )

                    result = field_mapper.map_field(str(infobox_data[english_key]))
                    mapped_fields.update(result)

                    logger.debug(f"Mapped field '{english_key}' -> '{mapping_config['arabic_key']}'")

                else:
                    logger.debug(f"No mapping found for field '{english_key}', skipping")

            except Exception as e:
                logger.warning(f"Failed to map field '{english_key}': {e}")
                # Continue with other fields - don't stop entire mapping

        # Return successful mappings
        return {
            "mapped_fields": mapped_fields,
            "template_name": self.template_name,
            "total_mapped_fields": len(mapped_fields),
            "original_field_count": len(infobox_data)
        }

    except Exception as e:
        logger.error(f"Template mapping failed: {e}")
        # Return minimal valid result
        return {
            "mapped_fields": {},
            "template_name": self.template_name,
            "total_mapped_fields": 0,
            "original_field_count": len(infobox_data) if infobox_data else 0
        }
```

## Performance Optimizations

### Mapping Cache Strategies

```python
class CachedTemplateMapper(TemplateMapper):
    """Template mapper with field mapping caching."""

    def __init__(self, template_name: str, max_cache_size: int = 1000):
        super().__init__(template_name)
        self.field_cache = {}
        self.max_cache_size = max_cache_size

    def _get_cached_field_mapper(self, english_key: str, arabic_key: str, field_type: str):
        """Get cached field mapper instance."""
        cache_key = f"{english_key}:{arabic_key}:{field_type}"

        if cache_key not in self.field_cache:
            if len(self.field_cache) < self.max_cache_size:
                mapper = FieldMapperFactory.create_mapper(english_key, arabic_key, field_type)
                self.field_cache[cache_key] = mapper

        return self.field_cache.get(cache_key)
```

### Batch Processing

```python
def bulk_map_infoboxes(self, infobox_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Efficiently map multiple infoboxes in bulk."""
    results = []

    for infobox_data in infobox_list:
        try:
            result = self.map_infobox(infobox_data)
            results.append(result)
        except Exception as e:
            logger.error(f"Bulk mapping failed for infobox: {e}")
            # Add error result to maintain list integrity
            results.append({
                "mapped_fields": {},
                "template_name": self.template_name,
                "total_mapped_fields": 0,
                "original_field_count": len(infobox_data),
                "error": str(e)
            })

    return results
```

## Related Classes

- **Concrete Implementations**: `FootballBiographyMapper`, `GenericTemplateMapper`, `CustomMovieMapper`
- **Field-Level Classes**: `FieldMapper` hierarchy, `FieldMapperFactory`
- **Integration Classes**: Map stage functions, pipeline coordination
- **Factory Class**: `TemplateMapperFactory`

---

**File Location**: `tasks/InfoboxSync/map/template_mapper.py`
**Status**: Abstract base class with multiple concrete implementations
**Design Pattern**: Strategy Pattern with Factory integration
**Dependencies**: `FieldMapperFactory`, `NumberedFieldMapper`, ANDC base mapping classes
**Since**: v1.0