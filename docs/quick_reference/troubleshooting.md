# Troubleshooting Guide
## Common Issues and Solutions

**Quick Reference**: Solutions to common problems

---

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [ETL Pipeline Issues](#etl-pipeline-issues)
3. [Database Issues](#database-issues)
4. [Dashboard Issues](#dashboard-issues)
5. [Performance Issues](#performance-issues)
6. [Data Quality Issues](#data-quality-issues)

---

## Installation Issues

### Issue: "Module not found" Error

**Error**:
```
ModuleNotFoundError: No module named 'duckdb'
```

**Cause**: Dependencies not installed or wrong Python environment

**Solution**:
```bash
# Check which Python you're using
which python  # Should show venv path

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import duckdb; print('✅ DuckDB installed')"
```

---

### Issue: "Permission denied" on Windows

**Error**:
```
cannot be loaded because running scripts is disabled
```

**Cause**: PowerShell execution policy

**Solution**:
```powershell
# Set execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run in Command Prompt instead of PowerShell
cmd
venv\Scripts\activate.bat
```

---

### Issue: pip install fails

**Error**:
```
ERROR: Could not install packages due to an OSError
```

**Solutions**:
```bash
# Try upgrading pip
python -m pip install --upgrade pip

# Install with --user flag
pip install --user -r requirements.txt

# Check Python version (need 3.9+)
python --version

# Try installing packages one at a time
pip install duckdb
pip install pandas
pip install dash
```

---

## ETL Pipeline Issues

### Issue: "File not found: NBA_Player_Totals.csv"

**Error**:
```
FileNotFoundError: data/raw/NBA_Player_Totals.csv
```

**Cause**: CSV file not in correct location

**Solution**:
```bash
# Check current directory
pwd

# List files in data/raw
ls data/raw/

# Move CSV to correct location
mv NBA_Player_Totals.csv data/raw/

# Or update path in extract.py
# csv_path = 'path/to/your/file.csv'
```

---

### Issue: "Conversion Error" during load

**Error**:
```
ConversionException: Could not convert string 'NBA' to INT32
```

**Cause**: Column order mismatch between DataFrame and database schema

**Solution**:
```python
# In etl/load.py, reorder DataFrame columns to match schema
def load_dataframe(self, df):
    # Get table column order
    table_cols = self.con.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name = 'players' ORDER BY ordinal_position"
    ).fetchall()
    table_col_names = [col[0] for col in table_cols]
    
    # Reorder DataFrame
    df_ordered = df[table_col_names]
    
    # Now insert
    self.con.execute("INSERT INTO players SELECT * FROM df_ordered")
```

---

### Issue: ETL runs but no data loaded

**Symptoms**: Pipeline completes but database is empty

**Debug**:
```python
# Add logging to check data at each step
print(f"After extract: {len(df)} rows")
print(f"After transform: {len(df_clean)} rows")

# Check database
import duckdb
con = duckdb.connect('data/duckdb/nba.db')
count = con.execute("SELECT COUNT(*) FROM players").fetchone()[0]
print(f"Database has {count} rows")
```

**Common causes**:
1. All rows filtered out in transform
2. Table created but insert failed silently
3. Wrong database file path

---

### Issue: "Unmapped positions found"

**Error**:
```
ValueError: Unmapped positions: ['G-F']
```

**Cause**: Position not in mapping dictionary

**Solution**:
```python
# Add missing position to POSITION_MAP in etl/transform.py
POSITION_MAP = {
    ...
    'G-F': 'SG',  # Add this line
    ...
}
```

---

## Database Issues

### Issue: Database file locked

**Error**:
```
database is locked
```

**Cause**: Another process has database open

**Solution**:
```bash
# Close any open connections
# Stop dashboard if running (Ctrl+C)

# Check for processes using the file (Linux/Mac)
lsof data/duckdb/nba.db

# Windows: Close DuckDB CLI or other connections

# If stuck, delete and recreate
rm data/duckdb/nba.db
python -m etl.pipeline
```

---

### Issue: Query returns no results

**Symptoms**: Query runs but returns 0 rows

**Debug**:
```sql
-- Check total rows
SELECT COUNT(*) FROM players;

-- Check if your filter is too restrictive
SELECT COUNT(*) FROM players WHERE season = 2025;
SELECT COUNT(*) FROM players WHERE team = 'LAL';

-- Check for NULL values
SELECT COUNT(*) FROM players WHERE column_name IS NULL;

-- Check actual values
SELECT DISTINCT season FROM players ORDER BY season;
SELECT DISTINCT team FROM players ORDER BY team;
```

---

### Issue: Slow queries

**Symptoms**: Queries take >1 second

**Solutions**:
```sql
-- 1. Check if indexes exist
SELECT * FROM duckdb_indexes();

-- 2. Create missing indexes
CREATE INDEX idx_season ON players(season);
CREATE INDEX idx_team ON players(team);

-- 3. Use EXPLAIN to see query plan
EXPLAIN SELECT * FROM players WHERE season = 2025;

-- 4. Select only needed columns
SELECT player, ppg FROM players  -- Good
SELECT * FROM players  -- Bad (slower)

-- 5. Filter early
SELECT * FROM players 
WHERE season = 2025 AND games >= 20  -- Filter first
ORDER BY ppg DESC;
```

---

## Dashboard Issues

### Issue: Dashboard won't start

**Error**:
```
Address already in use
```

**Cause**: Port 8050 already in use

**Solution**:
```bash
# Option 1: Use different port
python nba_dashboard_duckdb.py --port 8051

# Option 2: Find and kill process using port 8050
# Windows:
netstat -ano | findstr :8050
taskkill /PID <process_id> /F

# Mac/Linux:
lsof -i :8050
kill -9 <process_id>
```

---

### Issue: Dashboard loads but shows no data

**Symptoms**: Dashboard displays but charts are empty

**Debug**:
```python
# Check database connection in dashboard code
con = duckdb.connect('data/duckdb/nba.db')
print(con.execute("SELECT COUNT(*) FROM players").fetchone()[0])

# Check query results
df = con.execute("SELECT * FROM players LIMIT 5").fetchdf()
print(df)

# Add logging to callback
@app.callback(...)
def update_chart(...):
    print(f"Callback triggered with filters: {filters}")
    df = con.execute(query).fetchdf()
    print(f"Query returned {len(df)} rows")
    return fig
```

---

### Issue: Filters not working

**Symptoms**: Changing filters doesn't update chart

**Causes & Solutions**:

1. **Callback not triggered**:
```python
# Check Input/Output IDs match
@app.callback(
    Output('chart-id', 'figure'),  # Must match dcc.Graph id
    Input('filter-id', 'value')     # Must match dcc.Dropdown id
)
```

2. **Query not using filter**:
```python
# Make sure filter is in WHERE clause
query = f"SELECT * FROM players WHERE season = {season}"  # Good
query = f"SELECT * FROM players"  # Bad - ignores filter
```

3. **None value not handled**:
```python
# Handle None from clearable dropdowns
team = team or 'ALL'
if team != 'ALL':
    query += f" AND team = '{team}'"
```

---

### Issue: Dashboard is slow

**Symptoms**: Takes >2 seconds to update

**Solutions**:

1. **Add indexes** (most common fix):
```sql
CREATE INDEX idx_season ON players(season);
CREATE INDEX idx_team ON players(team);
```

2. **Limit data returned**:
```python
# Add LIMIT to queries
query = "SELECT * FROM players WHERE ... LIMIT 1000"
```

3. **Use caching**:
```python
from dash import dcc
import dash

# Enable caching
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Cache expensive queries
@cache.memoize(timeout=300)  # Cache for 5 minutes
def get_data(filters):
    return con.execute(query).fetchdf()
```

4. **Optimize queries**:
```python
# Select only needed columns
query = "SELECT player, ppg FROM players"  # Good
query = "SELECT * FROM players"  # Bad
```

---

## Performance Issues

### Issue: ETL takes too long

**Symptoms**: Pipeline takes >10 seconds for small dataset

**Solutions**:

1. **Use bulk operations**:
```python
# Good - bulk insert
con.execute("INSERT INTO table SELECT * FROM df")

# Bad - row by row
for _, row in df.iterrows():
    con.execute("INSERT INTO table VALUES (?)", row.tolist())
```

2. **Optimize transformations**:
```python
# Good - vectorized
df['ppg'] = df['points'] / df['games']

# Bad - iterating
for i, row in df.iterrows():
    df.at[i, 'ppg'] = row['points'] / row['games']
```

3. **Process in chunks** (for large files):
```python
chunks = pd.read_csv('large_file.csv', chunksize=10000)
for chunk in chunks:
    process(chunk)
```

---

### Issue: High memory usage

**Symptoms**: Python using >4GB RAM

**Solutions**:

1. **Process in chunks**:
```python
# Don't load entire file at once
for chunk in pd.read_csv(file, chunksize=10000):
    process_chunk(chunk)
```

2. **Select fewer columns**:
```python
# Only read needed columns
df = pd.read_csv(file, usecols=['col1', 'col2', 'col3'])
```

3. **Use appropriate dtypes**:
```python
# Use smaller types
df['age'] = df['age'].astype('int8')  # Instead of int64
df['category'] = df['category'].astype('category')  # For repeated strings
```

4. **Set DuckDB memory limit**:
```python
con.execute("SET memory_limit='2GB'")
```

---

## Data Quality Issues

### Issue: Unexpected NULL values

**Symptoms**: More NULLs than expected

**Debug**:
```sql
-- Check NULL counts
SELECT 
    COUNT(*) as total,
    COUNT(*) - COUNT(column_name) as nulls,
    (COUNT(*) - COUNT(column_name)) * 100.0 / COUNT(*) as null_percent
FROM players;

-- Find rows with NULLs
SELECT * FROM players WHERE column_name IS NULL LIMIT 10;

-- Check if 'NA' strings exist
SELECT COUNT(*) FROM players WHERE column_name = 'NA';
```

**Solutions**:
```python
# Convert 'NA' strings to NULL in transform
df = df.replace(['NA', 'N/A', 'null', ''], None)

# Or fill NULLs if appropriate
df['column'] = df['column'].fillna(0)
```

---

### Issue: Duplicate records

**Symptoms**: Same record appears multiple times

**Debug**:
```sql
-- Find duplicates
SELECT player_id, season, team, COUNT(*)
FROM players
GROUP BY player_id, season, team
HAVING COUNT(*) > 1;

-- Check for TOT records
SELECT COUNT(*) FROM players WHERE team = 'TOT';
```

**Solutions**:
```python
# Remove duplicates in transform
df = df.drop_duplicates(subset=['player_id', 'season', 'team'])

# Remove TOT records
df = df[df['team'] != 'TOT']
```

---

### Issue: Incorrect calculations

**Symptoms**: Derived metrics don't match expectations

**Debug**:
```sql
-- Verify calculations
SELECT 
    player,
    points, games, ppg,
    points / games as calculated_ppg,
    ABS(ppg - (points / games)) as difference
FROM players
WHERE games > 0
LIMIT 10;
```

**Solutions**:
```python
# Check for division by zero
df['ppg'] = df['points'] / df['games']
df['ppg'] = df['ppg'].replace([float('inf'), -float('inf')], None)

# Verify formula
# TS% = PTS / (2 * (FGA + 0.44 * FTA))
df['ts_percent'] = df['pts'] / (2 * (df['fga'] + 0.44 * df['fta']))
```

---

## Getting More Help

### Enable Debug Logging

```python
import logging

# Set to DEBUG level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Check Logs

```bash
# ETL logs show transformation details
python -m etl.pipeline 2>&1 | tee etl.log

# Dashboard logs show query performance
python nba_dashboard_duckdb.py 2>&1 | tee dashboard.log
```

### Verify Environment

```bash
# Check Python version
python --version  # Should be 3.9+

# Check installed packages
pip list

# Check DuckDB version
python -c "import duckdb; print(duckdb.__version__)"

# Check file locations
ls -R data/
```

### Test Components Individually

```python
# Test extract
from etl.extract import extract_data
df = extract_data('NBA_Player_Totals.csv')
print(f"Extracted {len(df)} rows")

# Test transform
from etl.transform import transform_data
df_clean = transform_data(df)
print(f"Transformed to {len(df_clean)} rows")

# Test database connection
import duckdb
con = duckdb.connect('data/duckdb/nba.db')
print(con.execute("SELECT COUNT(*) FROM players").fetchone()[0])
```

---

## Quick Diagnostic Commands

```bash
# Check if ETL ran successfully
python -c "import duckdb; con = duckdb.connect('data/duckdb/nba.db'); print(f'{con.execute(\"SELECT COUNT(*) FROM players\").fetchone()[0]:,} rows')"

# Check if indexes exist
python -c "import duckdb; con = duckdb.connect('data/duckdb/nba.db'); print(con.execute('SELECT * FROM duckdb_indexes()').fetchdf())"

# Check file sizes
ls -lh data/raw/
ls -lh data/duckdb/
ls -lh data/processed/

# Test dashboard connection
python -c "from dash import Dash; print('✅ Dash installed')"
```

---

## Still Stuck?

1. **Check documentation**:
   - [Implementation Guide](../implementation_guide.md)
   - [ETL Pattern Guide](../etl_pattern_guide.md)
   - [Architecture](../architecture.md)

2. **Review examples**:
   - [SQL Queries](../../sql/queries.sql)
   - [Data Dictionary](../data_dictionary.md)

3. **Verify setup**:
   - Run through [Quick Start](quickstart.md) again
   - Check all files are in correct locations
   - Ensure virtual environment is activated

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Covers**: Common issues in setup, ETL, database, and dashboard
