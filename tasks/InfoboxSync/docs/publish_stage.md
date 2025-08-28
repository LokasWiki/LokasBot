# Publish Stage Documentation

## Overview

The Publish stage is responsible for publishing Arabic Wikipedia templates directly to Arabic Wikipedia using the pywikibot library. This stage handles the final step of the InfoboxSync pipeline, managing the integration of localized templates into existing Arabic Wikipedia pages.

## Core Functionality

### Primary Features
- **Direct Wikipedia Publishing**: Publish templates directly to Arabic Wikipedia
- **Smart Template Insertion**: Intelligent placement of templates in existing pages
- **Existing Template Replacement**: Remove old infoboxes and insert new ones
- **Revision Tracking**: Capture revision IDs and metadata
- **Edit Summaries**: Provide descriptive edit summaries in Arabic
- **Safety Mechanisms**: Validation and error handling for publishing operations

### Integration Context
This stage represents the final output of the InfoboxSync pipeline, taking localized templates and making them live on Arabic Wikipedia.

## Architecture

### Core Publishing Functions

#### publish_arabic_template()
```python
def publish_arabic_template(translated_data: Dict[str, Any],
                           arabic_page_title: str,
                           edit_summary: str = "تحديث قالب السيرة الذاتية باستخدام InfoboxSync") -> PublishResult:
    """Publish an Arabic Wikipedia template to the specified page."""
```

#### publish_data()
```python
def publish_data(translated_data: Dict[str, Any],
                arabic_page_title: str,
                edit_summary: str = "تحديث قالب السيرة الذاتية باستخدام InfoboxSync") -> PublishResult:
    """Convenience function to publish translated data to Arabic Wikipedia."""
```

### Result Model

```python
@dataclass
class PublishResult:
    success: bool
    page_title: str
    edit_summary: str
    revision_id: Optional[int] = None
    errors: list = None
    metadata: Dict[str, Any] = None
```

## Publishing Process

### 1. Prerequisites Check
- **pywikibot Installation**: Verify pywikibot is installed and configured
- **Template Validation**: Ensure arabic_template exists and is valid
- **Page Title Validation**: Verify Arabic page title is provided

### 2. Wikipedia Site Connection
```python
# Initialize Arabic Wikipedia site
site = pywikibot.Site('ar', 'wikipedia')
logger.info("Connected to Arabic Wikipedia")
```

### 3. Page Operations
#### Page Existence Verification
```python
page = pywikibot.Page(site, arabic_page_title)
if not page.exists():
    return PublishResult(
        success=False,
        page_title=arabic_page_title,
        edit_summary=edit_summary,
        errors=[f"Page '{arabic_page_title}' does not exist on Arabic Wikipedia"]
    )
```

#### Content Retrieval
```python
current_content = page.text
logger.info(f"Retrieved current page content (length: {len(current_content)})")
```

### 4. Template Insertion Strategy

#### Smart Template Replacement
The stage uses wikitextparser to intelligently handle existing infoboxes:

1. **Parse Current Content**: Use wikitextparser to understand page structure
2. **Identify Existing Templates**: Find existing infobox templates
3. **Template Removal**: Remove old infoboxes carefully
4. **New Template Insertion**: Place new template at page beginning
5. **Content Cleanup**: Maintain readable formatting

#### Template Detection Logic
```python
# Find existing infobox templates
existing_infoboxes = []
for template in parsed_content.templates:
    template_name = template.name.strip()
    if any(infobox_name in template_name.lower() for infobox_name in [
        'صندوق', 'infobox', 'سيرة', 'biography', 'person', 'football'
    ]):
        existing_infoboxes.append(template)
```

#### Content Reconstruction
```python
if existing_infoboxes:
    # Remove existing infoboxes and insert new one
    for infobox in existing_infoboxes:
        infobox.string = ''
    final_content = template_text + '\n\n' + new_content.strip()
else:
    # Add template at the beginning of the page
    final_content = template_text + '\n\n' + current_content.strip()
```

### 5. Page Save Operation
```python
page.save(summary=edit_summary, minor=False)
revision_id = page.latest_revision_id
```

## Safety and Validation Features

### Pre-publishing Validation

#### Data Validation
```python
def validate_publish_data(translated_data: Dict[str, Any], arabic_page_title: str) -> Dict[str, Any]:
    """Validate data before publishing."""
    errors = []
    warnings = []
    
    # Check arabic_template
    if 'arabic_template' not in translated_data:
        errors.append("Missing arabic_template in translated_data")
    
    # Check template format
    elif not translated_data['arabic_template'].startswith('{{'):
        warnings.append("Template doesn't start with '{{'")
    
    # Validate page title
    if not arabic_page_title or len(arabic_page_title) > 255:
        errors.append("Invalid Arabic page title")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }
```

### Error Handling Categories

