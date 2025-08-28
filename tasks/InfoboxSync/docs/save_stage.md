# Save Stage Documentation

## Overview

The Save stage provides data persistence functionality for the InfoboxSync pipeline, enabling processed data to be stored as JSON files for later analysis, backup, or reuse. This stage ensures that the complete pipeline results are preserved in a structured, accessible format.

## Core Functionality

### Primary Features
- **JSON Data Persistence**: Store complete pipeline results as JSON files
- **Structured Data**: Preserve the entire processing pipeline data
- **File Organization**: Intelligent filename generation based on content
- **Unicode Support**: Proper handling of Arabic text encoding
- **Error Handling**: Robust error handling for file I/O operations

### Integration Context
The Save stage can be used at any point in the pipeline or as the final stage to ensure all processed data is preserved for future reference, analysis, or debugging.

## Architecture

### Core Save Function

```python
def save_data(translated_data: dict, output_dir: str = 'output') -> str:
    """
    Save the translated data to a file.

    Args:
        translated_data (dict): The translated data from the translate stage.
        output_dir (str): Directory to save the data (default: 'output').

    Returns:
        str: Path to the saved file.
    """
```

### File Naming Strategy

#### Intelligent Filename Generation
```python
# Generate filename based on page title
title = translated_data.get('page_title', 'unknown')
filename = f"{title.replace(' ', '_').lower()}.json"
filepath = os.path.join(output_dir, filename)
```

**Examples:**
- Input Title: `"Lionel Messi"`
- Generated Filename: `"lionel_messi.json"`
- Input Title: `"محمد بن سلمان"`
- Generated Filename: `"محمد_بن_سلمان.json"`

## Data Structure Preservation

### Complete Pipeline Data
The Save stage preserves the entire processed data structure:

```python
saved_data = {
    # Original page information
    'page_title': 'Lionel Messi',
    'arabic_title': 'ليونيل ميسي',
    'raw_content': '...original wikitext...',
    
    # Parsed data
    'infobox': {...},
    'categories': [...],
    'links': [...],
    
    # Mapped data
    'arabic_fields': {
        'الاسم': {'value': 'ليونيل ميسي', 'type': 'text'},
        'الطول': {'value': 1.70, 'type': 'number'}
    },
    'template_type': 'football_biography',
    
    # Translated data
    'translated_fields': {
        'الاسم': {'value': 'ليونيل ميسي', 'translated_value': 'ليونيل ميسي'},
        'الطول': {'value': 1.70, 'translated_value': 1.70}
    },
    'translation_metadata': {
        'service': 'Google Gemini AI',
        'target_language': 'ar',
        'total_fields': 15,
        'translated_fields': 12
    },
    
    # Constructed template
    'arabic_template': '{{صندوق سيرة كرة قدم\n| الاسم = ليونيل ميسي\n...}}',
    'construct_metadata': {
        'template_type': 'football_biography',
        'field_count': 12,
        'success': True
    },
    
    # Localization information
    'localization_metadata': {
        'links_replaced': 3,
        'templates_localized': 1,
        'waou_templates_inserted': 0
    },
    
    # Publishing result (if pipeline completed)
    'publish_metadata': {
        'page_title': 'ليونيل ميسي',
        'revision_id': 12345678,
        'published_at': '2024-01-15T10:30:00Z',
        'publish_success': True
    }
}
```

## File Management

### Directory Management
```python
# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
logger.info(f"Ensuring output directory exists: {output_dir}")
```

### File Writing Process
```python
# Save data as JSON with proper encoding
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(translated_data, f, indent=2, ensure_ascii=False)

logger.info(f"Successfully saved data to: {filepath}")
return filepath
```

## Data Format Features

### JSON Serialization Options
- **Unicode Preservation**: `ensure_ascii=False` maintains Arabic characters
- **Pretty Printing**: `indent=2` for human-readable formatting
- **Field Preservation**: All pipeline metadata and processing results maintained

### Size and Performance
- **Typical File Sizes**: 10-50KB for football player biographies
- **Structure Depth**: Maintains full nested data structure hierarchy
- **Metadata Richness**: Complete audit trail and processing information

## API Usage

### Basic Usage

#### Save Pipeline Data
```python
from save.save import save_data

# After any pipeline stage
result = save_data(
    translated_data=pipeline_result,
    output_dir='output/football_biographies'
)

print(f"Data saved to: {result}")
# Output: Data saved to: output/football_biographies/lionel_messi.json
```

### Intermediate Pipeline Checkpoint
```python
from save.save import save_data

def checkpoint_pipeline(current_data: dict, checkpoint_path: str) -> dict:
    """Save intermediate pipeline state for recovery."""
    
    # Add checkpoint metadata
    checkpoint_data = current_data.copy()
    checkpoint_data['checkpoint_metadata'] = {
        'checkpoint_time': datetime.now().isoformat(),
        'checkpoint_stage': 'intermediate',
        'pipeline_version': '1.0'
    }
    
    # Save checkpoint
    checkpoint_file = save_data(checkpoint_data, checkpoint_path)
    
    return {
        'original_data': current_data,
        'checkpoint_file': checkpoint_file,
        'can_recover': True
    }
```

