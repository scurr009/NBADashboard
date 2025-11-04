"""
Data transformation module for NBA player statistics
Cleans and standardizes raw data for analysis
"""
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Position consolidation mapping (5 standard positions)
POSITION_MAP = {
    # Point Guards
    'PG': 'PG',
    'PG-SG': 'PG',
    'PG-SF': 'PG',
    
    # Shooting Guards
    'SG': 'SG',
    'SG-PG': 'SG',
    'SG-SF': 'SG',
    'SG-PF': 'SG',
    'SG-PG-SF': 'SG',
    
    # Small Forwards
    'SF': 'SF',
    'SF-PG': 'SF',
    'SF-SG': 'SF',
    'SF-PF': 'SF',
    'SF-C': 'SF',
    
    # Power Forwards
    'PF': 'PF',
    'PF-C': 'PF',
    'PF-SF': 'PF',
    
    # Centers
    'C': 'C',
    'C-F': 'C',
    'C-PF': 'C',
    'C-SF': 'C',
    
    # Generic positions (map to most common)
    'F': 'SF',      # Generic forward → Small Forward
    'F-C': 'PF',    # Forward-Center → Power Forward
    'F-G': 'SF',    # Forward-Guard → Small Forward
    'G': 'SG',      # Generic guard → Shooting Guard
    'G-F': 'SG'     # Guard-Forward → Shooting Guard
}


def remove_tot_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove TOT (Total) records for traded players
    
    Args:
        df: Raw dataframe
        
    Returns:
        Dataframe without TOT records
    """
    initial_count = len(df)
    df_clean = df[df['tm'] != 'TOT'].copy()
    removed_count = initial_count - len(df_clean)
    
    logger.info(f"Removed {removed_count:,} TOT records ({removed_count/initial_count*100:.1f}%)")
    logger.info(f"Remaining rows: {len(df_clean):,}")
    
    return df_clean


def consolidate_positions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Consolidate 25 position variations into 5 standard positions
    
    Args:
        df: Dataframe with original positions
        
    Returns:
        Dataframe with consolidated positions
    """
    df = df.copy()
    
    # Map positions
    df['pos_original'] = df['pos']  # Keep original for reference
    df['pos'] = df['pos_original'].map(POSITION_MAP)
    
    # Check for unmapped positions
    unmapped = df[df['pos'].isnull()]['pos_original'].unique()
    if len(unmapped) > 0:
        logger.warning(f"Unmapped positions found: {unmapped}")
        raise ValueError(f"Unmapped positions: {unmapped}")
    
    # Add position group
    position_groups = {
        'PG': 'Guard',
        'SG': 'Guard',
        'SF': 'Forward',
        'PF': 'Forward',
        'C': 'Center'
    }
    df['pos_group'] = df['pos'].map(position_groups)
    
    logger.info("Position consolidation complete:")
    logger.info(f"\n{df['pos'].value_counts().sort_index()}")
    
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values and 'NA' strings
    
    Args:
        df: Dataframe with missing values
        
    Returns:
        Dataframe with cleaned missing values
    """
    df = df.copy()
    
    # Replace 'NA' strings with actual NULL
    df = df.replace('NA', None)
    
    # Log missing value summary
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    
    if len(missing) > 0:
        logger.info("Missing values after cleaning:")
        for col, count in missing.head(10).items():
            pct = count / len(df) * 100
            logger.info(f"  {col}: {count:,} ({pct:.1f}%)")
    
    return df


def validate_player_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate player_id integrity
    
    Args:
        df: Dataframe to validate
        
    Returns:
        Validated dataframe
    """
    df = df.copy()
    
    # Check for NULL player_ids
    null_ids = df['player_id'].isnull().sum()
    if null_ids > 0:
        logger.error(f"Found {null_ids} NULL player_ids")
        raise ValueError("player_id cannot be NULL")
    
    # Check for duplicate (player_id, season, tm) combinations
    duplicates = df.duplicated(subset=['player_id', 'season', 'tm'], keep=False)
    if duplicates.any():
        dup_count = duplicates.sum()
        logger.warning(f"Found {dup_count} duplicate (player_id, season, tm) combinations")
        logger.warning("Sample duplicates:")
        logger.warning(df[duplicates][['player', 'player_id', 'season', 'tm']].head())
    
    # Log player name duplicates (informational)
    name_dupes = df.groupby('player')['player_id'].nunique()
    multi_id_players = name_dupes[name_dupes > 1]
    logger.info(f"Players with duplicate names: {len(multi_id_players)}")
    if len(multi_id_players) > 0:
        logger.info(f"Examples: {list(multi_id_players.head().index)}")
    
    return df


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add calculated metrics for analysis
    
    Args:
        df: Dataframe with base stats
        
    Returns:
        Dataframe with derived metrics
    """
    df = df.copy()
    
    # Per-game stats (already exist in some cases, but recalculate for consistency)
    df['ppg'] = df['pts'] / df['g']
    df['rpg'] = df['trb'] / df['g']
    df['apg'] = df['ast'] / df['g']
    df['mpg'] = df['mp'] / df['g']
    
    # True Shooting Percentage: TS% = PTS / (2 * (FGA + 0.44 * FTA))
    df['ts_percent'] = df['pts'] / (2 * (df['fga'] + 0.44 * df['fta']))
    df['ts_percent'] = df['ts_percent'].replace([float('inf'), -float('inf')], None)
    
    logger.info("Added derived metrics: ppg, rpg, apg, mpg, ts_percent")
    
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main transformation pipeline
    
    Args:
        df: Raw dataframe from CSV
        
    Returns:
        Cleaned and transformed dataframe
    """
    logger.info("="*70)
    logger.info("STARTING DATA TRANSFORMATION")
    logger.info("="*70)
    logger.info(f"Initial rows: {len(df):,}")
    
    # Step 1: Remove TOT records
    logger.info("\n[1/5] Removing TOT records...")
    df = remove_tot_records(df)
    
    # Step 2: Consolidate positions
    logger.info("\n[2/5] Consolidating positions...")
    df = consolidate_positions(df)
    
    # Step 3: Handle missing values
    logger.info("\n[3/5] Handling missing values...")
    df = handle_missing_values(df)
    
    # Step 4: Validate player IDs
    logger.info("\n[4/5] Validating player IDs...")
    df = validate_player_ids(df)
    
    # Step 5: Add derived metrics
    logger.info("\n[5/5] Adding derived metrics...")
    df = add_derived_metrics(df)
    
    logger.info("\n" + "="*70)
    logger.info("TRANSFORMATION COMPLETE")
    logger.info("="*70)
    logger.info(f"Final rows: {len(df):,}")
    logger.info(f"Final columns: {len(df.columns)}")
    
    return df


if __name__ == '__main__':
    # Test transformation
    import os
    
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(script_dir, 'data', 'raw', 'NBA_Player_Totals.csv')
    
    print("Loading data...")
    df = pd.read_csv(csv_path)
    
    print("\nTransforming data...")
    df_clean = transform_data(df)
    
    print("\n" + "="*70)
    print("SAMPLE OUTPUT")
    print("="*70)
    print(df_clean[['player', 'player_id', 'season', 'tm', 'pos', 'pos_group', 'ppg']].head(10))
