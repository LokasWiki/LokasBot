# Translate Stage Documentation

## Overview

The Translate stage is responsible for translating English Wikipedia infobox data to Arabic using advanced AI translation services. This stage implements a sophisticated Strategy Pattern architecture that supports multiple translation services while providing single-request optimization for cost efficiency and performance.

## Design Patterns Used

### 1. Strategy Pattern
- **Context**: `translate_data()` function
- **Abstract Strategy**: `TranslationService` (abstract base class)
- **Concrete Strategies**:
  - `GeminiTranslator` - Google Gemini AI implementation
  - Extensible for additional services (OpenAI, DeepL, etc.)
- **Purpose**: Enable different translation services and methodologies

### 2. Factory Pattern
- **Factory Class**: `TranslationServiceFactory`
- **Purpose**: Centralized creation and registration of translation services
- **Features**: Service discovery, automatic registration, extensibility

### 3. Template Method Pattern
- **Base Class**: `TranslationService`
- **Hook Methods**: Service-specific implementation methods
- **Purpose**: Define common translation workflow with customizable steps

## Core Components

### Strategy Interface (TranslationService)

```python
class TranslationService(ABC):
    def __init__(self, source_lang: str = 'en', target_lang: str = 'ar')
    @abstractmethod
    def translate_text(self, text: str, **kwargs) -> TranslationResult
    @abstractmethod
    def translate_field(self, field_name: str, field_value: Any, **kwargs) -> TranslationResult
    @abstractmethod
    def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]
    @abstractmethod
    def is_available(self) -> bool
    @abstractmethod
    def get_service_name(self) -> str
```

### Translation Result Model

```python
@dataclass
class TranslationResult:
    translated_text: str
    original_text: str
    confidence: float
    metadata: Optional[Dict[str, Any]]
```

### Factory Implementation

#### TranslationServiceFactory
```python
@classmethod
def register_service(cls, service_name: str, service_class)
@classmethod
def create_service(cls, service_name: str, **kwargs) -> TranslationService
@classmethod
def get_available_services(cls) -> List[str]
```

## Gemini AI Implementation

### Single-Request Optimization
The key innovation of the translation stage is **Single-Request Translation**:

**Traditional Approach**: Multiple API calls (1 per field) → High cost, slow, context loss
**InfoboxSync Approach**: Single API call for ALL fields → Low cost, fast, context preservation

### Implementation Details

#### Prompt Engineering
- **Template-Based Prompts**: External `prompt_template.txt` file for easy customization
- **Content-Type Awareness**: Different translation rules for different data types
- **Structured Output**: Index-based field identification and mapping

#### Field Type Handling
```python
# Smart field type processing
if field_type == 'numbered':
    # Translate each item in the array
    for i, item in enumerate(value):
        fields_list.append(f"[{idx}_{i}]: {item}")
        field_mapping[f"{idx}_{i}"] = (arabic_key, i)
elif field_type in ['number', 'link', 'image']:
    # Preserve as-is (don't translate)
    field_mapping[str(idx)] = (arabic_key, None)
else:
    # Standard text translation
    fields_list.append(f"[{idx}]: {value}")
```

### Advanced Prompt Template

The translation stage uses a comprehensive prompt template that includes:

1. **Content Type Rules**: Specific instructions for plain text, links, templates, numbers
2. **Football Terminology**: Domain-specific translations for sports terms
3. **Wiki Syntax Preservation**: Rules for maintaining Wikipedia markup
4. **Quality Assurance**: Instructions for maintaining meaning and context

### Content Type Intelligence

#### Plain Text Translation
- **Natural Translation**: Descriptive and contextual
- **Examples**:
  - `"Professional footballer"` → `"لاعب كرة قدم محترف"`
  - `"American actor and comedian"` → `"ممثل وكوميدي أمريكي"`

