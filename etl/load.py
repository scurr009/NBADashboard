"""
Data loading module for NBA player statistics
Loads transformed data into DuckDB with optimized schema and indexes
"""
import duckdb
import pandas as pd
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading data into DuckDB"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize loader
        
        Args:
            db_path: Path to DuckDB database file (defaults to data/duckdb/nba.db)
        """
        if db_path is None:
            script_dir = Path(__file__).parent.parent
            db_dir = script_dir / 'data' / 'duckdb'
            db_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = db_dir / 'nba.db'
        else:
            self.db_path = Path(db_path)
        
        self.con = None
    
    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Connect to DuckDB database
        
        Returns:
            DuckDB connection
        """
        logger.info(f"Connecting to DuckDB: {self.db_path}")
        self.con = duckdb.connect(str(self.db_path))
        return self.con
    
    def create_schema(self) -> None:
        """Create optimized schema for NBA player data"""
        logger.info("Creating schema...")
        
        # Drop existing table if exists
        self.con.execute("DROP TABLE IF EXISTS players")
        
        # Create table with proper types
        create_table_sql = """
        CREATE TABLE players (
            -- Identifiers
            seas_id INTEGER,
            season INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            player VARCHAR NOT NULL,
            birth_year INTEGER,
            
            -- Position
            pos VARCHAR NOT NULL,
            pos_original VARCHAR,
            pos_group VARCHAR,
            
            -- Team & Demographics
            age INTEGER,
            experience VARCHAR,
            lg VARCHAR,
            tm VARCHAR NOT NULL,
            
            -- Games
            g INTEGER NOT NULL,
            gs INTEGER,
            mp DOUBLE,
            
            -- Shooting
            fg INTEGER,
            fga INTEGER,
            fg_percent DOUBLE,
            x3p INTEGER,
            x3pa INTEGER,
            x3p_percent DOUBLE,
            x2p INTEGER,
            x2pa INTEGER,
            x2p_percent DOUBLE,
            e_fg_percent DOUBLE,
            
            -- Free Throws
            ft INTEGER,
            fta INTEGER,
            ft_percent DOUBLE,
            
            -- Rebounds
            orb INTEGER,
            drb INTEGER,
            trb INTEGER,
            
            -- Other Stats
            ast INTEGER,
            stl INTEGER,
            blk INTEGER,
            tov INTEGER,
            pf INTEGER,
            pts INTEGER,
            
            -- Derived Metrics
            ppg DOUBLE,
            rpg DOUBLE,
            apg DOUBLE,
            mpg DOUBLE,
            ts_percent DOUBLE
        )
        """
        
        self.con.execute(create_table_sql)
        logger.info("✅ Schema created")
    
    def load_dataframe(self, df: pd.DataFrame) -> None:
        """
        Load dataframe into DuckDB
        
        Args:
            df: Transformed dataframe to load
        """
        logger.info(f"Loading {len(df):,} rows into DuckDB...")
        
        # Get column order from table
        table_cols = self.con.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'players' ORDER BY ordinal_position"
        ).fetchall()
        table_col_names = [col[0] for col in table_cols]
        
        # Reorder dataframe columns to match table schema
        df_ordered = df[table_col_names]
        
        # Insert data
        self.con.execute("INSERT INTO players SELECT * FROM df_ordered")
        
        # Verify
        count = self.con.execute("SELECT COUNT(*) FROM players").fetchone()[0]
        logger.info(f"✅ Loaded {count:,} rows")
    
    def create_indexes(self) -> None:
        """Create indexes for fast filtering"""
        logger.info("Creating indexes...")
        
        indexes = [
            "CREATE INDEX idx_season ON players(season)",
            "CREATE INDEX idx_player_id ON players(player_id)",
            "CREATE INDEX idx_team ON players(tm)",
            "CREATE INDEX idx_position ON players(pos)",
            "CREATE INDEX idx_pos_group ON players(pos_group)",
            "CREATE INDEX idx_player_season ON players(player_id, season)"
        ]
        
        for idx_sql in indexes:
            self.con.execute(idx_sql)
            logger.info(f"  ✅ {idx_sql.split('INDEX ')[1].split(' ON')[0]}")
        
        logger.info("✅ All indexes created")
    
    def export_to_parquet(self, output_path: str = None) -> None:
        """
        Export data to Parquet format for 10x faster performance
        
        Args:
            output_path: Path to output Parquet file
        """
        if output_path is None:
            script_dir = Path(__file__).parent.parent
            processed_dir = script_dir / 'data' / 'processed'
            processed_dir.mkdir(parents=True, exist_ok=True)
            output_path = processed_dir / 'nba_players_clean.parquet'
        
        logger.info(f"Exporting to Parquet: {output_path}")
        
        self.con.execute(f"""
            COPY players TO '{output_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """)
        
        # Get file size
        file_size = Path(output_path).stat().st_size / (1024 * 1024)
        logger.info(f"✅ Exported {file_size:.2f} MB")
    
    def get_statistics(self) -> dict:
        """
        Get database statistics
        
        Returns:
            Dictionary of statistics
        """
        stats = {}
        
        # Row count
        stats['total_rows'] = self.con.execute(
            "SELECT COUNT(*) FROM players"
        ).fetchone()[0]
        
        # Season range
        stats['season_range'] = self.con.execute(
            "SELECT MIN(season), MAX(season) FROM players"
        ).fetchone()
        
        # Unique counts
        stats['unique_players'] = self.con.execute(
            "SELECT COUNT(DISTINCT player_id) FROM players"
        ).fetchone()[0]
        
        stats['unique_teams'] = self.con.execute(
            "SELECT COUNT(DISTINCT tm) FROM players"
        ).fetchone()[0]
        
        # Position distribution
        pos_dist = self.con.execute(
            "SELECT pos, COUNT(*) as cnt FROM players GROUP BY pos ORDER BY pos"
        ).fetchdf()
        stats['position_distribution'] = pos_dist.to_dict('records')
        
        logger.info("\n" + "="*70)
        logger.info("DATABASE STATISTICS")
        logger.info("="*70)
        logger.info(f"Total rows: {stats['total_rows']:,}")
        logger.info(f"Season range: {stats['season_range'][0]} - {stats['season_range'][1]}")
        logger.info(f"Unique players: {stats['unique_players']:,}")
        logger.info(f"Unique teams: {stats['unique_teams']}")
        logger.info("\nPosition distribution:")
        for pos_info in stats['position_distribution']:
            logger.info(f"  {pos_info['pos']}: {pos_info['cnt']:,}")
        logger.info("="*70)
        
        return stats
    
    def close(self) -> None:
        """Close database connection"""
        if self.con:
            self.con.close()
            logger.info("Database connection closed")


