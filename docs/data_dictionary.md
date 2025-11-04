# Data Dictionary
## NBA Player Statistics Database

**Database**: `data/duckdb/nba.db`  
**Table**: `players`  
**Last Updated**: November 2025

---

## Table of Contents
1. [Overview](#overview)
2. [Field Definitions](#field-definitions)
3. [Derived Metrics](#derived-metrics)
4. [Data Transformations](#data-transformations)
5. [Data Quality Notes](#data-quality-notes)

---

## Overview

### Table: `players`

**Description**: NBA player season statistics from 1947-2025

**Row Count**: 29,508 (after cleaning)  
**Unique Players**: 5,293  
**Season Range**: 1947-2025  
**Grain**: One row per player per season per team

---

## Field Definitions

### Identifiers

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `seas_id` | INTEGER | Season record ID | 31871 | Unique identifier for each record |
| `season` | INTEGER | Season year | 2025 | Year season ended |
| `player_id` | INTEGER | Unique player identifier | 5025 | **Primary key** - use for all joins |
| `player` | VARCHAR | Player name | "A.J. Green" | Display only - 161 players have duplicate names |

### Demographics

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `birth_year` | INTEGER | Year of birth | 1990 | 91.2% missing (historical data) |
| `age` | INTEGER | Age during season | 25 | Age at start of season |
| `experience` | VARCHAR | Years of experience | "3" | String format |
| `lg` | VARCHAR | League | "NBA" | Always "NBA" in this dataset |

### Position

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `pos` | VARCHAR | Position (standardized) | "SG" | **Consolidated to 5 values**: PG, SG, SF, PF, C |
| `pos_original` | VARCHAR | Original position | "SG-PG" | Preserved from source data |
| `pos_group` | VARCHAR | Position group | "Guard" | **3 groups**: Guard, Forward, Center |

### Team

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `tm` | VARCHAR | Team abbreviation | "MIL" | 3-letter team code. **TOT records removed** |

### Games Played

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `g` | INTEGER | Games played | 39 | Total games in season |
| `gs` | INTEGER | Games started | 4 | 26.6% missing (older data) |
| `mp` | DOUBLE | Minutes played | 844.0 | Total minutes for season |

### Shooting Statistics

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `fg` | INTEGER | Field goals made | 101 | 2-point + 3-point makes |
| `fga` | INTEGER | Field goal attempts | 229 | Total shot attempts |
| `fg_percent` | DOUBLE | Field goal percentage | 0.441 | FG / FGA (0-1 scale) |
| `x3p` | INTEGER | 3-pointers made | 88 | 19.6% missing (pre-1980) |
| `x3pa` | INTEGER | 3-point attempts | 201 | 19.6% missing (pre-1980) |
| `x3p_percent` | DOUBLE | 3-point percentage | 0.438 | 3P / 3PA (0-1 scale), 32.8% missing |
| `x2p` | INTEGER | 2-pointers made | 13 | Calculated: FG - 3P |
| `x2pa` | INTEGER | 2-point attempts | 28 | Calculated: FGA - 3PA |
| `x2p_percent` | DOUBLE | 2-point percentage | 0.464 | 2P / 2PA (0-1 scale) |
| `e_fg_percent` | DOUBLE | Effective FG% | 0.633 | (FG + 0.5 * 3P) / FGA |

### Free Throws

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `ft` | INTEGER | Free throws made | 12 | Successful free throws |
| `fta` | INTEGER | Free throw attempts | 14 | Total free throw attempts |
| `ft_percent` | DOUBLE | Free throw percentage | 0.857 | FT / FTA (0-1 scale) |

### Rebounds

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `orb` | INTEGER | Offensive rebounds | 10 | 14.4% missing (pre-1974) |
| `drb` | INTEGER | Defensive rebounds | 81 | 14.4% missing (pre-1974) |
| `trb` | INTEGER | Total rebounds | 91 | ORB + DRB |

### Other Statistics

| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `ast` | INTEGER | Assists | 48 | Passes leading to baskets |
| `stl` | INTEGER | Steals | 20 | 17.3% missing (pre-1974) |
| `blk` | INTEGER | Blocks | 4 | 17.3% missing (pre-1974) |
| `tov` | INTEGER | Turnovers | 21 | 17.5% missing (pre-1978) |
| `pf` | INTEGER | Personal fouls | 85 | Total fouls committed |
| `pts` | INTEGER | Points | 302 | Total points scored |

---

## Derived Metrics

**Note**: These metrics are calculated during ETL and stored in the database.

### Per-Game Statistics

| Field | Formula | Description | Example |
|-------|---------|-------------|---------|
| `ppg` | `pts / g` | Points per game | 7.74 |
| `rpg` | `trb / g` | Rebounds per game | 2.33 |
| `apg` | `ast / g` | Assists per game | 1.23 |
| `mpg` | `mp / g` | Minutes per game | 21.64 |

### Advanced Metrics

| Field | Formula | Description | Example |
|-------|---------|-------------|---------|
| `ts_percent` | `pts / (2 * (fga + 0.44 * fta))` | True Shooting % | 0.60 |

**True Shooting %**: Measures shooting efficiency accounting for 2P, 3P, and FT

---

## Data Transformations

### Applied During ETL

1. **TOT Record Removal**
   - **Action**: Deleted all rows where `tm = 'TOT'`
   - **Reason**: TOT represents aggregate stats for traded players (prevents double-counting)
   - **Impact**: Removed 2,911 rows (9.0%)

2. **Position Consolidation**
   - **Action**: Mapped 25 position variations → 5 standard positions
   - **Mapping**:
     ```
     PG, PG-SG, PG-SF → PG
     SG, SG-PG, SG-SF, SG-PF, G → SG
     SF, SF-PG, SF-SG, SF-PF, F, F-G → SF
     PF, PF-C, PF-SF, F-C → PF
     C, C-F, C-PF, C-SF → C
     ```
   - **Preserved**: Original position in `pos_original`

3. **Missing Value Handling**
   - **Action**: Converted 'NA' strings to NULL
   - **Fields Affected**: All fields
   - **Reason**: Proper NULL handling in queries

4. **Derived Metrics**
   - **Action**: Calculated per-game stats and advanced metrics
   - **Fields Added**: `ppg`, `rpg`, `apg`, `mpg`, `ts_percent`, `pos_group`

---

## Data Quality Notes

### Missing Data

| Field | Missing % | Reason | Handling |
|-------|-----------|--------|----------|
| `birth_year` | 91.2% | Historical data unavailable | Keep as NULL |
| `x3p_percent` | 32.8% | 3-point line introduced 1979-80 | Keep as NULL |
| `gs` | 26.6% | Not tracked in early years | Keep as NULL |
| `x3p`, `x3pa` | 19.6% | Pre-1980 seasons | Keep as NULL |
| `tov` | 17.5% | Not tracked before 1977-78 | Keep as NULL |
| `stl`, `blk` | 17.3% | Not tracked before 1973-74 | Keep as NULL |
| `orb`, `drb` | 14.4% | Not tracked before 1973-74 | Keep as NULL |

### Data Integrity

- ✅ **No TOT records** - All removed during ETL
- ✅ **No NULL player_ids** - All records have valid player ID
- ✅ **No duplicates** - Unique (player_id, season, tm) combinations
- ✅ **Standardized positions** - All mapped to 5 values

### Known Issues

1. **Duplicate Player Names**
   - 161 players share names with others
   - Examples: Charles Smith (3 IDs), Charles Jones (3 IDs)
   - **Solution**: Always use `player_id` for queries

2. **Historical Stat Availability**
   - Many advanced stats not tracked before 1970s
   - 3-point stats only available from 1979-80 onward
   - **Solution**: Filter by season when analyzing specific stats

3. **Traded Players**
   - Players traded mid-season have multiple rows (one per team)
   - **Solution**: TOT records removed; use individual team stats

---

## Usage Examples

### Query by Player ID (Correct)
```sql
SELECT * FROM players
WHERE player_id = 5025  -- Specific A.J. Green
AND season = 2025;
```

### Query by Name (Risky - may return multiple players)
```sql
SELECT player, player_id, season, tm, ppg
FROM players
WHERE player = 'Charles Smith'  -- Returns 3 different players!
ORDER BY season DESC;
```

### Calculate Career Stats
```sql
SELECT 
    player_id,
    player,
    COUNT(*) as seasons,
    SUM(g) as career_games,
    AVG(ppg) as career_ppg,
    SUM(pts) as career_points
FROM players
GROUP BY player_id, player
HAVING SUM(g) >= 100  -- Minimum games filter
ORDER BY career_ppg DESC;
```

### Filter by Position
```sql
SELECT * FROM players
WHERE pos = 'PG'  -- Standardized position
AND season = 2025
AND g >= 20;
```

---

## Indexes

**Performance optimization indexes created**:

| Index Name | Columns | Purpose |
|------------|---------|---------|
| `idx_season` | `season` | Filter by season |
| `idx_player_id` | `player_id` | Player lookups |
| `idx_team` | `tm` | Filter by team |
| `idx_position` | `pos` | Filter by position |
| `idx_pos_group` | `pos_group` | Filter by position group |
| `idx_player_season` | `player_id, season` | Career queries |

---

## Change History

| Date | Version | Changes |
|------|---------|---------|
| Nov 2025 | 1.0 | Initial data dictionary |

---

## Related Documentation

- [Architecture](architecture.md) - Design decisions
- [ETL Pattern Guide](etl_pattern_guide.md) - Transformation details
- [Transformation Decisions](transformation_decisions.md) - Rationale for changes

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Data Version**: Season 2025 (through November)