### Batch Processing
```python
def save_batch_results(batch_results: List[dict], output_dir: str = 'output/batch') -> List[str]:
    """Save multiple pipeline results."""
    
    saved_files = []
    for i, result in enumerate(batch_results):
        batch_result = result.copy()
        batch_result['batch_metadata'] = {
            'batch_index': i,
            'total_in_batch': len(batch_results),
            'batch_id': f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        filepath = save_data(batch_result, output_dir)
        saved_files.append(filepath)
    
    return saved_files
```

## Error Handling and Resilience

### File I/O Error Handling
```python
try:
    os.makedirs(output_dir, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Successfully saved data to: {filepath}")
    return filepath
    
except FileNotFoundError as e:
    logger.error(f"Directory creation failed: {e}")
    raise
except PermissionError as e:
    logger.error(f"File write permission denied: {e}")
    raise
except json.JSONEncodeError as e:
    logger.error(f"JSON serialization failed: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error saving data: {e}")
    raise
```

### Error Scenarios Handled
1. **Directory Creation Failures**: Insufficient permissions or disk space
2. **File Write Errors**: Permission issues or disk full conditions
3. **JSON Serialization Errors**: Non-serializable data types
4. **Encoding Issues**: Unicode encoding problems
5. **Path Issues**: Invalid characters in filenames

## Integration with Pipeline

### Data Flow Connection Points

**Input → From Any Pipeline Stage:**
```python
# After Translate stage
translated_data = translate_stage_output
save_path = save_data(translated_data, 'output/translations')

# After Construct stage  
constructed_data = construct_stage_output
save_data(constructed_data, 'output/templates')

# After full pipeline completion
final_result = completed_pipeline_data
save_data(final_result, 'output/completed')
```

**Output → Filesystem:**
```
output/
├── completed/
│   └── lionel_messi.json
├── translations/
│   └── lionel_messi.json
└── templates/
    └── lionel_messi.json
```

### Pipeline Flexibility
- **Checkpoint Capability**: Save intermediate states for pipeline recovery
- **Backup Functionality**: Preserve data before risky operations
- **Audit Trail**: Complete record of all processing steps
- **Debug Support**: Saved data enables detailed pipeline analysis

## File Organization Strategies

### Directory Structure Options

#### By Template Type
```
output/
├── football_biography/
│   ├── lionel_messi.json
│   ├── cristiano_ronaldo.json
│   └── neymar.json
├── person/
│   ├── barack_obama.json
│   └── nelson_mandela.json
└── country/
    └── egypt.json
```

#### By Processing Date
```
output/
├── 2024-01-15/
│   ├── batch_001_part_001.json
│   └── batch_001_part_002.json
├── 2024-01-16/
│   ├── checkpoint_messi.json
│   └── checkpoint_ronaldo.json
```

#### By Pipeline Status
```
output/
├── completed/
├── intermediate/
└── failed/
```

## Analysis and Monitoring

### Data Inspection Utilities
```python
def inspect_saved_data(filepath: str) -> Dict[str, Any]:
    """Inspect saved pipeline data."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            'file_size': os.path.getsize(filepath),
            'has_translation': 'translated_fields' in data,
            'has_template': 'arabic_template' in data,
            'has_publish_metadata': 'publish_metadata' in data,
            'pipeline_stages_completed': _analyze_pipeline_completion(data),
            'error_summary': _extract_errors(data)
        }
    except Exception as e:
        return {'error': str(e)}
```

### Pipeline Analytics
```python
def analyze_batch_results(directory: str) -> Dict[str, Any]:
    """Analyze a directory of saved pipeline results."""
    files = glob.glob(os.path.join(directory, '*.json'))
    stats = {
        'total_files': len(files),
        'successful_translations': 0,
        'successful_publishes': 0,
        'average_file_size': 0,
        'template_types': Counter(),
        'error_rate': 0
    }
    
    total_size = 0
    total_errors = 0
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            total_size += len(str(data))
            
            if 'translated_fields' in data and data.get('translation_metadata', {}).get('success'):
                stats['successful_translations'] += 1
            
            if data.get('publish_metadata', {}).get('publish_success'):
                stats['successful_publishes'] += 1
            
            template_type = data.get('template_type', 'unknown')
            stats['template_types'][template_type] += 1
            
        except Exception as e:
            total_errors += 1
            continue
    
    if files:
        stats['average_file_size'] = total_size / len(files)
        stats['error_rate'] = total_errors / len(files)
    
    return stats
```

## Best Practices

### Storage Strategies
1. **Regular Backups**: Save critical pipeline results to multiple locations
2. **Version Control**: Consider git for pipeline result versioning
3. **Compression**: Use gzip for large result sets if needed
4. **Encryption**: Encrypt sensitive data if required

### Performance Optimization
1. **Batch Processing**: Write multiple files efficiently
2. **Memory Management**: Handle large datasets appropriately
3. **File Locking**: Prevent concurrent write issues
4. **Cleanup**: Remove temporary files after processing

### Data Retention Policies
1. **Time-based Archiving**: Archive old results automatically
2. **Size Management**: Implement storage quotas
3. **Importance Classification**: Keep crucial results longer
4. **Compression**: Archive less frequently accessed data

This save stage ensures the complete preservation of all InfoboxSync pipeline processing results, providing a robust data persistence layer that supports debugging, analysis, recovery, and future reuse of processed Wikipedia infobox data.