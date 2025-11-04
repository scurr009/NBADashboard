# Architecture & Design Decisions
## DuckDB ETL + Dashboard Template

**Last Updated**: November 2025  
**Project**: NBA Player Performance Dashboard  
**Purpose**: Document architectural decisions for reusable template

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Technology Stack](#technology-stack)
3. [Architecture Overview](#architecture-overview)
4. [Design Decisions](#design-decisions)
5. [Scalability Considerations](#scalability-considerations)
6. [Trade-offs & Alternatives](#trade-offs--alternatives)
7. [Future Considerations](#future-considerations)

---

## Executive Summary

This template provides a **production-ready pattern** for building analytics pipelines with interactive dashboards, optimized for datasets ranging from thousands to billions of rows.

### Key Characteristics
- **Embedded analytics**: Single-machine deployment
- **OLAP-optimized**: Read-heavy analytical queries
- **Scalable**: Handles large datasets efficiently
- **Fast development**: Python-native, minimal infrastructure
- **Maintainable**: Clear separation of concerns

### Use Cases
✅ Business intelligence dashboards  
✅ Data exploration tools  
✅ Analytics prototypes → production  
✅ Time-series analysis  
✅ Reporting applications  

❌ Transactional systems (OLTP)  
❌ Real-time streaming  
❌ Multi-user write-heavy apps  
❌ Distributed computing requirements  

---

## Technology Stack

### Core Technologies

#### 1. **DuckDB** - Analytical Database
**Version**: 0.9.0+

**Why DuckDB?**
- **Embedded**: No separate server process, runs in-process
- **OLAP-optimized**: Columnar storage, vectorized execution
- **SQL interface**: Standard SQL, easy to query
- **Fast**: Optimized for analytical workloads
- **Scalable**: Handles billions of rows on single machine
- **Zero-config**: No installation or setup required

**Alternatives Considered**:
- **SQLite**: OLTP-focused, row-based, slower for analytics
- **PostgreSQL**: Requires server, overkill for embedded use
- **Pandas only**: Memory-limited, no SQL, slower queries
- **Spark**: Too heavy for single-machine, complex setup

**Decision**: DuckDB provides best balance of performance, simplicity, and scalability for embedded analytics.

---

#### 2. **Parquet** - Storage Format
**Library**: PyArrow 14.0+

**Why Parquet?**
- **Columnar**: Only read columns you need
- **Compressed**: 60-80% smaller than CSV
- **Fast**: 10-100x faster reads than CSV
- **Typed**: Preserves data types
- **Standard**: Widely supported format

**Alternatives Considered**:
- **CSV**: Human-readable but slow, large, untyped
- **JSON**: Flexible but inefficient for tabular data
- **Feather**: Fast but less compression
- **HDF5**: Good for arrays, overkill for tables

**Decision**: Parquet offers best performance and compression for analytical data.

---

#### 3. **Pandas** - Data Manipulation
**Version**: 2.0.0+

**Why Pandas?**
- **Familiar**: Industry-standard Python library
- **Rich API**: Comprehensive data manipulation
- **Integration**: Works seamlessly with DuckDB
- **Ecosystem**: Extensive library support

**Alternatives Considered**:
- **Polars**: Faster but less mature ecosystem
- **Dask**: For distributed computing (not needed)
- **PySpark**: Too heavy for single-machine

**Decision**: Pandas provides best balance of functionality and familiarity.

---

#### 4. **Dash + Plotly** - Dashboard Framework
**Versions**: Dash 2.14.0+, Plotly 5.18.0+

**Why Dash?**
- **Python-native**: No JavaScript required
- **Reactive**: Automatic UI updates
- **Plotly integration**: Rich visualizations
- **Production-ready**: Used by enterprises
- **Customizable**: Full control over layout

**Alternatives Considered**:
- **Streamlit**: Simpler but less control, rerun model
- **Bokeh**: More complex API
- **Flask + Chart.js**: More work, requires JavaScript
- **Tableau/PowerBI**: Not code-based, licensing costs

**Decision**: Dash provides best balance of power and Python-native development.

---

## Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│                  (Dash Dashboard)                        │
│  • Interactive filters                                   │
│  • Real-time visualizations                              │
│  • User interface                                        │
└────────────────────┬────────────────────────────────────┘
                     │ SQL Queries
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     DATA LAYER                           │
│                   (DuckDB + Parquet)                     │
│  • Indexed database                                      │
│  • Optimized storage                                     │
│  • Query engine                                          │
└────────────────────┬────────────────────────────────────┘
                     │ ETL Pipeline
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                       │
│                   (ETL Pipeline)                         │
│  • Extract: Data ingestion                               │
│  • Transform: Cleaning & enrichment                      │
│  • Load: Database population                             │
└────────────────────┬────────────────────────────────────┘
                     │ Raw Data
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    SOURCE LAYER                          │
│              (CSV, APIs, Databases)                      │
│  • Raw data files                                        │
│  • External systems                                      │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
Raw CSV → Extract → Transform → Load → DuckDB → Dashboard
                                   ↓
                               Parquet (optional fast path)
```

### Folder Structure Rationale

```
project/
├── data/           # Data isolation
│   ├── raw/        # Immutable source data
│   ├── processed/  # Transformed data (Parquet)
│   └── duckdb/     # Database files
├── etl/            # Business logic separation
├── dashboard/      # Presentation layer
├── sql/            # Query reusability
├── tests/          # Quality assurance
├── docs/           # Knowledge management
└── skills/         # Best practices
```

**Principles**:
- **Separation of concerns**: Each folder has single purpose
- **Data isolation**: Raw data never modified
- **Modularity**: Components can be developed independently
- **Testability**: Clear boundaries for testing
- **Scalability**: Easy to add new components

---

## Design Decisions

### 1. **ETL Pattern: Extract → Transform → Load**

**Decision**: Separate ETL into three distinct phases

**Rationale**:
- **Modularity**: Each phase can be developed/tested independently
- **Reusability**: Transform logic can be reused across projects
- **Debugging**: Easy to isolate issues to specific phase
- **Flexibility**: Can swap extraction sources without changing transform

**Implementation**:
```python
# etl/extract.py - Data ingestion
# etl/transform.py - Business logic
# etl/load.py - Database operations
# etl/pipeline.py - Orchestration
```

---

### 2. **Player ID as Primary Key**

**Decision**: Use `player_id` instead of player name for all operations

**Rationale**:
- **161 players have duplicate names** (e.g., 3 different "Charles Smith")
- Names can change (trades, corrections)
- IDs are stable and unique
- Prevents data integrity issues

**Impact**:
- All queries filter by `player_id`
- UI shows names but filters by ID
- Joins use `player_id`

---

### 3. **Position Consolidation: 25 → 5**

**Decision**: Map 25 position variations to 5 standard positions

**Rationale**:
- **Usability**: 25 positions too granular for filtering
- **Analysis**: Easier to compare position groups
- **Consistency**: Standardized across eras
- **Flexibility**: Original position preserved for reference

**Mapping**:
```
PG, SG, SF, PF, C ← Standard positions
PG-SG, SG-PG, etc. ← Mapped to primary position
```

---

### 4. **Remove TOT (Total) Records**

**Decision**: Delete all rows where `tm = 'TOT'`

**Rationale**:
- **Prevents double-counting**: TOT is aggregate of team stats
- **9% of data**: 2,911 duplicate records
- **Data integrity**: Ensures accurate aggregations

**Example**:
```
Player traded mid-season:
✅ Keep: Team A stats (10 games)
✅ Keep: Team B stats (29 games)
❌ Remove: TOT stats (39 games) ← Duplicate
```

---

### 5. **Indexing Strategy**

**Decision**: Create indexes on frequently filtered columns

**Indexes Created**:
- `season` - Time-based filtering
- `player_id` - Player lookups
- `tm` - Team filtering
- `pos` - Position filtering
- `pos_group` - Position group filtering
- `(player_id, season)` - Composite for career queries

**Rationale**:
- **Query performance**: Sub-millisecond filtering
- **User experience**: Instant dashboard updates
- **Scalability**: Maintains performance at scale

**Trade-off**: Slightly slower writes (not an issue for read-heavy analytics)

---

### 6. **Derived Metrics in Database**

**Decision**: Calculate and store derived metrics (ppg, rpg, apg, ts_percent)

**Rationale**:
- **Performance**: Pre-calculated vs compute on every query
- **Consistency**: Same calculation everywhere
- **Simplicity**: Easier queries
- **Documentation**: Formulas in one place

**Alternative Considered**: Calculate in queries
- **Rejected**: Slower, inconsistent, harder to maintain

---

### 7. **Parquet Export for Performance**

**Decision**: Export cleaned data to Parquet alongside DuckDB

**Rationale**:
- **Speed**: 10-100x faster than CSV
- **Compression**: 60% smaller than CSV
- **Flexibility**: Can use Parquet directly or DuckDB
- **Portability**: Standard format for data exchange

**Use Cases**:
- Fast dashboard loading
- Data sharing
- Backup/archival
- Integration with other tools

---

### 8. **Embedded Database (Not Client-Server)**

**Decision**: Use DuckDB in embedded mode, not as separate server

**Rationale**:
- **Simplicity**: No server to manage
- **Performance**: No network overhead
- **Deployment**: Single executable
- **Development**: Faster iteration

**Trade-off**: Single-user access (acceptable for analytics dashboards)

---

## Scalability Considerations

### Current Performance (NBA Dataset)
- **Rows**: 29,508
- **ETL Time**: 1.48 seconds
- **Storage**: 1.69 MB (Parquet)
- **Query Time**: <10ms with indexes

### Scalability Projections

| Dataset Size | ETL Time | Storage | Query Time | Recommendation |
|--------------|----------|---------|------------|----------------|
| 100K rows | ~5s | ~5 MB | <10ms | ✅ Optimal |
| 1M rows | ~30s | ~50 MB | <50ms | ✅ Optimal |
| 10M rows | ~5min | ~500 MB | <200ms | ✅ Good |
| 100M rows | ~30min | ~5 GB | <1s | ✅ Acceptable |
| 1B rows | ~5hrs | ~50 GB | <5s | ⚠️ Consider partitioning |
| 10B+ rows | - | - | - | ❌ Use distributed system |

### Scaling Strategies

**For 100M+ rows**:
1. **Partitioning**: Partition by year/season
2. **Incremental loads**: Append new data only
3. **Materialized views**: Pre-aggregate common queries
4. **Sampling**: Dashboard shows sample, full data on-demand

**For 1B+ rows**:
1. **Consider distributed system** (Spark, Presto)
2. **Data warehouse** (Snowflake, BigQuery)
3. **Time-based archival**: Move old data to cold storage

---

## Trade-offs & Alternatives

### DuckDB vs Alternatives

| Feature | DuckDB | SQLite | PostgreSQL | Spark |
|---------|--------|--------|------------|-------|
| **Setup** | None | None | Server | Complex |
| **OLAP Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **OLTP Performance** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Scalability** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **SQL Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

**Decision**: DuckDB optimal for embedded analytics use case

---

### Dash vs Alternatives

| Feature | Dash | Streamlit | Bokeh | Flask+JS |
|---------|------|-----------|-------|----------|
| **Python-Native** | ✅ | ✅ | ✅ | Partial |
| **Learning Curve** | Medium | Low | High | High |
| **Customization** | High | Medium | High | Highest |
| **Performance** | Good | Good | Good | Excellent |
| **Production Ready** | ✅ | ⚠️ | ✅ | ✅ |

**Decision**: Dash provides best balance for production dashboards

---

## Future Considerations

### Potential Enhancements

1. **Incremental ETL**
   - Append new data without full reload
   - Track last update timestamp
   - Delta processing

2. **Caching Layer**
   - Cache common queries
   - Redis for distributed caching
   - Reduce database load

3. **Authentication**
   - User login
   - Role-based access
   - Audit logging

4. **Multi-tenancy**
   - Support multiple datasets
   - User-specific views
   - Data isolation

5. **Real-time Updates**
   - WebSocket connections
   - Live data streaming
   - Auto-refresh dashboards

6. **Advanced Analytics**
   - Machine learning integration
   - Predictive analytics
   - Anomaly detection

### Migration Paths

**If outgrow single-machine**:
1. **DuckDB → PostgreSQL**: Similar SQL, add server
2. **DuckDB → Snowflake**: Cloud data warehouse
3. **DuckDB → Spark**: Distributed processing
4. **Hybrid**: DuckDB for recent data, warehouse for historical

---

## Conclusion

This architecture provides a **pragmatic, scalable solution** for embedded analytics:

✅ **Fast development**: Python-native, minimal setup  
✅ **High performance**: Optimized for analytics  
✅ **Scalable**: Handles millions to billions of rows  
✅ **Maintainable**: Clear structure, good separation  
✅ **Production-ready**: Battle-tested technologies  

**Best for**: Analytics dashboards, BI tools, data exploration, prototyping

**Not for**: Transactional systems, real-time streaming, distributed computing

---

## Related Documentation

- [Implementation Guide](implementation_guide.md) - Step-by-step setup
- [ETL Pattern Guide](etl_pattern_guide.md) - Detailed ETL patterns
- [Database Design Guide](database_design.md) - Schema and indexing
- [Template Overview](template_overview.md) - High-level overview

---

**Document Version**: 1.0  
**Last Review**: November 2025  
**Next Review**: Quarterly or after major changes
