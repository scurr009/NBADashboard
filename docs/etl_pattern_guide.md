# ETL Pattern Guide
## Reusable Patterns for Extract, Transform, Load

**Target Audience**: Data engineers, developers  
**Purpose**: Reference guide for common ETL patterns

---

## Table of Contents
1. [Extract Patterns](#extract-patterns)
2. [Transform Patterns](#transform-patterns)
3. [Load Patterns](#load-patterns)
4. [Error Handling](#error-handling)
5. [Performance Optimization](#performance-optimization)
6. [Pattern Library](#pattern-library)

---

## Extract Patterns

### Pattern 1: CSV Extraction with Validation

**Use Case**: Reading CSV files with schema validation

```python
import pandas as pd
from pathlib import Path
import logging

class CSVExtractor:
    def __init__(self, data_dir='data/raw'):
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(__name__)
    
    def extract(self, filename, required_columns=None):
        """
        Extract data from CSV with validation
        
        Args:
            filename: CSV file name
            required_columns: List of required column names
            
        Returns:
            DataFrame
        """
        csv_path = self.data_dir / filename
        
        # Validate file exists
        if not csv_path.exists():
            raise FileNotFoundError(f"File not found: {csv_path}")
        
        # Read CSV
        self.logger.info(f"Reading: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Validate schema
        if required_columns:
            missing = set(required_columns) - set(df.columns)
            if missing:
                raise ValueError(f"Missing columns: {missing}")
        
        # Log metadata
        self.logger.info(f"Loaded {len(df):,} rows, {len(df.columns)} columns")
        
        return df
```

**Usage**:
```python
extractor = CSVExtractor()
df = extractor.extract('data.csv', required_columns=['id', 'name', 'value'])
```

---

### Pattern 2: Chunked Reading for Large Files

**Use Case**: Files too large for memory

```python
def extract_large_csv(filename, chunksize=10000):
    """Process large CSV in chunks"""
    chunks = []
    
    for chunk in pd.read_csv(filename, chunksize=chunksize):
        # Process each chunk
        chunk_processed = process_chunk(chunk)
        chunks.append(chunk_processed)
    
    # Combine all chunks
    df = pd.concat(chunks, ignore_index=True)
    return df

def process_chunk(chunk):
    """Process individual chunk"""
    # Apply transformations that can work on chunks
    chunk = chunk.dropna(subset=['id'])
    chunk['processed'] = True
    return chunk
```

---

### Pattern 3: Multi-File Extraction

**Use Case**: Combine multiple files into one dataset

```python
def extract_multiple_files(file_pattern='data/raw/*.csv'):
    """Extract and combine multiple CSV files"""
    from glob import glob
    
    files = glob(file_pattern)
    logger.info(f"Found {len(files)} files")
    
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        df['source_file'] = Path(file).name
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    logger.info(f"Combined {len(combined):,} rows from {len(files)} files")
    
    return combined
```

---

### Pattern 4: API Extraction

**Use Case**: Fetch data from REST API

```python
import requests
import pandas as pd

class APIExtractor:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
    
    def extract(self, endpoint, params=None):
        """Extract data from API endpoint"""
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data)
        
        logger.info(f"Extracted {len(df):,} rows from {endpoint}")
        return df
```

---

## Transform Patterns

### Pattern 1: Duplicate Removal

**Use Case**: Remove duplicate records

```python
def remove_duplicates(df, subset=None, keep='first'):
    """
    Remove duplicate rows
    
    Args:
        df: DataFrame
        subset: Columns to consider for duplicates (None = all)
        keep: 'first', 'last', or False (remove all duplicates)
    """
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=subset, keep=keep)
    removed = initial_count - len(df_clean)
    
    logger.info(f"Removed {removed:,} duplicates ({removed/initial_count*100:.1f}%)")
    return df_clean
```

**Usage**:
```python
# Remove complete duplicates
df = remove_duplicates(df)

# Remove duplicates based on specific columns
df = remove_duplicates(df, subset=['id', 'date'])

# Remove all duplicate rows (keep none)
df = remove_duplicates(df, subset=['id'], keep=False)
```

---

### Pattern 2: Missing Value Handling

**Use Case**: Handle NULL/NA values consistently

```python
def handle_missing_values(df, strategy='convert'):
    """
    Handle missing values
    
    Strategies:
    - 'convert': Convert 'NA' strings to NULL
    - 'drop': Drop rows with any NULL
    - 'fill': Fill with default values
    """
    if strategy == 'convert':
        df = df.replace(['NA', 'N/A', 'null', ''], None)
        logger.info("Converted string NAs to NULL")
    
    elif strategy == 'drop':
        initial = len(df)
        df = df.dropna()
        logger.info(f"Dropped {initial - len(df)} rows with NULLs")
    
    elif strategy == 'fill':
        # Fill numeric columns with 0, strings with 'Unknown'
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna('Unknown')
        logger.info("Filled NULL values")
    
    return df
```

---

### Pattern 3: Value Standardization

**Use Case**: Standardize inconsistent values

```python
def standardize_values(df, column, mapping):
    """
    Standardize values using mapping
    
    Args:
        df: DataFrame
        column: Column to standardize
        mapping: Dict of old_value -> new_value
    """
    df[f'{column}_original'] = df[column]  # Preserve original
    df[column] = df[column].map(mapping)
    
    # Check for unmapped values
    unmapped = df[df[column].isnull()][f'{column}_original'].unique()
    if len(unmapped) > 0:
        logger.warning(f"Unmapped values in {column}: {unmapped}")
    
    logger.info(f"Standardized {column}: {len(mapping)} mappings")
    return df
```

**Example**:
```python
# Standardize position codes
position_map = {
    'PG': 'Point Guard',
    'SG': 'Shooting Guard',
    'SF': 'Small Forward',
    'PF': 'Power Forward',
    'C': 'Center'
}
df = standardize_values(df, 'position', position_map)
```

---

### Pattern 4: Derived Metrics

**Use Case**: Calculate new columns from existing data

```python
def add_derived_metrics(df, metrics_config):
    """
    Add calculated columns
    
    Args:
        df: DataFrame
        metrics_config: Dict of {new_col: calculation_func}
    """
    for col_name, calc_func in metrics_config.items():
        df[col_name] = calc_func(df)
        logger.info(f"Added derived metric: {col_name}")
    
    return df
```

**Example**:
```python
metrics = {
    'ppg': lambda df: df['points'] / df['games'],
    'rpg': lambda df: df['rebounds'] / df['games'],
    'efficiency': lambda df: (df['points'] + df['rebounds'] + df['assists']) / df['games']
}
df = add_derived_metrics(df, metrics)
```

---

### Pattern 5: Data Type Conversion

**Use Case**: Ensure correct data types

```python
def convert_types(df, type_map):
    """
    Convert column data types
    
    Args:
        df: DataFrame
        type_map: Dict of {column: dtype}
    """
    for col, dtype in type_map.items():
        if col in df.columns:
            try:
                if dtype == 'datetime':
                    df[col] = pd.to_datetime(df[col])
                else:
                    df[col] = df[col].astype(dtype)
                logger.info(f"Converted {col} to {dtype}")
            except Exception as e:
                logger.error(f"Failed to convert {col}: {e}")
    
    return df
```

**Example**:
```python
types = {
    'id': 'int64',
    'value': 'float64',
    'date': 'datetime',
    'category': 'category'
}
df = convert_types(df, types)
```

---

### Pattern 6: Filtering

**Use Case**: Remove unwanted records

```python
def filter_data(df, conditions):
    """
    Filter DataFrame based on conditions
    
    Args:
        df: DataFrame
        conditions: List of (column, operator, value) tuples
    """
    initial_count = len(df)
    
    for col, op, value in conditions:
        if op == '==':
            df = df[df[col] == value]
        elif op == '!=':
            df = df[df[col] != value]
        elif op == '>':
            df = df[df[col] > value]
        elif op == '>=':
            df = df[df[col] >= value]
        elif op == '<':
            df = df[df[col] < value]
        elif op == '<=':
            df = df[df[col] <= value]
        elif op == 'in':
            df = df[df[col].isin(value)]
        elif op == 'not in':
            df = df[~df[col].isin(value)]
    
    removed = initial_count - len(df)
    logger.info(f"Filtered {removed:,} rows ({removed/initial_count*100:.1f}%)")
    
    return df
```

**Example**:
```python
conditions = [
    ('team', '!=', 'TOT'),  # Remove TOT records
    ('games', '>=', 10),     # Minimum 10 games
    ('season', 'in', [2023, 2024, 2025])  # Recent seasons only
]
df = filter_data(df, conditions)
```

---

## Load Patterns

### Pattern 1: Bulk Load with Schema Creation

**Use Case**: Create table and load data

```python
class BulkLoader:
    def __init__(self, db_path):
        self.con = duckdb.connect(db_path)
    
    def load(self, df, table_name, schema=None):
        """
        Create table and load data
        
        Args:
            df: DataFrame to load
            table_name: Target table name
            schema: Optional CREATE TABLE statement
        """
        # Drop existing table
        self.con.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Create schema
        if schema:
            self.con.execute(schema)
        else:
            # Auto-create from DataFrame
            self.con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df LIMIT 0")
        
        # Bulk insert
        self.con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        
        count = self.con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        logger.info(f"Loaded {count:,} rows into {table_name}")
```

---

### Pattern 2: Incremental Load

**Use Case**: Append new data without full reload

```python
def incremental_load(df, table_name, key_column, con):
    """
    Load only new records
    
    Args:
        df: New data
        table_name: Target table
        key_column: Column to check for existing records
        con: DuckDB connection
    """
    # Get existing keys
    existing_keys = con.execute(
        f"SELECT DISTINCT {key_column} FROM {table_name}"
    ).fetchdf()[key_column].tolist()
    
    # Filter to new records only
    df_new = df[~df[key_column].isin(existing_keys)]
    
    if len(df_new) > 0:
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df_new")
        logger.info(f"Loaded {len(df_new):,} new records")
    else:
        logger.info("No new records to load")
```

---

### Pattern 3: Upsert (Update or Insert)

**Use Case**: Update existing records, insert new ones

```python
def upsert(df, table_name, key_columns, con):
    """
    Update existing records or insert new ones
    
    Args:
        df: Data to upsert
        table_name: Target table
        key_columns: Columns that define uniqueness
        con: DuckDB connection
    """
    # Create temp table
    con.execute("DROP TABLE IF EXISTS temp_upsert")
    con.execute("CREATE TABLE temp_upsert AS SELECT * FROM df")
    
    # Delete existing records
    key_condition = " AND ".join([f"t.{col} = s.{col}" for col in key_columns])
    con.execute(f"""
        DELETE FROM {table_name} t
        WHERE EXISTS (
            SELECT 1 FROM temp_upsert s
            WHERE {key_condition}
        )
    """)
    
    # Insert all records from temp
    con.execute(f"INSERT INTO {table_name} SELECT * FROM temp_upsert")
    
    # Cleanup
    con.execute("DROP TABLE temp_upsert")
    
    logger.info(f"Upserted {len(df):,} records")
```

---

### Pattern 4: Index Creation

**Use Case**: Optimize query performance

```python
def create_indexes(table_name, index_columns, con):
    """
    Create indexes on specified columns
    
    Args:
        table_name: Table to index
        index_columns: List of columns or list of column lists for composite
        con: DuckDB connection
    """
    for cols in index_columns:
        if isinstance(cols, str):
            cols = [cols]
        
        idx_name = f"idx_{'_'.join(cols)}"
        col_list = ', '.join(cols)
        
        sql = f"CREATE INDEX {idx_name} ON {table_name}({col_list})"
        con.execute(sql)
        logger.info(f"Created index: {idx_name}")
```

**Example**:
```python
indexes = [
    'season',           # Single column
    'player_id',        # Single column
    ['player_id', 'season']  # Composite index
]
create_indexes('players', indexes, con)
```

---

## Error Handling

### Pattern: Robust ETL with Error Handling

```python
class RobustETL:
    def __init__(self):
        self.errors = []
    
    def run_pipeline(self, steps):
        """
        Run pipeline with error handling
        
        Args:
            steps: List of (step_name, step_function, args) tuples
        """
        for step_name, step_func, args in steps:
            try:
                logger.info(f"Running: {step_name}")
                result = step_func(*args)
                logger.info(f"✅ {step_name} complete")
            except Exception as e:
                error_msg = f"❌ {step_name} failed: {str(e)}"
                logger.error(error_msg)
                self.errors.append((step_name, str(e)))
                
                # Decide whether to continue or stop
                if self.is_critical_step(step_name):
                    raise
                else:
                    logger.warning(f"Continuing despite error in {step_name}")
        
        return len(self.errors) == 0
    
    def is_critical_step(self, step_name):
        """Define which steps are critical"""
        critical_steps = ['extract', 'load']
        return step_name in critical_steps
```

---

## Performance Optimization

### Pattern 1: Parallel Processing

```python
from multiprocessing import Pool

def process_in_parallel(data_chunks, process_func, n_workers=4):
    """Process data chunks in parallel"""
    with Pool(n_workers) as pool:
        results = pool.map(process_func, data_chunks)
    
    return pd.concat(results, ignore_index=True)
```

### Pattern 2: Batch Processing

```python
def batch_load(df, table_name, batch_size=10000, con=None):
    """Load data in batches"""
    total_rows = len(df)
    
    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i:i+batch_size]
        con.execute(f"INSERT INTO {table_name} SELECT * FROM batch")
        logger.info(f"Loaded batch {i//batch_size + 1}: {len(batch)} rows")
```

---

## Pattern Library

### Quick Reference

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| CSV Extraction | Read CSV with validation | Low |
| Chunked Reading | Large files | Medium |
| Multi-File | Combine multiple files | Low |
| API Extraction | REST API data | Medium |
| Remove Duplicates | Data quality | Low |
| Handle Missing | NULL values | Low |
| Standardize Values | Inconsistent data | Low |
| Derived Metrics | Calculated columns | Low |
| Type Conversion | Data types | Low |
| Filtering | Remove unwanted rows | Low |
| Bulk Load | Initial load | Low |
| Incremental Load | Append new data | Medium |
| Upsert | Update or insert | Medium-High |
| Create Indexes | Performance | Low |
| Error Handling | Robustness | Medium |
| Parallel Processing | Performance | High |

---

## Related Documentation

- [Implementation Guide](implementation_guide.md) - Step-by-step setup
- [Code Standards](code_standards.md) - Coding conventions
- [Database Design Guide](database_design.md) - Schema patterns

---

**Document Version**: 1.0  
**Last Updated**: November 2025
