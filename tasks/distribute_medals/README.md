# Medal Distribution System - Clean Architecture Implementation

A complete refactor of the medal distribution system using Clean Architecture principles.

## Overview

This project distributes medals to eligible Wikipedia users based on their edit counts. The system has been refactored to follow Clean Architecture principles, providing better separation of concerns, testability, and maintainability.

## Architecture

The system is organized into four main layers:

### 1. Domain Layer (`domain/`)
Contains the core business logic and entities that are independent of external concerns.

- **`entities/`**: Core business entities
  - `Medal`: Represents medal configurations
  - `User`: Represents eligible users
  - `Template`: Represents formatted templates
  - `Signature`: Represents user signatures

- **`repositories/`**: Repository interfaces (contracts)
  - `DatabaseRepository`: Database operations interface
  - `WikiRepository`: Wiki operations interface
  - `SignatureRepository`: Signature operations interface

- **`use_cases/`**: Business logic orchestrators
  - `DistributeMedals`: Main medal distribution workflow
  - `FetchEligibleUsers`: User eligibility checking
  - `ManageSignatures`: Signature management
  - `SendMedalTemplate`: Template sending logic

### 2. Infrastructure Layer (`infrastructure/`)
Contains concrete implementations of repository interfaces and external dependencies.

- **`database/`**: Database implementations
  - `MySQLDatabase`: MySQL database operations

- **`wiki/`**: Wiki operation implementations
  - `PywikibotWiki`: Pywikibot-based wiki operations

- **`scanners/`**: Text scanning implementations
  - `SignatureScanner`: Regex-based signature extraction

### 3. Presentation Layer (`presentation/`)
Handles orchestration and provides entry points for the application.

- **`controllers/`**: Application controllers
  - `MedalController`: Main application controller

- **`cli/`**: Command-line interface
  - `main.py`: CLI entry point with test and production modes

## Key Benefits

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Business logic can be tested without external dependencies
3. **Maintainability**: Changes to one layer don't affect others
4. **Scalability**: Easy to add new medal types or data sources
5. **Dependency Inversion**: High-level modules don't depend on low-level ones

## Usage

### Production Mode
```bash
# Using the new clean architecture
python -m tasks.distribute_medals.main

# Legacy compatibility
python tasks/distribute_medals/run.py
```

### Test Mode
```bash
# Using the new clean architecture
python -m tasks.distribute_medals.main --test

# Legacy compatibility
python tasks/distribute_medals/test.py
```

## Architecture Flow

```
CLI Presentation → MedalController → Use Cases → Repository Interfaces
                                                           ↓
External Dependencies: Database ← Infrastructure → Wiki ← API
```

## Configuration

The system uses the existing medal configurations from `data.py` and integrates them into the new architecture. No changes to the configuration format are required.

## Dependencies

- `pymysql`: MySQL database operations
- `pywikibot`: Wikipedia API operations
- `wikitextparser`: Wiki text parsing

## Migration from Legacy Code

The legacy `run.py` and `test.py` files have been updated to use the new clean architecture while maintaining backward compatibility. The existing functionality remains the same, but now uses the improved architecture internally.

## Testing

The new architecture includes comprehensive error handling and logging. The test mode (`--test`) validates all system components before running the distribution process.

## Error Handling

- Structured error handling across all layers
- Graceful degradation when external services are unavailable
- Comprehensive logging for debugging and monitoring

## Future Enhancements

- Configuration-based medal definitions
- Multiple database backend support
- Enhanced signature management
- RESTful API interface
- Async processing capabilities

## Development

When adding new features:

1. **Domain Layer**: Add business logic to appropriate use cases
2. **Infrastructure**: Implement new repository interfaces
3. **Presentation**: Update controllers and CLI as needed
4. **Testing**: Add unit tests for new functionality

## File Structure

```
tasks/distribute_medals/
├── __init__.py
├── main.py                      # New main entry point
├── README.md                    # This documentation
├── domain/                      # Core business logic
│   ├── entities/               # Business entities
│   ├── repositories/           # Repository interfaces
│   └── use_cases/              # Business logic
├── infrastructure/             # External implementations
│   ├── database/               # Database operations
│   ├── wiki/                   # Wiki operations
│   └── scanners/               # Text scanning
├── presentation/               # UI/Orchestration
│   ├── controllers/            # Application controllers
│   └── cli/                    # Command line interface
├── data.py                     # Medal configurations (unchanged)
├── module.py                   # Legacy code (deprecated)
├── run.py                      # Legacy entry point (updated)
└── test.py                     # Legacy test entry (updated)
```

## Version

- **Current**: 2.0.0 (Clean Architecture)
- **Previous**: 1.x.x (Monolithic)