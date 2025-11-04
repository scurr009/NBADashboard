# Code Standards
## Python Style Guide and Best Practices

**Target Audience**: All developers  
**Purpose**: Ensure consistent, maintainable code across the project

---

## Table of Contents
1. [Python Style Guide](#python-style-guide)
2. [Module Structure](#module-structure)
3. [Documentation Requirements](#documentation-requirements)
4. [Error Handling](#error-handling)
5. [Logging Standards](#logging-standards)
6. [Testing Requirements](#testing-requirements)
7. [Performance Guidelines](#performance-guidelines)

---

## Python Style Guide

### Follow PEP 8

**Base Standard**: [PEP 8 - Style Guide for Python Code](https://pep8.org/)

**Key Rules**:
- 4 spaces for indentation (no tabs)
- Max line length: 100 characters (not 79)
- 2 blank lines between top-level functions/classes
- 1 blank line between methods
- Imports at top of file

---

### Naming Conventions

**Variables and Functions**: `snake_case`
```python
# Good
player_count = 100
def calculate_average_points():
    pass

# Bad
PlayerCount = 100
def CalculateAveragePoints():
    pass
```

**Classes**: `PascalCase`
```python
# Good
class DataExtractor:
    pass

# Bad
class data_extractor:
    pass
```

**Constants**: `UPPER_SNAKE_CASE`
```python
# Good
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Bad
maxRetries = 3
```

**Private Methods/Variables**: Prefix with `_`
```python
class DataLoader:
    def __init__(self):
        self._connection = None  # Private
    
    def _validate_schema(self):  # Private method
        pass
    
    def load_data(self):  # Public method
        pass
```

---

### Type Hints

**Always use type hints** for function signatures

```python
# Good
def calculate_ppg(points: int, games: int) -> float:
    return points / games

def extract_data(filename: str) -> pd.DataFrame:
    pass

def process_batch(items: List[Dict[str, Any]]) -> None:
    pass

# Bad
def calculate_ppg(points, games):
    return points / games
```

**Import types**:
```python
from typing import List, Dict, Optional, Union, Any, Tuple
import pandas as pd
```

**Optional values**:
```python
def get_player(player_id: int) -> Optional[Dict[str, Any]]:
    """Returns player dict or None if not found"""
    pass
```

---

### Imports

**Order**:
1. Standard library
2. Third-party packages
3. Local modules

**Format**:
```python
# Standard library
import os
import sys
from pathlib import Path
from typing import List, Dict

# Third-party
import pandas as pd
import duckdb
from dash import Dash, html

# Local
from etl.extract import extract_data
from etl.transform import transform_data
```

**Avoid**:
```python
# Bad - wildcard imports
from pandas import *

# Bad - importing everything
import pandas, duckdb, os, sys
```

---

## Module Structure

### File Organization

**Standard module structure**:
```python
"""
Module docstring explaining purpose
"""

# Imports
import os
from typing import List

# Constants
MAX_RETRIES = 3
DEFAULT_BATCH_SIZE = 1000

# Classes
class MyClass:
    """Class docstring"""
    pass

# Functions
def my_function() -> None:
    """Function docstring"""
    pass

# Main execution
if __name__ == '__main__':
    # Test or example code
    pass
```

---

### Class Structure

**Standard class organization**:
```python
class DataProcessor:
    """
    Process data for analytics
    
    Attributes:
        data_dir: Path to data directory
        batch_size: Number of records per batch
    """
    
    # Class variables
    DEFAULT_BATCH_SIZE = 1000
    
    def __init__(self, data_dir: str, batch_size: int = None):
        """
        Initialize processor
        
        Args:
            data_dir: Path to data directory
            batch_size: Optional batch size override
        """
        self.data_dir = Path(data_dir)
        self.batch_size = batch_size or self.DEFAULT_BATCH_SIZE
        self._connection = None  # Private attribute
    
    # Public methods
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data"""
        pass
    
    # Private methods
    def _validate(self, data: pd.DataFrame) -> bool:
        """Validate data"""
        pass
    
    # Properties
    @property
    def is_connected(self) -> bool:
        """Check if connected"""
        return self._connection is not None
```

---

## Documentation Requirements

### Module Docstrings

**Every module must have a docstring**:
```python
"""
ETL Transform Module

This module provides data transformation functions for cleaning
and standardizing NBA player statistics.

Functions:
    remove_duplicates: Remove duplicate records
    standardize_positions: Map positions to standard values
    transform_data: Main transformation pipeline

Example:
    from etl.transform import transform_data
    
    df_clean = transform_data(df_raw)
"""
```

---

### Function Docstrings

**Use Google style docstrings**:
```python
def calculate_efficiency(points: int, rebounds: int, assists: int, 
                        games: int) -> float:
    """
    Calculate player efficiency rating
    
    Efficiency is calculated as (points + rebounds + assists) / games.
    This is a simplified metric for demonstration purposes.
    
    Args:
        points: Total points scored
        rebounds: Total rebounds
        assists: Total assists
        games: Number of games played
    
    Returns:
        Efficiency rating as float
    
    Raises:
        ValueError: If games is zero or negative
    
    Example:
        >>> calculate_efficiency(1000, 500, 300, 50)
        36.0
    """
    if games <= 0:
        raise ValueError("Games must be positive")
    
    return (points + rebounds + assists) / games
```

---

### Class Docstrings

```python
class DataExtractor:
    """
    Extract data from various sources
    
    This class provides methods to extract data from CSV files, APIs,
    and databases. It handles validation and error handling.
    
    Attributes:
        data_dir: Path to data directory
        logger: Logger instance for this class
    
    Example:
        extractor = DataExtractor('data/raw')
        df = extractor.extract_csv('data.csv')
    """
    pass
```

---

### Inline Comments

**When to comment**:
- ✅ Complex logic that isn't obvious
- ✅ Why something is done a certain way
- ✅ Workarounds or non-obvious solutions
- ✅ TODOs and FIXMEs

**When NOT to comment**:
- ❌ Obvious code
- ❌ Repeating what code does
- ❌ Outdated information

```python
# Good - explains WHY
# Use player_id instead of name because 161 players have duplicate names
df = df.groupby('player_id')

# Bad - states the obvious
# Loop through dataframe
for index, row in df.iterrows():
    pass

# Good - explains workaround
# DuckDB requires column order to match schema, so reorder here
df_ordered = df[table_columns]

# Good - marks future work
# TODO: Add support for incremental updates
# FIXME: This fails for datasets > 1GB
```

---

## Error Handling

### Use Specific Exceptions

```python
# Good
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    logger.error(f"File not found: {filename}")
    raise
except pd.errors.EmptyDataError:
    logger.error(f"File is empty: {filename}")
    raise

# Bad
try:
    df = pd.read_csv(filename)
except Exception as e:
    print(f"Error: {e}")
```

---

### Provide Context

```python
# Good
try:
    result = process_data(df)
except ValueError as e:
    raise ValueError(f"Failed to process data for season {season}: {e}") from e

# Bad
try:
    result = process_data(df)
except ValueError:
    raise
```

---

### Clean Up Resources

```python
# Good - use context managers
with open('file.txt', 'r') as f:
    data = f.read()

# Good - use try/finally
con = duckdb.connect('db.db')
try:
    con.execute(query)
finally:
    con.close()

# Bad - no cleanup
f = open('file.txt', 'r')
data = f.read()
# File never closed!
```

---

## Logging Standards

### Use Logging Module

```python
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Use appropriate levels
logger.debug("Detailed diagnostic information")
logger.info("General informational messages")
logger.warning("Warning messages")
logger.error("Error messages")
logger.critical("Critical errors")
```

---

### Logging Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| DEBUG | Detailed diagnostic info | "Processing row 1234" |
| INFO | General progress | "Loaded 10,000 rows" |
| WARNING | Unexpected but handled | "Missing optional field" |
| ERROR | Error that was caught | "Failed to connect to API" |
| CRITICAL | Severe error | "Database corrupted" |

---

### Logging Best Practices

```python
# Good - structured logging
logger.info(f"Loaded {row_count:,} rows from {filename}")
logger.error(f"Failed to process player_id={player_id}: {error}")

# Bad - unstructured
logger.info("Loaded data")
logger.error("Error occurred")

# Good - log exceptions with traceback
try:
    process_data()
except Exception as e:
    logger.error("Failed to process data", exc_info=True)

# Good - use appropriate level
logger.debug(f"Processing record {i}")  # Verbose, only in debug mode
logger.info(f"Completed phase 1")  # Important milestone
```

---

## Testing Requirements

### Test Coverage

**Minimum requirements**:
- All public functions must have tests
- Critical paths must have tests
- Edge cases must have tests
- Target: 80%+ code coverage

---

### Test Structure

```python
import pytest
import pandas as pd
from etl.transform import remove_duplicates

class TestRemoveDuplicates:
    """Tests for remove_duplicates function"""
    
    def test_removes_exact_duplicates(self):
        """Should remove rows that are exactly the same"""
        df = pd.DataFrame({
            'id': [1, 1, 2],
            'value': [10, 10, 20]
        })
        
        result = remove_duplicates(df)
        
        assert len(result) == 2
        assert list(result['id']) == [1, 2]
    
    def test_keeps_unique_rows(self):
        """Should keep all rows if no duplicates"""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [10, 20, 30]
        })
        
        result = remove_duplicates(df)
        
        assert len(result) == 3
    
    def test_handles_empty_dataframe(self):
        """Should handle empty dataframe"""
        df = pd.DataFrame()
        
        result = remove_duplicates(df)
        
        assert len(result) == 0
```

---

### Test Naming

```python
# Good - descriptive names
def test_calculate_ppg_with_valid_inputs():
    pass

def test_calculate_ppg_raises_error_when_games_is_zero():
    pass

# Bad - unclear names
def test_ppg():
    pass

def test_error():
    pass
```

---

## Performance Guidelines

### Use Vectorized Operations

```python
# Good - vectorized (fast)
df['ppg'] = df['points'] / df['games']

# Bad - iterating (slow)
for i, row in df.iterrows():
    df.at[i, 'ppg'] = row['points'] / row['games']
```

---

### Avoid Unnecessary Copies

```python
# Good - modify in place
df.drop_duplicates(inplace=True)

# Bad - creates copy
df = df.drop_duplicates()  # If you don't need the original
```

---

### Use Appropriate Data Types

```python
# Good - use category for repeated strings
df['position'] = df['position'].astype('category')

# Good - use smaller int types when possible
df['age'] = df['age'].astype('int8')  # Age never > 127

# Bad - everything as object/string
df['age'] = df['age'].astype(str)
```

---

### Profile Before Optimizing

```python
# Use cProfile for profiling
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
process_data()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

---

## Code Review Checklist

### Before Submitting Code

- [ ] Code follows PEP 8
- [ ] Type hints added
- [ ] Docstrings complete
- [ ] Tests written and passing
- [ ] No hardcoded values (use constants)
- [ ] Error handling implemented
- [ ] Logging added
- [ ] No commented-out code
- [ ] No print() statements (use logging)
- [ ] Performance considered
- [ ] Documentation updated

---

## Anti-Patterns to Avoid

### ❌ Don't Do This

```python
# Bad - bare except
try:
    something()
except:
    pass

# Bad - mutable default arguments
def process(items=[]):
    items.append(1)
    return items

# Bad - comparing to True/False
if flag == True:
    pass

# Bad - not using context managers
f = open('file.txt')
data = f.read()
f.close()

# Bad - string concatenation in loops
result = ""
for item in items:
    result += str(item)
```

### ✅ Do This Instead

```python
# Good - specific exception
try:
    something()
except ValueError:
    logger.error("Invalid value")

# Good - None as default
def process(items=None):
    if items is None:
        items = []
    items.append(1)
    return items

# Good - direct boolean check
if flag:
    pass

# Good - use context manager
with open('file.txt') as f:
    data = f.read()

# Good - use join
result = ''.join(str(item) for item in items)
```

---

## Tools

### Recommended Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| **black** | Code formatter | `black .` |
| **flake8** | Linter | `flake8 .` |
| **mypy** | Type checker | `mypy .` |
| **pytest** | Testing | `pytest tests/` |
| **coverage** | Test coverage | `coverage run -m pytest` |
| **pylint** | Code analysis | `pylint etl/` |

### Configuration

**pyproject.toml**:
```toml
[tool.black]
line-length = 100
target-version = ['py39']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.coverage.run]
source = ["etl", "dashboard"]
omit = ["*/tests/*"]
```

---

## Related Documentation

- [Implementation Guide](implementation_guide.md) - Project setup
- [ETL Pattern Guide](etl_pattern_guide.md) - Code patterns
- [Architecture](architecture.md) - Design decisions

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Based on**: PEP 8, Google Python Style Guide
