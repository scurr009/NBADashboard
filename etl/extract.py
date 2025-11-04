"""
Data extraction module for NBA player statistics
Reads and validates raw CSV data
"""
import pandas as pd
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    """Handles extraction of NBA player data from CSV"""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize extractor
        
        Args:
            data_dir: Path to data directory (defaults to project data/raw)
        """
        if data_dir is None:
            script_dir = Path(__file__).parent.parent
            self.data_dir = script_dir / 'data' / 'raw'
        else:
            self.data_dir = Path(data_dir)
    
    def extract_csv(self, filename: str = 'NBA_Player_Totals.csv') -> pd.DataFrame:
        """
        Extract data from CSV file
        
        Args:
            filename: Name of CSV file to read
            
        Returns:
            Raw dataframe
        """
        csv_path = self.data_dir / filename
        
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        logger.info(f"Reading CSV from: {csv_path}")
        
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Log metadata
        file_size = csv_path.stat().st_size / (1024 * 1024)  # MB
        logger.info(f"File size: {file_size:.2f} MB")
        logger.info(f"Rows: {len(df):,}")
        logger.info(f"Columns: {len(df.columns)}")
        
        # Validate structure
        self._validate_structure(df)
        
        return df
    
    def _validate_structure(self, df: pd.DataFrame) -> None:
        """
        Validate CSV structure has required columns
        
        Args:
            df: Dataframe to validate
        """
        required_columns = [
            'seas_id', 'season', 'player_id', 'player', 'pos', 'tm',
            'g', 'pts', 'trb', 'ast', 'fg', 'fga', 'ft', 'fta'
        ]
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        logger.info("✅ CSV structure validation passed")
    
    def get_metadata(self, df: pd.DataFrame) -> dict:
        """
        Get metadata about the dataset
        
        Args:
            df: Dataframe to analyze
            
        Returns:
            Dictionary of metadata
        """
        metadata = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'season_range': (df['season'].min(), df['season'].max()),
            'unique_players': df['player_id'].nunique(),
            'unique_teams': df['tm'].nunique(),
            'unique_positions': df['pos'].nunique(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
        
        logger.info("\n" + "="*70)
        logger.info("DATASET METADATA")
        logger.info("="*70)
        for key, value in metadata.items():
            logger.info(f"{key}: {value}")
        logger.info("="*70)
        
        return metadata


def extract_data(csv_filename: str = 'NBA_Player_Totals.csv') -> pd.DataFrame:
    """
    Main extraction function
    
    Args:
        csv_filename: Name of CSV file to extract
        
    Returns:
        Raw dataframe
    """
    extractor = DataExtractor()
    df = extractor.extract_csv(csv_filename)
    extractor.get_metadata(df)
    return df


if __name__ == '__main__':
    # Test extraction
    print("Testing data extraction...")
    df = extract_data()
    print("\nSample data:")
    print(df.head())
    print("\nExtraction complete!")
