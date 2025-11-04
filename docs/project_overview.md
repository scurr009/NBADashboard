# Project Overview

## Objective

Build a scalable ETL pipeline and interactive dashboard for NBA player performance analytics.

## Architecture

### Data Flow

```
Raw CSV → Extract → Transform → Load → DuckDB → Dashboard
```

1. **Extract**: Read CSV from `data/raw/`
2. **Transform**: Clean, validate, and enrich data
3. **Load**: Store in DuckDB with indexes
4. **Dashboard**: Query and visualize via Dash

## Data Quality Issues to Address

Based on initial analysis of `NBA_Player_Totals.csv`:

### Missing Values
- `birth_year`: All values are NA
- Percentage fields: Some NA values
- Solution: Convert NA strings to NULL, handle in queries

### Data Inconsistencies
- **Team 'TOT'**: Represents players traded mid-season (aggregate stats)
- **Position variations**: PG, SG-PG, PF-SF, etc.
- **Percentage ranges**: Should be 0-1, need validation

### Duplicates
- Players with multiple team entries per season (trades)
- Need deduplication strategy

## ETL Pipeline Design

### Extract (`etl/extract.py`)
- Read CSV with proper encoding
- Validate file structure
- Log metadata (rows, columns, size)

### Transform (`etl/transform.py`)
- Replace 'NA' strings with NULL
- Validate percentage ranges (0-1)
- Standardize position codes
- Calculate derived metrics (PER, TS%, etc.)
- Flag data quality issues

### Load (`etl/load.py`)
- Create DuckDB database
- Define schema with proper types
- Create indexes on: season, team, position, player
- Export to Parquet for performance
- Generate data quality report

## Dashboard Features

### Filters
- Season range slider
- Team dropdown
- Position dropdown
- Player search

### Visualizations
- Line chart: Player performance over time
- Top 10 rankings by selected metric
- Query performance metrics

### Metrics Available
- Points per game (PPG)
- Rebounds per game (RPG)
- Assists per game (APG)
- Field goal percentage
- 3-point percentage
- And more...

## Performance Considerations

- **DuckDB**: Columnar storage, optimized for analytics
- **Parquet**: 10x faster than CSV
- **Indexes**: Fast filtering on common columns
- **Query optimization**: CTEs, proper WHERE clauses

## Next Steps

1. Build ETL pipeline modules
2. Refactor existing dashboard code
3. Add data validation tests
4. Create data dictionary
5. Add more visualizations
