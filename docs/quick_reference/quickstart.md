# Quick Start Guide
## Get Running in 5 Minutes

**Goal**: Set up and run the NBA Dashboard project quickly

---

## Prerequisites

- Python 3.9 or higher
- Git (optional, for cloning)
- 5-10 minutes

---

## Step 1: Get the Code (30 seconds)

```bash
# Clone or download the project
cd path/to/project

# Verify you're in the right directory
ls
# Should see: data/, etl/, dashboard/, docs/, etc.
```

---

## Step 2: Set Up Environment (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully

---

## Step 3: Run ETL Pipeline (1 minute)

```bash
# Run the ETL pipeline
python -m etl.pipeline
```

**Expected output**:
```
======================================================================
ETL PIPELINE STARTING
======================================================================

[1/3] EXTRACT
Reading: C:\...\data\raw\NBA_Player_Totals.csv
Loaded 32,419 rows

[2/3] TRANSFORM
Removed 2,911 TOT records (9.0%)
Position consolidation complete
...

[3/3] LOAD
Loading 29,508 rows into DuckDB...
✅ Loaded 29,508 rows
✅ All indexes created
✅ Exported 1.69 MB

✅ Pipeline executed successfully!
```

**Time**: ~1-2 seconds

---

## Step 4: Launch Dashboard (30 seconds)

```bash
# Start the dashboard
python nba_dashboard_duckdb.py
```

**Expected output**:
```
======================================================================
🏀 NBA Interactive Dashboard - DuckDB Version
======================================================================

📊 Features:
  ✅ DuckDB backend (scalable to billions of rows)
  ✅ Indexed queries for fast filtering
  ...

🌐 Starting dashboard...
   Opening at: http://127.0.0.1:8050/

💡 Press Ctrl+C to stop the server
```

---

## Step 5: Open in Browser (10 seconds)

1. Open your web browser
2. Go to: **http://127.0.0.1:8050/**
3. You should see the NBA Dashboard!

---

## What You Should See

### Dashboard Features:
- **Left Panel**: Filters (metric, season, team, position, player)
- **Right Panel**: Interactive line chart showing top 10 players
- **Performance**: Query times displayed at bottom

### Try These:
1. Change the metric dropdown (PPG, RPG, APG, etc.)
2. Adjust the season range slider
3. Filter by team or position
4. Search for a specific player
5. Hover over lines for details
6. Click legend items to show/hide players

---

## Quick Verification

### Check Database
```bash
# Open DuckDB CLI
duckdb data/duckdb/nba.db

# Run a query
SELECT COUNT(*) FROM players;
# Should return: 29508

# Check a player
SELECT player, season, tm, ppg 
FROM players 
WHERE player_id = 4066 
ORDER BY season DESC 
LIMIT 5;

# Exit
.quit
```

### Check Files
```bash
# Verify files were created
ls data/duckdb/
# Should see: nba.db

ls data/processed/
# Should see: nba_players_clean.parquet
```

---

## Common Issues & Fixes

### Issue: "Module not found"
**Fix**: Make sure virtual environment is activated
```bash
# Check which Python
which python  # Should show venv path

# Reactivate if needed
source venv/bin/activate  # or venv\Scripts\activate
```

### Issue: "File not found: NBA_Player_Totals.csv"
**Fix**: Ensure CSV is in `data/raw/` folder
```bash
ls data/raw/
# Should see: NBA_Player_Totals.csv

# If missing, move it there
mv NBA_Player_Totals.csv data/raw/
```

### Issue: Dashboard won't start
**Fix**: Check if port 8050 is already in use
```bash
# Try a different port
python nba_dashboard_duckdb.py --port 8051
```

### Issue: "Permission denied" on Windows
**Fix**: Run as administrator or use PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Next Steps

Now that you're running:

1. **Explore the Data**
   - Try different filters
   - Look at different metrics
   - Find your favorite players

2. **Learn the Code**
   - Read [Architecture](../architecture.md)
   - Check [Implementation Guide](../implementation_guide.md)
   - Review [ETL Pattern Guide](../etl_pattern_guide.md)

3. **Customize**
   - Add new metrics
   - Change visualizations
   - Adapt for your data

4. **Query the Database**
   - See [SQL Queries](../../sql/queries.sql) for examples
   - Use DuckDB CLI to explore
   - Build custom reports

---

## Useful Commands

```bash
# Run ETL
python -m etl.pipeline

# Run Dashboard
python nba_dashboard_duckdb.py

# Run Tests
pytest tests/ -v

# Analyze Data
python etl/analyze_data.py

# Query Database
duckdb data/duckdb/nba.db

# Check Python Environment
python --version
pip list
```

---

## File Locations

| What | Where |
|------|-------|
| Raw Data | `data/raw/NBA_Player_Totals.csv` |
| Database | `data/duckdb/nba.db` |
| Parquet | `data/processed/nba_players_clean.parquet` |
| ETL Code | `etl/` folder |
| Dashboard | `nba_dashboard_duckdb.py` |
| SQL Queries | `sql/queries.sql` |
| Documentation | `docs/` folder |

---

## Performance Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| ETL Pipeline | ~1.5s | 32K → 29K rows |
| Dashboard Load | <2s | Initial page load |
| Filter Change | <100ms | With indexes |
| Query Execution | <10ms | Typical dashboard query |

---

## Getting Help

1. **Check Documentation**
   - [Architecture](../architecture.md)
   - [Implementation Guide](../implementation_guide.md)
   - [Troubleshooting](troubleshooting.md)

2. **Review Examples**
   - [SQL Queries](../../sql/queries.sql)
   - [ETL Patterns](../etl_pattern_guide.md)

3. **Inspect Logs**
   - ETL logs show transformation details
   - Dashboard shows query performance

---

## Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] ETL pipeline ran successfully
- [ ] Database created (29,508 rows)
- [ ] Parquet file exported
- [ ] Dashboard accessible in browser
- [ ] Filters working
- [ ] Charts displaying

---

**Time to Complete**: 5-10 minutes  
**Difficulty**: Beginner  
**Last Updated**: November 2025

---

## What's Next?

You're now running! Here's what to explore:

- **Understand the Architecture**: Read [architecture.md](../architecture.md)
- **Learn the Patterns**: Check [etl_pattern_guide.md](../etl_pattern_guide.md)
- **Customize**: Follow [implementation_guide.md](../implementation_guide.md)
- **Query**: Try examples in [queries.sql](../../sql/queries.sql)

Happy analyzing! 🏀📊