#### Link Preservation
- **URL Integrity**: Keep exact URL format unchanged
- **Display Text Translation**: Translate only human-readable text
- **Examples**:
  - `[http://www.example.com Football website]` → `[http://www.example.com موقع كرة قدم]`

#### Wiki Link Handling
- **Link Target Preservation**: Never modify link targets (`[[Real_Madrid|R.Madrid]]`)
- **Display Text Translation**: Translate only display part (`[[Real_Madrid|ريال مدريد]]`)

#### Template Processing
- **Template Name Preservation**: Never translate template names (`{{birth date}}`)
- **Parameter Translation**: Translate only human-readable parameters
- **Structural Integrity**: Maintain template syntax and structure

#### Number and Measure Handling
- **Value Preservation**: Keep all numerical values unchanged
- **Unit Translation**: Translate only units and suffixes
- **Examples**:
  - `1.84 m` → `1.84 متر`
  - `25 years old` → `25 عامًا`

### Configuration Management

#### TranslationConfig Class
```python
DEFAULT_CONFIG = {
    'gemini': {
        'model': 'gemini/gemini-2.0-flash',
        'temperature': 0.3,
        'api_key_env_vars': ['GEMINI_API_KEY', 'GOOGLE_AI_API_KEY']
    },
    'default_service': 'gemini',
    'fallback_service': None,
    'enable_caching': True,
    'cache_max_size': 1000,
    'request_timeout': 30,
    'retry_attempts': 3,
    'retry_delay': 1.0
}
```

#### Environment Variable Integration
```bash
export GEMINI_API_KEY="your-google-ai-api-key"
export GOOGLE_AI_API_KEY="your-google-ai-api-key"
export TRANSLATION_DEFAULT_SERVICE="gemini"
export TRANSLATION_ENABLE_CACHING="true"
```

## API Usage

### Main Entry Points

#### translate_data()
```python
def translate_data(mapped_data: dict, target_lang: str = 'ar',
                  service_name: Optional[str] = None) -> dict:
    """
    Translate mapped data using AI translation services.

    Args:
        mapped_data (dict): Mapped data from map stage
        target_lang (str): Target language code
        service_name (Optional[str]): Specific service to use

    Returns:
        dict: Translated data with metadata
    """
```

**Input Format**:
```python
{
    'page_title': 'Lionel Messi',
    'arabic_fields': {
        'اسم': {'value': 'Lionel Messi', 'type': 'text'},
        'الطول': {'value': 1.70, 'type': 'number'},
        'الأندية': {'value': ['FC Barcelona', 'PSG'], 'type': 'numbered'}
    },
    'template_type': 'football_biography'
}
```

**Output Format**:
```python
{
    'page_title': 'Lionel Messi',
    'translated_fields': {
        'اسم': {
            'value': 'Lionel Messi', 
            'translated_value': 'ليونيل ميسي',
            'type': 'text',
            'translation_confidence': 0.9
        },
        'الطول': {
            'value': 1.70,
            'translated_value': 1.70,  # Numbers preserved
            'type': 'number',
            'translation_confidence': 1.0
        },
        'الأندية': {
            'value': ['FC Barcelona', 'PSG'],
            'translated_value': ['إف سي برشلونة', 'باريس سان جيرمان'],
            'type': 'numbered',
            'translation_confidence': 0.9
        }
    },
    'translation_metadata': {
        'service': 'Google Gemini AI',
        'target_language': 'ar',
        'translation_method': 'single_request',
        'total_fields': 3,
        'translated_fields': 3,
        'success': True
    }
}
```

### Alternative Translation Methods

#### Field-by-Field Translation
```python
def translate_field_by_field(mapped_data: dict, target_lang: str = 'ar',
                           service_name: Optional[str] = None) -> dict:
    """
    Alternative: Translate each field individually.
    Useful for debugging or when single-request fails.
    """
```

**Advantages**:
- Granular control over each field
- Easier to handle failures per field
- Better debugging capabilities

