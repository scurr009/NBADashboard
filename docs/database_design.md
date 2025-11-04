# Database Design Guide
## DuckDB Schema Design and Optimization

**Target Audience**: Database designers, backend developers  
**Purpose**: Guide for designing efficient DuckDB schemas

---

## Table of Contents
1. [Schema Design Principles](#schema-design-principles)
2. [Data Type Selection](#data-type-selection)
3. [Indexing Strategy](#indexing-strategy)
4. [Query Optimization](#query-optimization)
5. [Performance Tuning](#performance-tuning)
6. [Best Practices](#best-practices)

---

## Schema Design Principles

### 1. Denormalization for Analytics

**OLAP vs OLTP**:
- **OLTP** (Transactional): Normalized, avoid redundancy
- **OLAP** (Analytical): Denormalized, optimize for reads

**For analytics, prefer denormalization**:

```sql
-- Good for analytics (denormalized)
CREATE TABLE player_stats (
    player_id INTEGER,
    player_name VARCHAR,      -- Denormalized
    team_name VARCHAR,         -- Denormalized
    season INTEGER,
    points INTEGER,
    ...
)

-- Traditional OLTP (normalized) - slower for analytics
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name VARCHAR
)

CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR
)

CREATE TABLE stats (
    stat_id INTEGER PRIMARY KEY,
    player_id INTEGER REFERENCES players,
    team_id INTEGER REFERENCES teams,
    ...
)
```

**Why denormalize?**:
- Fewer joins = faster queries
- Simpler queries
- Better for columnar storage
- Acceptable redundancy for read-heavy workloads

---

### 2. Choose Appropriate Grain

**Grain**: What does one row represent?

**Examples**:
- One row per player per season per team ✅ (NBA example)
- One row per order line item ✅
- One row per daily metric ✅
- One row per transaction ✅

**Too fine**: One row per second (unless needed)  
**Too coarse**: One row per year (loses detail)

**Document your grain**:
```sql
-- Table: player_stats
-- Grain: One row per player per season per team
-- Note: Players traded mid-season have multiple rows
CREATE TABLE player_stats (...)
```

---

### 3. Include Derived Metrics

**Pre-calculate common metrics**:

```sql
CREATE TABLE sales (
    order_id VARCHAR,
    quantity INTEGER,
    unit_price DOUBLE,
    discount DOUBLE,
    
    -- Derived metrics (calculated during ETL)
    subtotal DOUBLE,           -- quantity * unit_price
    discount_amount DOUBLE,    -- subtotal * discount
    total DOUBLE,              -- subtotal - discount_amount
    margin_percent DOUBLE      -- (total - cost) / total
)
```

**Benefits**:
- Faster queries (no calculation needed)
- Consistent calculations
- Simpler queries

**Trade-off**: Slightly larger storage (usually worth it)

---

## Data Type Selection

### DuckDB Data Types

| Type | Use For | Size | Example |
|------|---------|------|---------|
| `INTEGER` | Whole numbers | 4 bytes | 42 |
| `BIGINT` | Large integers | 8 bytes | 9223372036854775807 |
| `DOUBLE` | Decimals | 8 bytes | 3.14159 |
| `VARCHAR` | Text | Variable | "Hello" |
| `DATE` | Dates | 4 bytes | 2025-01-15 |
| `TIMESTAMP` | Date + time | 8 bytes | 2025-01-15 10:30:00 |
| `BOOLEAN` | True/False | 1 byte | TRUE |

---

### Type Selection Guidelines

**Integers**:
```sql
-- Use INTEGER for most cases
age INTEGER,              -- -2B to 2B range
season INTEGER,           -- Year values
count INTEGER,            -- Counts

-- Use BIGINT only if needed
user_id BIGINT,          -- Large ID ranges
timestamp_ms BIGINT      -- Unix timestamps in milliseconds
```

**Decimals**:
```sql
-- Use DOUBLE for most decimals
price DOUBLE,            -- Money (if precision not critical)
percentage DOUBLE,       -- 0.0 to 1.0
latitude DOUBLE,         -- Geographic coordinates

-- Use DECIMAL for exact precision
account_balance DECIMAL(15, 2),  -- Financial data
tax_rate DECIMAL(5, 4)           -- Precise percentages
```

**Strings**:
```sql
-- Use VARCHAR for variable-length strings
name VARCHAR,            -- No length limit needed
email VARCHAR,
description VARCHAR,

-- Use CHAR only for fixed-length
country_code CHAR(2),    -- Always 2 characters: "US"
```

**Dates and Times**:
```sql
-- Use DATE for dates without time
birth_date DATE,         -- 1990-05-15
order_date DATE,

-- Use TIMESTAMP for date + time
created_at TIMESTAMP,    -- 2025-01-15 10:30:00
last_login TIMESTAMP
```

---

### Optimize Storage

**Use smallest appropriate type**:

```sql
-- Good - optimized types
CREATE TABLE optimized (
    age TINYINT,           -- 0-255 (1 byte)
    year SMALLINT,         -- -32K to 32K (2 bytes)
    count INTEGER,         -- -2B to 2B (4 bytes)
    id BIGINT              -- Large range (8 bytes)
)

-- Bad - everything as BIGINT
CREATE TABLE wasteful (
    age BIGINT,            -- Wastes 7 bytes per row
    year BIGINT,           -- Wastes 6 bytes per row
    count BIGINT,          -- Wastes 4 bytes per row
    id BIGINT
)
```

**Impact**: For 1M rows, wasteful design uses 17MB more storage

---

## Indexing Strategy

### When to Create Indexes

**Create indexes on columns used in**:
- ✅ WHERE clauses (filtering)
- ✅ JOIN conditions
- ✅ GROUP BY clauses
- ✅ ORDER BY clauses

**Don't index**:
- ❌ Columns rarely queried
- ❌ Columns with low cardinality (few unique values)
- ❌ Very large text columns

---

### Single-Column Indexes

```sql
-- Index frequently filtered columns
CREATE INDEX idx_season ON players(season);
CREATE INDEX idx_team ON players(team);
CREATE INDEX idx_player_id ON players(player_id);

-- Query benefits
SELECT * FROM players 
WHERE season = 2025;  -- Uses idx_season
```

---

### Composite Indexes

**For queries filtering on multiple columns**:

```sql
-- Create composite index
CREATE INDEX idx_player_season ON players(player_id, season);

-- Queries that benefit
SELECT * FROM players 
WHERE player_id = 123 AND season = 2025;  -- Uses idx_player_season

SELECT * FROM players 
WHERE player_id = 123;  -- Also uses idx_player_season (leftmost prefix)

-- Query that doesn't benefit
SELECT * FROM players 
WHERE season = 2025;  -- Doesn't use idx_player_season (not leftmost)
```

**Column order matters**: Put most selective column first

---

### Index Naming Convention

```sql
-- Pattern: idx_{column_names}
CREATE INDEX idx_season ON players(season);
CREATE INDEX idx_player_id ON players(player_id);
CREATE INDEX idx_player_season ON players(player_id, season);
CREATE INDEX idx_team_date ON orders(team, order_date);
```

---

### Index Maintenance

**Check index usage**:
```sql
-- DuckDB doesn't have built-in index stats
-- Monitor query performance to validate indexes

-- Test query with EXPLAIN
EXPLAIN SELECT * FROM players WHERE season = 2025;
```

**When to rebuild**: DuckDB handles this automatically

---

## Query Optimization

### Use Column Selection

```sql
-- Good - select only needed columns
SELECT player_id, player_name, points
FROM players
WHERE season = 2025;

-- Bad - select all columns
SELECT *
FROM players
WHERE season = 2025;
```

**Why**: Columnar storage only reads selected columns

---

### Use WHERE Filters

```sql
-- Good - filter early
SELECT AVG(points)
FROM players
WHERE season = 2025 AND games >= 20;

-- Bad - filter after aggregation
SELECT AVG(points)
FROM (
    SELECT * FROM players WHERE season = 2025
)
WHERE games >= 20;
```

---

### Use CTEs for Readability

```sql
-- Good - readable with CTEs
WITH qualified_players AS (
    SELECT player_id, points, games
    FROM players
    WHERE season = 2025 AND games >= 20
),
player_averages AS (
    SELECT player_id, points / games as ppg
    FROM qualified_players
)
SELECT * FROM player_averages
WHERE ppg > 20
ORDER BY ppg DESC;

-- Bad - nested subqueries
SELECT * FROM (
    SELECT player_id, points / games as ppg
    FROM (
        SELECT player_id, points, games
        FROM players
        WHERE season = 2025 AND games >= 20
    )
)
WHERE ppg > 20
ORDER BY ppg DESC;
```

---

### Optimize Joins

```sql
-- Good - join on indexed columns
SELECT p.player_name, s.points
FROM players p
JOIN stats s ON p.player_id = s.player_id  -- Indexed
WHERE s.season = 2025;

-- Good - filter before joining
WITH recent_stats AS (
    SELECT * FROM stats WHERE season = 2025  -- Filter first
)
SELECT p.player_name, s.points
FROM players p
JOIN recent_stats s ON p.player_id = s.player_id;
```

---

### Use Aggregations Efficiently

```sql
-- Good - aggregate in database
SELECT 
    team,
    AVG(points) as avg_points,
    SUM(rebounds) as total_rebounds
FROM players
WHERE season = 2025
GROUP BY team;

-- Bad - aggregate in Python
-- SELECT * FROM players WHERE season = 2025
-- df.groupby('team').agg({'points': 'mean', 'rebounds': 'sum'})
```

**Why**: Database aggregations are faster (vectorized, optimized)

---

## Performance Tuning

### Analyze Query Performance

```sql
-- Use EXPLAIN to see query plan
EXPLAIN SELECT * FROM players WHERE season = 2025;

-- Use EXPLAIN ANALYZE to see actual execution
EXPLAIN ANALYZE SELECT * FROM players WHERE season = 2025;
```

---

### Partition Large Tables

**For very large tables (100M+ rows)**:

```sql
-- Create partitioned table
CREATE TABLE players_partitioned (
    player_id INTEGER,
    season INTEGER,
    points INTEGER,
    ...
) PARTITION BY (season);

-- Queries only scan relevant partitions
SELECT * FROM players_partitioned 
WHERE season = 2025;  -- Only scans 2025 partition
```

---

### Use Appropriate Batch Sizes

```python
# Good - batch inserts
batch_size = 10000
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    con.execute("INSERT INTO table SELECT * FROM batch")

# Bad - row-by-row inserts
for _, row in df.iterrows():
    con.execute("INSERT INTO table VALUES (?)", row.tolist())
```

---

### Monitor Memory Usage

```python
# Check DuckDB memory usage
con.execute("SELECT * FROM duckdb_memory()").fetchdf()

# Set memory limit if needed
con.execute("SET memory_limit='4GB'")
```

---

## Best Practices

### 1. Document Your Schema

```sql
-- Always include comments
CREATE TABLE players (
    -- Identifiers
    player_id INTEGER NOT NULL,     -- Unique player ID (primary key)
    player_name VARCHAR NOT NULL,   -- Display name
    
    -- Season info
    season INTEGER NOT NULL,        -- Year season ended
    team VARCHAR NOT NULL,          -- 3-letter team code
    
    -- Statistics
    games INTEGER NOT NULL,         -- Games played
    points INTEGER,                 -- Total points scored
    
    -- Derived metrics
    ppg DOUBLE                      -- Points per game (points / games)
);

-- Document grain
-- Grain: One row per player per season per team
-- Note: Traded players have multiple rows per season
```

---

### 2. Use Constraints

```sql
CREATE TABLE players (
    player_id INTEGER NOT NULL,     -- NOT NULL constraint
    season INTEGER NOT NULL,
    games INTEGER CHECK (games > 0), -- CHECK constraint
    ppg DOUBLE CHECK (ppg >= 0)      -- Validate derived metrics
);
```

---

### 3. Version Your Schema

```sql
-- Include version in comments
-- Schema Version: 1.0
-- Last Updated: 2025-01-15
-- Changes: Initial schema

CREATE TABLE players (
    ...
);
```

---

### 4. Test Schema Changes

```python
# Test schema migration
def test_schema_migration():
    # Create old schema
    con.execute("CREATE TABLE players_v1 (...)")
    
    # Migrate to new schema
    con.execute("CREATE TABLE players_v2 (...)")
    con.execute("INSERT INTO players_v2 SELECT ... FROM players_v1")
    
    # Validate
    old_count = con.execute("SELECT COUNT(*) FROM players_v1").fetchone()[0]
    new_count = con.execute("SELECT COUNT(*) FROM players_v2").fetchone()[0]
    assert old_count == new_count
```

---

### 5. Backup Before Changes

```python
# Export before schema changes
con.execute("COPY players TO 'backup_players.parquet' (FORMAT PARQUET)")

# Make changes
con.execute("ALTER TABLE players ...")

# Restore if needed
con.execute("CREATE TABLE players AS SELECT * FROM 'backup_players.parquet'")
```

---

## Common Patterns

### Pattern 1: Slowly Changing Dimensions

**Track historical changes**:

```sql
CREATE TABLE customers (
    customer_id INTEGER,
    customer_name VARCHAR,
    email VARCHAR,
    
    -- SCD Type 2 fields
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);

-- Query current records
SELECT * FROM customers WHERE is_current = TRUE;

-- Query historical state
SELECT * FROM customers 
WHERE '2024-01-15' BETWEEN valid_from AND valid_to;
```

---

### Pattern 2: Fact and Dimension Tables

**Star schema for analytics**:

```sql
-- Fact table (large, many rows)
CREATE TABLE fact_sales (
    sale_id BIGINT,
    date_key INTEGER,          -- FK to dim_date
    customer_key INTEGER,      -- FK to dim_customer
    product_key INTEGER,       -- FK to dim_product
    quantity INTEGER,
    revenue DOUBLE
);

-- Dimension tables (small, descriptive)
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day_of_week VARCHAR
);

CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id VARCHAR,
    customer_name VARCHAR,
    segment VARCHAR
);
```

---

### Pattern 3: Audit Columns

**Track data lineage**:

```sql
CREATE TABLE players (
    -- Business columns
    player_id INTEGER,
    player_name VARCHAR,
    ...
    
    -- Audit columns
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR DEFAULT CURRENT_USER,
    source_system VARCHAR,
    etl_batch_id VARCHAR
);
```

---

## Troubleshooting

### Slow Queries

**Check**:
1. Are indexes created?
2. Are you selecting only needed columns?
3. Are you filtering early?
4. Is the table too large (needs partitioning)?

**Debug**:
```sql
EXPLAIN ANALYZE SELECT ...;
```

---

### High Memory Usage

**Solutions**:
1. Process in batches
2. Select fewer columns
3. Filter earlier
4. Increase memory limit

```python
con.execute("SET memory_limit='8GB'")
```

---

### Index Not Being Used

**Reasons**:
1. Column not in WHERE clause
2. Using function on indexed column: `WHERE YEAR(date) = 2025`
3. Type mismatch
4. Query optimizer chose different plan

**Fix**:
```sql
-- Bad - function on indexed column
WHERE YEAR(order_date) = 2025

-- Good - filter on indexed column directly
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'
```

---

## Related Documentation

- [Architecture](architecture.md) - Why DuckDB
- [ETL Pattern Guide](etl_pattern_guide.md) - Loading patterns
- [Performance Benchmarks](performance_benchmarks.md) - Expected performance

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**DuckDB Version**: 0.9.0+
