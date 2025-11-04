-- Common NBA Player Queries
-- Use these queries with the cleaned DuckDB database

-- ============================================================================
-- TOP PERFORMERS
-- ============================================================================

-- Top 10 scorers all-time (career PPG, min 100 games)
SELECT 
    player,
    player_id,
    COUNT(*) as seasons,
    SUM(g) as total_games,
    AVG(ppg) as career_ppg,
    SUM(pts) as career_points
FROM players
GROUP BY player, player_id
HAVING SUM(g) >= 100
ORDER BY career_ppg DESC
LIMIT 10;

-- Top 10 scorers by season
SELECT 
    season,
    player,
    player_id,
    tm,
    pos,
    g,
    ppg,
    pts
FROM players
WHERE season = 2025
ORDER BY ppg DESC
LIMIT 10;

-- ============================================================================
-- POSITION ANALYSIS
-- ============================================================================

-- Average stats by position (current season)
SELECT 
    pos,
    COUNT(*) as player_count,
    ROUND(AVG(ppg), 2) as avg_ppg,
    ROUND(AVG(rpg), 2) as avg_rpg,
    ROUND(AVG(apg), 2) as avg_apg,
    ROUND(AVG(fg_percent), 3) as avg_fg_pct
FROM players
WHERE season = 2025 AND g >= 10
GROUP BY pos
ORDER BY pos;

-- ============================================================================
-- TEAM ANALYSIS
-- ============================================================================

-- Team roster and stats (specific season)
SELECT 
    player,
    player_id,
    pos,
    age,
    g,
    ppg,
    rpg,
    apg
FROM players
WHERE season = 2025 AND tm = 'LAL'
ORDER BY ppg DESC;

-- ============================================================================
-- PLAYER CAREER PROGRESSION
-- ============================================================================

-- Single player career stats
SELECT 
    season,
    tm,
    pos,
    age,
    g,
    ppg,
    rpg,
    apg,
    fg_percent,
    x3p_percent
FROM players
WHERE player_id = 4066  -- Anthony Davis
ORDER BY season;

-- ============================================================================
-- SHOOTING EFFICIENCY
-- ============================================================================

-- Best shooters (min 100 3PA, current season)
SELECT 
    player,
    player_id,
    tm,
    pos,
    x3pa as attempts,
    x3p as makes,
    ROUND(x3p_percent, 3) as pct
FROM players
WHERE season = 2025 AND x3pa >= 100
ORDER BY x3p_percent DESC
LIMIT 20;

-- True shooting percentage leaders
SELECT 
    player,
    player_id,
    tm,
    pos,
    g,
    ppg,
    ROUND(ts_percent, 3) as ts_pct
FROM players
WHERE season = 2025 AND g >= 20
ORDER BY ts_percent DESC
LIMIT 20;

-- ============================================================================
-- HISTORICAL TRENDS
-- ============================================================================

-- Average PPG by decade
SELECT 
    FLOOR(season / 10) * 10 as decade,
    COUNT(DISTINCT player_id) as unique_players,
    ROUND(AVG(ppg), 2) as avg_ppg,
    ROUND(AVG(x3p_percent), 3) as avg_3pt_pct
FROM players
WHERE g >= 20
GROUP BY decade
ORDER BY decade;

-- ============================================================================
-- ADVANCED QUERIES
-- ============================================================================

-- Players who improved PPG most year-over-year
WITH yearly_stats AS (
    SELECT 
        player_id,
        player,
        season,
        ppg,
        LAG(ppg) OVER (PARTITION BY player_id ORDER BY season) as prev_ppg
    FROM players
    WHERE g >= 20
)
SELECT 
    player,
    player_id,
    season,
    ROUND(ppg, 2) as current_ppg,
    ROUND(prev_ppg, 2) as previous_ppg,
    ROUND(ppg - prev_ppg, 2) as improvement
FROM yearly_stats
WHERE prev_ppg IS NOT NULL
ORDER BY improvement DESC
LIMIT 20;

-- Most consistent players (lowest PPG standard deviation, min 5 seasons)
SELECT 
    player,
    player_id,
    COUNT(*) as seasons,
    ROUND(AVG(ppg), 2) as avg_ppg,
    ROUND(STDDEV(ppg), 2) as ppg_stddev
FROM players
WHERE g >= 20
GROUP BY player, player_id
HAVING COUNT(*) >= 5
ORDER BY ppg_stddev ASC
LIMIT 20;

-- ============================================================================
-- DATA QUALITY CHECKS
-- ============================================================================

-- Check for missing values
SELECT 
    'birth_year' as column_name,
    COUNT(*) - COUNT(birth_year) as null_count,
    ROUND((COUNT(*) - COUNT(birth_year)) * 100.0 / COUNT(*), 2) as null_pct
FROM players
UNION ALL
SELECT 
    'x3p_percent',
    COUNT(*) - COUNT(x3p_percent),
    ROUND((COUNT(*) - COUNT(x3p_percent)) * 100.0 / COUNT(*), 2)
FROM players
UNION ALL
SELECT 
    'fg_percent',
    COUNT(*) - COUNT(fg_percent),
    ROUND((COUNT(*) - COUNT(fg_percent)) * 100.0 / COUNT(*), 2)
FROM players;

-- Verify no TOT records remain
SELECT COUNT(*) as tot_count
FROM players
WHERE tm = 'TOT';  -- Should be 0

-- Position distribution
SELECT pos, COUNT(*) as count
FROM players
GROUP BY pos
ORDER BY pos;