**Disadvantages**:
- Multiple API calls (higher cost)
- Loss of contextual relationships
- Slower performance

### Service Management

#### Service Discovery
```python
def get_available_translation_services() -> list:
    """Get list of registered translation services."""
    return ['gemini', 'google_gemini']  # Extensible

def test_translation_service(service_name: str = 'gemini') -> bool:
    """Test if a translation service is working."""
```

## Cost Optimization Features

### Single-Request Translation
- **Efficiency**: All fields in one API call
- **Cost Savings**: ~80% reduction in API costs compared to individual calls
- **Performance**: Significantly faster translation
- **Context Preservation**: Maintains relationships between fields

### Smart Field Type Filtering
- **Number Fields**: Skipped (no translation needed)
- **Image Fields**: Preserved (URLs and filenames kept)
- **Link Fields**: Only display text translated
- **Raw Fields**: Template syntax preserved

## Error Handling and Resilience

### Service Fallback
- **Primary Service Failure**: Automatic fallback to alternative service
- **Graceful Degradation**: Continue with untranslated fields if translation fails
- **Detailed Logging**: Comprehensive error reporting for debugging

### Validation and Quality Assurance
- **Confidence Scoring**: Each translation gets a confidence score
- **Field Type Validation**: Ensure translated content matches expected format
- **Content Preservation**: Original data always preserved alongside translations

## Performance Optimization

### LiteLLM Integration
- **Unified API**: Single interface for multiple AI providers
- **Load Balancing**: Automatic distribution across providers
- **Rate Limiting**: Built-in request throttling
- **Caching**: Optional translation result caching

### Configuration Tuning
- **Temperature Control**: Adjustable creativity vs. accuracy (default: 0.3 for consistent translations)
- **Token Limits**: Configurable maximum response length
- **Timeout Management**: Configurable request timeouts
- **Retry Logic**: Automatic retry with exponential backoff

## Extensibility

### Adding New Translation Services
```python
from translate.base_translator import TranslationService, TranslationServiceFactory

class OpenAITranslator(TranslationService):
    def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        # OpenAI-specific implementation
        pass
    
    def is_available(self) -> bool:
        # Check OpenAI API availability
        pass

# Register the service
TranslationServiceFactory.register_service("openai", OpenAITranslator)
```

### Custom Translation Strategies
```python
class HybridTranslator(TranslationService):
    """Combine multiple services for optimal results."""
    
    def translate_infobox(self, infobox_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        # Use Gemini for text, preserve for numbers/links, etc.
        pass
```

## Testing and Quality Assurance

### Translation Accuracy Testing
- **Field-by-Field Validation**: Compare expected vs. actual translations
- **Context Preservation**: Verify that translations maintain meaning
- **Format Consistency**: Ensure translations follow Arabic Wikipedia standards
- **Performance Metrics**: Track translation time, cost, and success rates

### Service Reliability Testing
- **Availability Checks**: Regular service health monitoring
- **Fallback Testing**: Verify fallback mechanisms work correctly
- **Load Testing**: Performance under high-volume translation requests

## Integration with Pipeline

### Data Flow Connection Points

**Input → From Map Stage:**
```python
mapped_data = {
    'arabic_fields': arabic_mapped_dict,  # ← Translation input
    'template_type': template_identifier
}
```

**Output → To Construct Stage:**
```python
translated_data = {
    'translated_fields': arabic_translated_dict,  # ← Template construction input
    'translation_metadata': translation_info
}
```

### Pipeline Integration Benefits
- **Seamless Data Flow**: Direct field mapping without data transformation
- **Metadata Propagation**: Translation context carried through pipeline stages
- **Error Isolation**: Translation failures don't stop entire pipeline
- **Quality Tracking**: Confidence scores and metadata for downstream processing

This translation stage represents a sophisticated AI-powered translation system that not only provides high-quality Arabic translations but also implements cost-effective optimization strategies and maintains the flexibility to integrate additional translation services as needed.