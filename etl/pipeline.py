"""
ETL Pipeline Orchestration
Coordinates extract, transform, and load operations
"""
import logging
import time
from pathlib import Path

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_pipeline(
    csv_filename: str = 'NBA_Player_Totals.csv',
    db_path: str = None,
    export_parquet: bool = True
) -> None:
    """
    Run complete ETL pipeline
    
    Args:
        csv_filename: Name of CSV file to process
        db_path: Path to DuckDB database (None for default)
        export_parquet: Whether to export to Parquet format
    """
    start_time = time.time()
    
    logger.info("="*70)
    logger.info("NBA ETL PIPELINE STARTING")
    logger.info("="*70)
    
    try:
        # EXTRACT
        logger.info("\n" + "="*70)
        logger.info("STEP 1: EXTRACT")
        logger.info("="*70)
        df_raw = extract_data(csv_filename)
        extract_time = time.time() - start_time
        logger.info(f"Extract completed in {extract_time:.2f}s")
        
        # TRANSFORM
        logger.info("\n" + "="*70)
        logger.info("STEP 2: TRANSFORM")
        logger.info("="*70)
        transform_start = time.time()
        df_clean = transform_data(df_raw)
        transform_time = time.time() - transform_start
        logger.info(f"Transform completed in {transform_time:.2f}s")
        
        # LOAD
        logger.info("\n" + "="*70)
        logger.info("STEP 3: LOAD")
        logger.info("="*70)
        load_start = time.time()
        load_data(df_clean, db_path, export_parquet)
        load_time = time.time() - load_start
        logger.info(f"Load completed in {load_time:.2f}s")
        
        # SUMMARY
        total_time = time.time() - start_time
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*70)
        logger.info(f"Total execution time: {total_time:.2f}s")
        logger.info(f"  Extract: {extract_time:.2f}s ({extract_time/total_time*100:.1f}%)")
        logger.info(f"  Transform: {transform_time:.2f}s ({transform_time/total_time*100:.1f}%)")
        logger.info(f"  Load: {load_time:.2f}s ({load_time/total_time*100:.1f}%)")
        logger.info("="*70)
        
        # Output locations
        script_dir = Path(__file__).parent.parent
        logger.info("\n📁 Output Files:")
        logger.info(f"  Database: {script_dir / 'data' / 'duckdb' / 'nba.db'}")
        if export_parquet:
            logger.info(f"  Parquet: {script_dir / 'data' / 'processed' / 'nba_players_clean.parquet'}")
        
        logger.info("\n✅ Pipeline executed successfully!")
        
    except Exception as e:
        logger.error(f"\n❌ Pipeline failed: {str(e)}", exc_info=True)
        raise


if __name__ == '__main__':
    # Run the pipeline
    run_pipeline()
