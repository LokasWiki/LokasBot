# Wiki Localization Stage Documentation

## Overview

The Wiki Localization stage is a post-processing component that transforms Arabic templates containing English wiki syntax into properly localized Arabic Wikipedia content. It handles the conversion of English internal links, template names, and wiki markup to their Arabic equivalents, ensuring seamless integration with Arabic Wikipedia standards.

## Core Functionality

### Primary Features
- **Link Localization**: Convert English internal links to Arabic equivalents
- **Template Localization**: Translate template names to Arabic
- **Fallback Mechanisms**: Handle missing Arabic equivalents with "واو" templates
- **Smart Detection**: Identify and process different types of wiki markup
- **Error Resilience**: Continue processing even with partial failures

### Integration Point
This stage fits between the Construct stage (template building) and Publish stage (Wikipedia publishing), serving as the final content optimization step.

## Architecture

### Main Integration Function

```python
def process_construct_to_publish(
    construct_result: Dict[str, Any],
    enable_local_link_replacement: bool = True,
    enable_template_localization: bool = True
) -> LocalizationProcessingResult:
    """Process construct output through localization for publishing."""
```

### Key Components

#### LocalizationProcessingResult
```python
@dataclass
class LocalizationProcessingResult:
    success: bool
    localized_data: Dict[str, Any]
    localization_info: WikiLocalizeResult
    processing_time: float
    errors: list
```

#### WikiLocalizeResult
```python
@dataclass
class WikiLocalizeResult:
    localized_content: str
    original_links_replaced: int
    templates_localized: int
    waou_templates_inserted: int
    errors: List[str]
```

## Link Localization Process

### Internal Link Conversion
- **Input**: `[[Manchester United|Manchester United F.C.]]`
- **Output**: `[[مانشستر يونايتد|مانشستر يونايتد]]`

### Processing Steps
1. **Extract Link Components**: Parse link target and display text
2. **Find Arabic Equivalent**: Query Arabic Wikipedia for link target
3. **Translate Display Text**: Convert display text to Arabic
4. **Reconstruct Link**: Build properly formatted Arabic link

### Template Localization
- **Input**: `{{Birth date|1990|5|15}}`
- **Output**: `{{تاريخ الميلاد|1990|5|15}}`

## Fallback Mechanisms

### "واو" Template System
For wiki links without direct Arabic equivalents, the system inserts "واو" templates:

- **Purpose**: Provide Arabic Wikipedia community with translation opportunities
- **Implementation**: `{{واو|English Title}}`
- **Benefit**: Creates systematic path for community-driven localization

## Error Handling and Resilience

### Processing Strategies
- **Individual Link Failures**: Don't stop entire localization process
- **Partial Success Tracking**: Detailed metrics on successful vs failed operations
- **Graceful Degradation**: Continue with partial localization if complete processing fails

### Error Categories
1. **Link Resolution Errors**: Cannot find Arabic equivalent for link target
2. **Translation Service Errors**: Issues translating display text
3. **Template Recognition Errors**: Cannot identify template names to localize
4. **Wiki Syntax Errors**: Malformed wiki markup

## Performance Considerations

### Optimization Features
- **Batch Processing**: Process multiple links efficiently
- **Caching**: Cache Arabic link equivalents for repeated links
- **Selective Processing**: Allow disabling link or template localization
- **Timout Handling**: Prevent hanging on slow wiki API calls

### Performance Metrics
The stage tracks processing time and provides detailed statistics:
```python
{
    'total_links_processed': 15,
    'links_successfully_replaced': 12,
    'waou_fallback_templates': 3,
    'templates_localized': 8,
    'success_rate': 85.0
}
```

## Configuration and Control

### Processing Options
```python
# Enable/disable specific features
enable_local_link_replacement: bool = True
enable_template_localization: bool = True
```

### Extensibility Points
- **Custom Link Resolvers**: Add custom Arabic link lookup mechanisms
- **Template Translation Tables**: Expand template name mappings
- **Localization Rules**: Customize localization behavior per wiki

## Quality Assurance

### Validation Features
- **Link Integrity**: Ensure all processed links maintain valid wiki syntax
- **Template Consistency**: Verify template names follow Arabic Wikipedia conventions
- **Content Preservation**: Ensure no content is lost during localization

### Monitoring and Reporting
- **Detailed Logging**: Comprehensive logs of all localization operations
- **Metrics Collection**: Performance and success statistics
- **Error Categorization**: Classified error reporting for debugging

## Integration with Pipeline

### Input/Output Flow

**Input (from Construct Stage):**
```python
{
    'arabic_template': '{{صندوق سيرة كرة قدم\n| اسم = Player\n| أندية1 = [[Manchester United]]\n}}',
    'template_type': 'football_biography',
    ...
}
```

**Output (to Publish Stage):**
```python
{
    'arabic_template': '{{صندوق سيرة كرة قدم\n| اسم = Player\n| أندية1 = [[مانشستر يونايتد]]\n}}',
    'localization_metadata': {
        'links_replaced': 1,
        'templates_localized': 0,
        'waou_templates_inserted': 0,
        'localization_errors': []
    },
    ...
}
```

### Pipeline Benefits
- **Content Optimization**: Maximize compatibility with Arabic Wikipedia
- **Community Integration**: "واو" template system enables community participation
- **Error Isolation**: Localization failures don't prevent publishing
- **Quality Enhancement**: Improved user experience with localized content

## Usage Examples

### Basic Usage
```python
from tasks.InfoboxSync.wikilocalize.integrator import process_construct_to_publish

# Localize construct output
result = process_construct_to_publish(
    construct_result=constructed_data,
    enable_local_link_replacement=True,
    enable_template_localization=True
)

if result.success:
    # Use localized data for publishing
    localized_template = result.localized_data['arabic_template']
    # Continue to publish stage...
```

### Selective Processing
```python
# Only replace links, skip template localization
result = process_construct_to_publish(
    construct_result=constructed_data,
    enable_local_link_replacement=True,    # ✓ Enabled
    enable_template_localization=False     # ✗ Disabled
)
```

### Statistics Analysis
```python
# Get detailed localization statistics
stats = get_localization_statistics(result.localization_info)
print(f"Links processed: {stats['total_links_processed']}")
print(f"Success rate: {stats['success_rate']}%")
```

## Future Enhancements

### Planned Improvements
- **Machine Learning**: AI-powered link equivalent discovery
- **Community Database**: Crowdsourced Arabic link mappings
- **Advanced Fallbacks**: Improved "واو" template system
- **Template Recognition**: Enhanced template name detection algorithms

This wiki localization stage ensures that Arabic Wikipedia templates are fully compatible with Arabic Wikipedia standards and conventions, providing a high-quality, localized user experience while maintaining robust error handling and extensive monitoring capabilities.