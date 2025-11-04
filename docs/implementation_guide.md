# Implementation Guide
## Building a DuckDB ETL + Dashboard Project

**Target Audience**: Developers implementing this template  
**Time to Complete**: 1-2 days for basic implementation  
**Prerequisites**: Python 3.9+, basic SQL knowledge

---

## Table of Contents
1. [Phase 1: Project Setup](#phase-1-project-setup)
2. [Phase 2: Data Analysis](#phase-2-data-analysis)
3. [Phase 3: ETL Development](#phase-3-etl-development)
4. [Phase 4: Dashboard Development](#phase-4-dashboard-development)
5. [Phase 5: Testing & Validation](#phase-5-testing--validation)
6. [Common Pitfalls](#common-pitfalls)

---

## Phase 1: Project Setup

**Time**: 30 minutes  
**Goal**: Create project structure and install dependencies

### Step 1.1: Create Folder Structure

```bash
# Create project directory
mkdir my-analytics-project
cd my-analytics-project

# Create folder structure
mkdir -p data/raw data/processed data/duckdb
mkdir -p etl dashboard sql tests docs skills

# Create Python package files
touch etl/__init__.py
touch dashboard/__init__.py
```

### Step 1.2: Create Configuration Files

**requirements.txt**:
```txt
# Core dependencies
duckdb>=0.9.0
pandas>=2.0.0
pyarrow>=14.0.0

# Dashboard
dash>=2.14.0
plotly>=5.18.0

# Data validation
pydantic>=2.0.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
```

**.gitignore**:
```txt
# Python
__pycache__/
*.py[cod]
*.egg-info/
venv/

# Data
*.db
*.duckdb
data/processed/*.parquet
data/duckdb/*.db

# IDE
.vscode/
.idea/
```

### Step 1.3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 1.4: Verify Installation

```bash
python -c "import duckdb; import pandas; import dash; print('✅ All dependencies installed')"
```

### ✅ Phase 1 Checklist
- [ ] Folder structure created
- [ ] requirements.txt created
- [ ] .gitignore created
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Installation verified

---

## Phase 2: Data Analysis

**Time**: 1-2 hours  
**Goal**: Understand data quality issues and transformation needs

### Step 2.1: Place Raw Data

```bash
# Copy your data file to data/raw/
cp /path/to/your/data.csv data/raw/
```

### Step 2.2: Create Analysis Script

**etl/analyze_data.py**:
```python
import pandas as pd
import os

# Load data
csv_path = 'data/raw/your_data.csv'
df = pd.read_csv(csv_path)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"\nColumn types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nSample data:\n{df.head()}")

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"\nDuplicate rows: {duplicates}")

# Analyze key columns
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique values")
```

### Step 2.3: Run Analysis

```bash
python etl/analyze_data.py
```

### Step 2.4: Document Findings

Create `docs/data_quality_issues.md`:
```markdown
# Data Quality Issues

## Identified Issues
1. **Duplicates**: X duplicate records found
2. **Missing values**: Column Y has Z% missing
3. **Inconsistencies**: Column A has variations (list them)

## Transformation Decisions
1. **Issue**: Duplicate records
   **Solution**: Remove based on criteria X
   
2. **Issue**: Missing values
   **Solution**: Convert to NULL, handle in queries
```

### ✅ Phase 2 Checklist
- [ ] Raw data placed in data/raw/
- [ ] Analysis script created
- [ ] Analysis run successfully
- [ ] Data quality issues documented
- [ ] Transformation plan created

---

## Phase 3: ETL Development

**Time**: 3-4 hours  
**Goal**: Build extract, transform, load pipeline

### Step 3.1: Create Extract Module

**etl/extract.py**:
```python
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataExtractor:
    def __init__(self, data_dir='data/raw'):
        self.data_dir = Path(data_dir)
    
    def extract_csv(self, filename):
        csv_path = self.data_dir / filename
        logger.info(f"Reading: {csv_path}")
        
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df):,} rows")
        
        return df

def extract_data(filename):
    extractor = DataExtractor()
    return extractor.extract_csv(filename)
```

### Step 3.2: Create Transform Module

**etl/transform.py**:
```python
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate records"""
    initial = len(df)
    df = df.drop_duplicates()
    removed = initial - len(df)
    logger.info(f"Removed {removed} duplicates")
    return df

def handle_missing_values(df):
    """Handle missing values"""
    df = df.replace('NA', None)
    logger.info("Converted 'NA' strings to NULL")
    return df

def add_derived_metrics(df):
    """Add calculated columns"""
    # Example: Add per-game stats
    if 'total_points' in df.columns and 'games' in df.columns:
        df['ppg'] = df['total_points'] / df['games']
        logger.info("Added derived metric: ppg")
    return df

def transform_data(df):
    """Main transformation pipeline"""
    logger.info("Starting transformation...")
    
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = add_derived_metrics(df)
    
    logger.info(f"Transformation complete: {len(df):,} rows")
    return df
```

### Step 3.3: Create Load Module

**etl/load.py**:
```python
import duckdb
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, db_path='data/duckdb/database.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.con = None
    
    def connect(self):
        logger.info(f"Connecting to: {self.db_path}")
        self.con = duckdb.connect(str(self.db_path))
        return self.con
    
    def create_schema(self, table_name='data'):
        """Create table schema - customize for your data"""
        self.con.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Customize this CREATE TABLE statement for your schema
        create_sql = f"""
        CREATE TABLE {table_name} (
            id INTEGER,
            name VARCHAR,
            value DOUBLE,
            date DATE
        )
        """
        self.con.execute(create_sql)
        logger.info(f"Schema created: {table_name}")
    
    def load_dataframe(self, df, table_name='data'):
        logger.info(f"Loading {len(df):,} rows...")
        self.con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        logger.info("✅ Data loaded")
    
    def create_indexes(self, table_name='data'):
        """Create indexes - customize for your queries"""
        indexes = [
            f"CREATE INDEX idx_id ON {table_name}(id)",
            f"CREATE INDEX idx_date ON {table_name}(date)"
        ]
        for idx_sql in indexes:
            self.con.execute(idx_sql)
        logger.info("✅ Indexes created")
    
    def export_parquet(self, table_name='data', output_path='data/processed/data.parquet'):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.con.execute(f"""
            COPY {table_name} TO '{output_path}' (FORMAT PARQUET)
        """)
        logger.info(f"✅ Exported to: {output_path}")
    
    def close(self):
        if self.con:
            self.con.close()

def load_data(df, db_path=None):
    loader = DataLoader(db_path)
    try:
        loader.connect()
        loader.create_schema()
        loader.load_dataframe(df)
        loader.create_indexes()
        loader.export_parquet()
    finally:
        loader.close()
```

### Step 3.4: Create Pipeline Orchestration

**etl/pipeline.py**:
```python
import logging
import time
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline(csv_filename='your_data.csv'):
    start_time = time.time()
    
    logger.info("="*70)
    logger.info("ETL PIPELINE STARTING")
    logger.info("="*70)
    
    # Extract
    logger.info("\n[1/3] EXTRACT")
    df_raw = extract_data(csv_filename)
    
    # Transform
    logger.info("\n[2/3] TRANSFORM")
    df_clean = transform_data(df_raw)
    
    # Load
    logger.info("\n[3/3] LOAD")
    load_data(df_clean)
    
    # Summary
    elapsed = time.time() - start_time
    logger.info(f"\n✅ Pipeline complete in {elapsed:.2f}s")

if __name__ == '__main__':
    run_pipeline()
```

### Step 3.5: Test ETL Pipeline

```bash
python -m etl.pipeline
```

### ✅ Phase 3 Checklist
- [ ] extract.py created and tested
- [ ] transform.py created with business logic
- [ ] load.py created with schema
- [ ] pipeline.py orchestrates all steps
- [ ] Pipeline runs successfully
- [ ] Database created in data/duckdb/
- [ ] Parquet exported to data/processed/

---

## Phase 4: Dashboard Development

**Time**: 2-3 hours  
**Goal**: Create interactive dashboard

### Step 4.1: Create Basic Dashboard

**dashboard/app.py**:
```python
import duckdb
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

# Connect to database
con = duckdb.connect('data/duckdb/database.db')

# Create app
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Analytics Dashboard'),
    
    # Filters
    html.Div([
        html.Label('Select Metric:'),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Metric 1', 'value': 'metric1'},
                {'label': 'Metric 2', 'value': 'metric2'}
            ],
            value='metric1'
        )
    ]),
    
    # Visualization
    dcc.Graph(id='main-chart')
])

@app.callback(
    Output('main-chart', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_chart(metric):
    # Query database
    query = f"SELECT * FROM data ORDER BY date LIMIT 100"
    df = con.execute(query).fetchdf()
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df[metric],
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title=f'{metric} Over Time',
        xaxis_title='Date',
        yaxis_title=metric
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
```

### Step 4.2: Test Dashboard

```bash
python dashboard/app.py
```

Visit: http://127.0.0.1:8050/

### Step 4.3: Enhance Dashboard (Optional)

Add more features:
- Multiple visualizations
- Additional filters
- Performance metrics
- Export functionality

### ✅ Phase 4 Checklist
- [ ] Basic dashboard created
- [ ] Database connection working
- [ ] Filters functional
- [ ] Visualizations displaying
- [ ] Dashboard accessible in browser

---

## Phase 5: Testing & Validation

**Time**: 1-2 hours  
**Goal**: Ensure quality and correctness

### Step 5.1: Create Data Validation Tests

**tests/test_transform.py**:
```python
import pytest
import pandas as pd
from etl.transform import remove_duplicates, handle_missing_values

def test_remove_duplicates():
    df = pd.DataFrame({
        'id': [1, 1, 2],
        'value': [10, 10, 20]
    })
    result = remove_duplicates(df)
    assert len(result) == 2

def test_handle_missing_values():
    df = pd.DataFrame({
        'col1': ['NA', 'value', 'NA']
    })
    result = handle_missing_values(df)
    assert result['col1'].isnull().sum() == 2
```

### Step 5.2: Run Tests

```bash
pytest tests/ -v
```

### Step 5.3: Validate Data Quality

Create validation queries in `sql/validation.sql`:
```sql
-- Check for duplicates
SELECT COUNT(*) as duplicate_count
FROM (
    SELECT *, COUNT(*) OVER (PARTITION BY id) as cnt
    FROM data
) WHERE cnt > 1;

-- Check for NULL values
SELECT 
    COUNT(*) - COUNT(column1) as nulls_col1,
    COUNT(*) - COUNT(column2) as nulls_col2
FROM data;

-- Check data ranges
SELECT 
    MIN(value) as min_value,
    MAX(value) as max_value,
    AVG(value) as avg_value
FROM data;
```

### ✅ Phase 5 Checklist
- [ ] Unit tests created
- [ ] Tests passing
- [ ] Data validation queries created
- [ ] Data quality verified
- [ ] Documentation updated

---

## Common Pitfalls

### 1. **Schema Mismatch**
**Problem**: DataFrame columns don't match database schema  
**Solution**: Reorder DataFrame columns to match table schema
```python
table_cols = ['col1', 'col2', 'col3']
df_ordered = df[table_cols]
```

### 2. **Memory Issues with Large Files**
**Problem**: CSV too large to fit in memory  
**Solution**: Use chunked reading
```python
chunks = pd.read_csv('large_file.csv', chunksize=10000)
for chunk in chunks:
    process(chunk)
```

### 3. **Slow Queries**
**Problem**: Dashboard queries are slow  
**Solution**: Add indexes on filtered columns
```sql
CREATE INDEX idx_date ON table(date);
CREATE INDEX idx_category ON table(category);
```

### 4. **Type Conversion Errors**
**Problem**: Data types don't match schema  
**Solution**: Explicitly convert types
```python
df['date'] = pd.to_datetime(df['date'])
df['value'] = df['value'].astype(float)
```

### 5. **Missing Dependencies**
**Problem**: Import errors  
**Solution**: Ensure virtual environment is activated
```bash
# Check which Python
which python  # Should show venv path

# Reinstall if needed
pip install -r requirements.txt
```

---

## Quick Reference Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run ETL
python -m etl.pipeline

# Run Dashboard
python dashboard/app.py

# Run Tests
pytest tests/ -v

# Query Database
duckdb data/duckdb/database.db
```

---

## Next Steps

After completing implementation:
1. ✅ Review [Code Standards](code_standards.md)
2. ✅ Read [ETL Pattern Guide](etl_pattern_guide.md)
3. ✅ Explore [Database Design Guide](database_design.md)
4. ✅ Check [Troubleshooting Guide](quick_reference/troubleshooting.md)

---

## Time Estimates Summary

| Phase | Time | Complexity |
|-------|------|------------|
| Phase 1: Setup | 30 min | Low |
| Phase 2: Analysis | 1-2 hrs | Medium |
| Phase 3: ETL | 3-4 hrs | Medium-High |
| Phase 4: Dashboard | 2-3 hrs | Medium |
| Phase 5: Testing | 1-2 hrs | Low-Medium |
| **Total** | **8-12 hrs** | - |

**Experienced developers**: Lower end of range  
**New to stack**: Upper end of range  

---

**Document Version**: 1.0  
**Last Updated**: November 2025