1. **Configuration Errors**: Missing pywikibot installation or setup
2. **Connection Errors**: Cannot connect to Arabic Wikipedia
3. **Page Access Errors**: Page doesn't exist or access denied
4. **Content Errors**: Invalid template or content processing issues
5. **Save Errors**: Publishing permission issues or edit conflicts

## Integration Features

### Arabic Edit Summaries
The stage provides meaningful Arabic edit summaries:
```python
edit_summary = "تحديث قالب السيرة الذاتية باستخدام InfoboxSync - football_biography"
```

### Revision Tracking
Complete revision metadata capture:
```python
metadata={
    'template_length': len(template_text),
    'site': 'ar.wikipedia.org',
    'published_at': page.editTime().isoformat(),
    'revision_id': revision_id
}
```

## Performance Considerations

### Optimization Strategies
- **Lazy pywikibot Initialization**: Connect only when needed
- **Efficient Content Processing**: Minimal parsing operations
- **Smart Template Detection**: Targeted infobox identification
- **Batch Operations**: Support for multiple page updates

### Rate Limiting
- **Wikipedia API Limits**: Respects editing rate limits
- **Automatic Throttling**: Built-in delays between operations
- **Error Recovery**: Handles rate limit errors gracefully

## Testing and Validation

### Testing Scenarios
1. **Successful Publishing**: Complete template insertion and save
2. **Page Not Found**: Handle non-existent pages gracefully
3. **Permission Errors**: Handle edit restrictions appropriately
4. **Template Conflicts**: Manage multiple infobox scenarios
5. **Network Issues**: Handle connectivity problems

### Quality Assurance
- **Template Format Verification**: Ensure valid wiki syntax
- **Content Integrity**: Verify no content loss during processing
- **Edit Summary Accuracy**: Confirm meaningful Arabic summaries
- **Revision Tracking**: Validate revision ID capture

## API Usage

### Main Entry Points

#### Basic Publishing
```python
from publish.publish import publish_data

result = publish_data(
    translated_data={
        'arabic_template': '{{صندوق سيرة كرة قدم\n| اسم = اللاعب\n}}',
        # ... other data
    },
    arabic_page_title="لاعب كرة قدم",
    edit_summary="تحديث قالب السيرة الذاتية"
)

if result.success:
    print(f"Published successfully! Revision ID: {result.revision_id}")
else:
    print(f"Publishing failed: {result.errors}")
```

#### Advanced Usage with Validation
```python
from publish.publish import validate_publish_data, publish_data

# Validate before publishing
validation = validate_publish_data(translated_data, arabic_page_title)
if not validation['valid']:
    print(f"Validation errors: {validation['errors']}")
    return

# Publish if validation passes
result = publish_data(translated_data, arabic_page_title, edit_summary)
```

## Integration with Pipeline

### Data Flow Integration

**Input → From Wiki Localization Stage:**
```python
localized_data = {
    'arabic_template': localized_template,  # ← Publishing input
    'localization_metadata': {...},
    'page_title': arabic_page_title
}
```

**Output → Final Pipeline Result:**
```python
publish_result = PublishResult(
    success=True,                           # Pipeline success indicator
    page_title=arabic_page_title,
    revision_id=12345678,                   # Wikipedia revision tracking
    metadata={'template_length': 450, 'site': 'ar.wikipedia.org'}
)
```

### Pipeline Completion
This stage marks the successful completion of the InfoboxSync pipeline:
- **Template Live**: Arabic infobox is now published on Arabic Wikipedia
- **Revision History**: Change is recorded in Wikipedia's version control
- **Community Access**: Template is immediately available to Arabic Wikipedia users
- **Audit Trail**: Complete metadata available for monitoring and reporting

## Configuration Requirements

### Pywikibot Setup
```bash
# Install pywikibot
pip install pywikibot

# Generate user configuration
pywikibot generate_user_files

# Configure user-config.py with:
# Arabic Wikipedia bot account credentials
# Appropriate user agent strings
# Edit rate limiting settings
```

### Permission Requirements
- **Bot Account**: Dedicated Arabic Wikipedia bot account
- **Edit Permissions**: Appropriate editing rights on target pages
- **User Agent**: Valid user agent string for API identification

## Monitoring and Reporting

### Success Metrics
- **Publish Success Rate**: Percentage of successful template insertions
- **Average Processing Time**: Time from request to successful save
- **Template Quality Scores**: Validation metrics for published content
- **Revision Tracking**: Complete audit trail of all changes

### Error Monitoring
- **Failure Categories**: Classified error reporting
- **Retry Mechanisms**: Automatic retry for transient failures
- **Alert Integration**: Integration with monitoring systems for critical failures

This publish stage provides a robust, reliable mechanism for integrating Arabic Wikipedia templates into the Arabic Wikipedia ecosystem, with comprehensive validation, error handling, and monitoring capabilities to ensure successful template publication.