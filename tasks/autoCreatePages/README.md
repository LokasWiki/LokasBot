# AutoCreatePages - Clean Architecture Implementation

This task has been refactored to follow Clean Architecture principles for better maintainability, testability, and separation of concerns.

## Architecture Overview

The implementation follows a layered architecture with clear separation of responsibilities:

```
tasks/autoCreatePages/
├── main.py                     # Main entry point
├── CLEAN_ARCHITECTURE_PLAN.md  # Implementation documentation
├── domain/                     # Business logic layer
│   ├── entities/              # Core business objects
│   ├── repositories/          # Abstract data access interfaces
│   └── use_cases/             # Application-specific business rules
├── data/                      # Data access layer
│   ├── wiki_page_repository.py    # Wiki page operations
│   └── wiki_category_repository.py # Wiki category operations
├── presentation/              # Presentation layer
│   └── wiki_operations.py     # Wiki API abstractions
├── config/                    # Configuration layer
│   └── config_loader.py       # Configuration management
└── tests/                     # Test suite
    └── test_create_monthly_pages.py # Unit tests
```

## Key Benefits

1. **Testability**: Each layer can be tested independently with mocks
2. **Maintainability**: Clear separation of concerns makes code easier to understand
3. **Scalability**: New features can be added without affecting existing code
4. **Framework Independence**: Business logic is independent of external frameworks
5. **Configuration Management**: Externalized configuration for templates and settings

## Usage

### Running the Main Script

```bash
cd tasks/autoCreatePages
python main.py
```

The script will:
1. Check if today is the first day of the month
2. Load page configurations (from external files or defaults)
3. Create monthly maintenance pages
4. Create/update block user category
5. Log all operations

### Configuration

The system supports external configuration files:

- `config/pages_config.json`: Monthly page configurations
- `config/categories_config.json`: Category configurations

If configuration files don't exist, the system uses built-in defaults.

### Running Tests

```bash
cd tasks/autoCreatePages
python -m unittest tests/
# or
python -m pytest tests/
```

## Architecture Layers

### Domain Layer
- **Entities**: `Page`, `Category` - Core business objects
- **Repositories**: Abstract interfaces for data access
- **Use Cases**: `CreateMonthlyPages`, `CreateBlockCategory` - Business logic

### Data Layer
- **Repository Implementations**: Concrete implementations using pywikibot
- **Error Handling**: Comprehensive error handling and logging

### Presentation Layer
- **Wiki Operations**: Abstraction layer for wiki API interactions
- **Date Utilities**: Date validation and formatting utilities

### Configuration Layer
- **External Configuration**: JSON-based configuration management
- **Validation**: Configuration validation and fallbacks

## Migration from Legacy Code

The original `create.py` and `create_block_cat.py` files have been marked as deprecated. The new architecture provides the same functionality with improved structure.

## Testing Strategy

- **Unit Tests**: Test business logic in isolation using mocks
- **Integration Tests**: Test repository implementations
- **End-to-End Tests**: Test complete workflows

Example test execution:
```python
# Test the CreateMonthlyPages use case
mock_repository = Mock(spec=PageRepository)
use_case = CreateMonthlyPages(mock_repository)

result = use_case.execute(page_configs, test_date)
assert len(result['created_pages']) == expected_count
```

## Development Guidelines

1. **Dependency Direction**: Dependencies point inward toward domain layer
2. **Interface Segregation**: Use interfaces to decouple layers
3. **Single Responsibility**: Each class has one clear responsibility
4. **Test-Driven Development**: Write tests before implementing features

## Error Handling

The architecture includes comprehensive error handling:
- Repository operations include try-catch blocks
- Use cases handle business logic errors
- Presentation layer manages external API errors
- All errors are logged with appropriate levels

## Logging

The system includes comprehensive logging:
- File logging: `autoCreatePages.log`
- Console logging for immediate feedback
- Different log levels for different types of messages
- Structured logging with context information

## Future Enhancements

1. **Additional Use Cases**: Easy to add new page creation workflows
2. **Alternative Repositories**: Can implement different data sources
3. **Enhanced Configuration**: Support for more complex configuration schemas
4. **Monitoring**: Add metrics and monitoring capabilities
5. **Caching**: Implement caching for frequently accessed data

## Files Structure Summary

- `main.py`: Orchestrates the entire application
- `domain/`: Contains business rules and entities
- `data/`: Contains data access implementations
- `presentation/`: Contains external interface abstractions
- `config/`: Contains configuration management
- `tests/`: Contains test suites
- `create.py` (deprecated): Legacy implementation
- `create_block_cat.py` (deprecated): Legacy implementation