def load_data(df: pd.DataFrame, db_path: str = None, export_parquet: bool = True) -> None:
    """
    Main loading function
    
    Args:
        df: Transformed dataframe to load
        db_path: Path to DuckDB database
        export_parquet: Whether to export to Parquet format
    """
    loader = DataLoader(db_path)
    
    try:
        # Connect
        loader.connect()
        
        # Create schema
        loader.create_schema()
        
        # Load data
        loader.load_dataframe(df)
        
        # Create indexes
        loader.create_indexes()
        
        # Export to Parquet
        if export_parquet:
            loader.export_to_parquet()
        
        # Get statistics
        loader.get_statistics()
        
    finally:
        loader.close()


if __name__ == '__main__':
    # Test loading with sample data
    print("Testing data loading...")
    
    # Create sample dataframe
    sample_data = {
        'seas_id': [1, 2],
        'season': [2024, 2024],
        'player_id': [1, 2],
        'player': ['Test Player 1', 'Test Player 2'],
        'birth_year': [1990, 1991],
        'pos': ['PG', 'SG'],
        'pos_original': ['PG', 'SG'],
        'pos_group': ['Guard', 'Guard'],
        'age': [34, 33],
        'experience': ['10', '9'],
        'lg': ['NBA', 'NBA'],
        'tm': ['LAL', 'BOS'],
        'g': [82, 80],
        'gs': [82, 75],
        'mp': [2800.0, 2600.0],
        'fg': [600, 550],
        'fga': [1200, 1100],
        'fg_percent': [0.5, 0.5],
        'x3p': [200, 180],
        'x3pa': [500, 450],
        'x3p_percent': [0.4, 0.4],
        'x2p': [400, 370],
        'x2pa': [700, 650],
        'x2p_percent': [0.57, 0.57],
        'e_fg_percent': [0.58, 0.58],
        'ft': [300, 280],
        'fta': [350, 320],
        'ft_percent': [0.86, 0.88],
        'orb': [50, 45],
        'drb': [350, 320],
        'trb': [400, 365],
        'ast': [600, 200],
        'stl': [100, 90],
        'blk': [30, 25],
        'tov': [150, 140],
        'pf': [180, 170],
        'pts': [1700, 1560],
        'ppg': [20.7, 19.5],
        'rpg': [4.9, 4.6],
        'apg': [7.3, 2.5],
        'mpg': [34.1, 32.5],
        'ts_percent': [0.60, 0.59]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Load to test database
    test_db = Path(__file__).parent.parent / 'data' / 'duckdb' / 'test.db'
    load_data(df, str(test_db), export_parquet=False)
    
    print("\nLoading test complete!")
