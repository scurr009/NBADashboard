# ETL Transformation Plan

## Data Quality Issues Identified

### 1. Player Name Duplicates ✅ CRITICAL
- **Issue**: 161 players have duplicate names with different player_ids
- **Example**: "Charles Smith" has 3 different player_ids
- **Impact**: Queries by name will return wrong/mixed results
- **Solution**: **Use `player_id` as primary key, not `player` name**

### 2. Position Consolidation 🎯 REQUIRED
- **Issue**: 25 different position variations
- **Current**: C, C-F, C-PF, F, F-C, F-G, G, G-F, PF, PF-C, PG, PG-SG, SF, SF-PF, SG, SG-PF, etc.
- **Impact**: Difficult to filter and analyze by position

### 3. Team 'TOT' Records 🗑️ REMOVE
- **Issue**: 2,911 rows (9.0%) have team='TOT' (traded player aggregates)
- **Impact**: Double-counting stats, inflated totals
- **Solution**: **Delete all rows where tm='TOT'**

### 4. Missing Values 📊 HANDLE
- **birth_year**: 29,547 missing (91% of data)
- **3-point stats**: 10,563 missing (pre-1980 era)
- **Other stats**: Various missing values
- **Solution**: Keep as NULL, handle in queries

---

## Proposal 1: Position Consolidation

### Option A: 5 Primary Positions (RECOMMENDED)

Map all variations to 5 standard positions based on **primary position**:

| New Position | Includes Original Positions | Count | Description |
|--------------|----------------------------|-------|-------------|
| **PG** | PG, PG-SG, PG-SF | 5,995 | Point Guard |
| **SG** | SG, SG-PG, SG-SF, SG-PF, SG-PG-SF | 6,627 | Shooting Guard |
| **SF** | SF, SF-PG, SF-SG, SF-PF, SF-C | 6,147 | Small Forward |
| **PF** | PF, PF-C, PF-SF | 6,451 | Power Forward |
| **C** | C, C-F, C-PF, C-SF | 6,292 | Center |

**Mapping Logic:**
```python
position_map = {
    'PG': 'PG', 'PG-SG': 'PG', 'PG-SF': 'PG',
    'SG': 'SG', 'SG-PG': 'SG', 'SG-SF': 'SG', 'SG-PF': 'SG', 'SG-PG-SF': 'SG',
    'SF': 'SF', 'SF-PG': 'SF', 'SF-SG': 'SF', 'SF-PF': 'SF', 'SF-C': 'SF',
    'PF': 'PF', 'PF-C': 'PF', 'PF-SF': 'PF',
    'C': 'C', 'C-F': 'C', 'C-PF': 'C', 'C-SF': 'C',
    'F': 'SF', 'F-C': 'PF', 'F-G': 'SF',  # Generic forwards
    'G': 'SG'  # Generic guard
}
```

### Option B: 3 Position Groups (ALTERNATIVE)

Simpler grouping:

| Position Group | Includes | Description |
|----------------|----------|-------------|
| **Guard** | PG, SG, G, all guard combos | Backcourt |
| **Forward** | SF, PF, F, all forward combos | Frontcourt wings |
| **Center** | C, all center combos | Frontcourt bigs |

**Recommendation: Option A (5 positions)** - Better granularity while still being manageable.

---

## Proposal 2: Player ID Strategy

### Implementation

1. **Primary Key**: Use `player_id` for all joins and aggregations
2. **Display Name**: Keep `player` for UI display only
3. **Unique Constraint**: Enforce `(player_id, season, tm)` uniqueness after TOT removal

### Query Pattern Change

**Before:**
```sql
WHERE player = 'Charles Smith'  -- Returns 3 different players!
```

**After:**
```sql
WHERE player_id = 3047  -- Returns specific Charles Smith
```

### Dashboard Impact

- Dropdown should show: `"Charles Smith (ID: 3047)"` or similar
- Backend filters by `player_id`
- Handles duplicate names correctly

---

## Proposal 3: TOT Record Removal

### Strategy

**Remove all rows where `tm = 'TOT'`**

### Rationale

When a player is traded mid-season:
- Original team stats: Keep ✅
- New team stats: Keep ✅
- TOT (aggregate): Remove ❌ (prevents double-counting)

### Example: D'Angelo Russell 2025

**Before Removal:**
```
season  tm   g   pts
2025    BRK  10  149
2025    LAL  29  359
2025    TOT  39  508  ← Remove this
```

**After Removal:**
```
season  tm   g   pts
2025    BRK  10  149  ← Keep
2025    LAL  29  359  ← Keep
```

### Impact

- Removes 2,911 rows (9.0%)
- Final dataset: ~29,508 rows
- Prevents stat inflation in aggregations

---

## Transformation Pipeline

### Step 1: Filter TOT Records
```python
df = df[df['tm'] != 'TOT']
```

### Step 2: Consolidate Positions
```python
df['pos_clean'] = df['pos'].map(position_map)
```

### Step 3: Validate Player IDs
```python
# Ensure player_id is primary identifier
df = df.sort_values(['player_id', 'season', 'tm'])
```

### Step 4: Handle Missing Values
```python
# Convert 'NA' strings to NULL
df = df.replace('NA', None)
```

### Step 5: Add Derived Columns
```python
# Add position group (optional)
df['pos_group'] = df['pos_clean'].map({
    'PG': 'Guard', 'SG': 'Guard',
    'SF': 'Forward', 'PF': 'Forward',
    'C': 'Center'
})
```

---

## Data Quality Checks

After transformation, validate:

1. ✅ No `tm = 'TOT'` records remain
2. ✅ All positions mapped to 5 standard values
3. ✅ `player_id` is never NULL
4. ✅ No duplicate `(player_id, season, tm)` combinations
5. ✅ Row count reduced by ~9%

---

## Next Steps

1. Implement `etl/transform.py` with these rules
2. Update dashboard to use `player_id` instead of `player`
3. Update dropdown to show player names with disambiguation
4. Add data quality tests
5. Document position mapping in data dictionary
