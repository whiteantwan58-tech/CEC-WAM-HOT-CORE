"""
csv_operations.py
-----------------
Automated CSV file operations including merging, updating, and synchronization.
Integrates with Pandas for dynamic data manipulation.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import shutil

from config import Config
from logging_config import get_logger

logger = get_logger('csv_operations')


class CSVOperations:
    """Handles automated CSV file operations."""
    
    def __init__(self):
        """Initialize CSV operations handler."""
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
    
    def backup_file(self, file_path: str) -> str:
        """
        Create a backup of a file before modification.
        
        Args:
            file_path: Path to file to backup
        
        Returns:
            Path to backup file
        """
        if not Path(file_path).exists():
            logger.warning(f"Cannot backup non-existent file: {file_path}")
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = Path(file_path).name
        backup_path = self.backup_dir / f"{timestamp}_{filename}"
        
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        
        return str(backup_path)
    
    def merge_csv_files(
        self, 
        file_paths: List[str], 
        output_path: str,
        deduplicate: bool = True,
        sort_by: Optional[str] = None
    ) -> bool:
        """
        Merge multiple CSV files into one.
        
        Args:
            file_paths: List of CSV file paths to merge
            output_path: Path for merged output file
            deduplicate: Whether to remove duplicate rows
            sort_by: Optional column name to sort by
        
        Returns:
            True if merge successful
        """
        logger.info(f"Merging {len(file_paths)} CSV files")
        
        try:
            dataframes = []
            
            for file_path in file_paths:
                if Path(file_path).exists():
                    df = pd.read_csv(file_path)
                    df['_source_file'] = file_path
                    dataframes.append(df)
                    logger.info(f"Loaded {len(df)} rows from {file_path}")
                else:
                    logger.warning(f"File not found: {file_path}")
            
            if not dataframes:
                logger.error("No valid files to merge")
                return False
            
            # Merge all dataframes
            merged_df = pd.concat(dataframes, ignore_index=True)
            logger.info(f"Merged dataframe has {len(merged_df)} rows")
            
            # Remove duplicates if requested
            if deduplicate:
                original_count = len(merged_df)
                # Keep all columns except _source_file for duplicate detection
                cols_for_dedup = [col for col in merged_df.columns if col != '_source_file']
                merged_df = merged_df.drop_duplicates(subset=cols_for_dedup, keep='first')
                removed = original_count - len(merged_df)
                if removed > 0:
                    logger.info(f"Removed {removed} duplicate rows")
            
            # Sort if requested
            if sort_by and sort_by in merged_df.columns:
                merged_df = merged_df.sort_values(by=sort_by)
                logger.info(f"Sorted by column: {sort_by}")
            
            # Save merged file
            merged_df.to_csv(output_path, index=False)
            logger.info(f"Merged file saved to: {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error merging CSV files: {e}")
            return False
    
    def update_csv_file(
        self,
        file_path: str,
        updates: Dict[str, Any],
        filter_column: str,
        filter_value: Any
    ) -> bool:
        """
        Update specific rows in a CSV file.
        
        Args:
            file_path: Path to CSV file
            updates: Dictionary of column: value updates
            filter_column: Column to filter rows for update
            filter_value: Value to match in filter column
        
        Returns:
            True if update successful
        """
        logger.info(f"Updating {file_path} where {filter_column}={filter_value}")
        
        try:
            # Backup first
            self.backup_file(file_path)
            
            # Load CSV
            df = pd.read_csv(file_path)
            
            # Apply updates
            mask = df[filter_column] == filter_value
            rows_affected = mask.sum()
            
            if rows_affected == 0:
                logger.warning(f"No rows found matching {filter_column}={filter_value}")
                return False
            
            for column, value in updates.items():
                if column in df.columns:
                    df.loc[mask, column] = value
                else:
                    logger.warning(f"Column '{column}' not found in dataframe")
            
            # Save updated CSV
            df.to_csv(file_path, index=False)
            logger.info(f"Updated {rows_affected} rows in {file_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating CSV file: {e}")
            return False
    
    def append_to_csv(self, file_path: str, data: Dict[str, Any]) -> bool:
        """
        Append a new row to a CSV file.
        
        Args:
            file_path: Path to CSV file
            data: Dictionary of column: value for new row
        
        Returns:
            True if append successful
        """
        logger.info(f"Appending data to {file_path}")
        
        try:
            path = Path(file_path)
            
            if path.exists():
                df = pd.read_csv(file_path)
            else:
                # Create new dataframe with columns from data
                df = pd.DataFrame(columns=list(data.keys()))
            
            # Append new row
            new_row = pd.DataFrame([data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Save
            df.to_csv(file_path, index=False)
            logger.info(f"Appended row to {file_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error appending to CSV: {e}")
            return False
    
    def sync_csv_to_excel(self, csv_path: str, excel_path: str, sheet_name: str = 'Sheet1') -> bool:
        """
        Sync CSV data to an Excel file.
        
        Args:
            csv_path: Path to source CSV file
            excel_path: Path to target Excel file
            sheet_name: Name of Excel sheet to update
        
        Returns:
            True if sync successful
        """
        logger.info(f"Syncing {csv_path} to {excel_path}")
        
        try:
            # Backup Excel file if it exists
            if Path(excel_path).exists():
                self.backup_file(excel_path)
            
            # Load CSV
            df = pd.read_csv(csv_path)
            
            # Write to Excel
            # Use 'w' mode to avoid sheet name conflicts, or 'a' with if_sheet_exists for newer pandas
            excel_exists = Path(excel_path).exists()
            write_mode = 'a' if excel_exists else 'w'
            
            # For pandas >= 1.4.0, we can use if_sheet_exists parameter
            try:
                with pd.ExcelWriter(excel_path, engine='openpyxl', mode=write_mode, if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            except TypeError:
                # Fallback for older pandas versions - use 'w' mode
                with pd.ExcelWriter(excel_path, engine='openpyxl', mode='w') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.info(f"Synced {len(df)} rows to {excel_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error syncing CSV to Excel: {e}")
            return False
    
    def validate_csv_schema(self, file_path: str, expected_columns: List[str]) -> Dict[str, Any]:
        """
        Validate that a CSV has the expected schema.
        
        Args:
            file_path: Path to CSV file
            expected_columns: List of expected column names
        
        Returns:
            Dictionary with validation results
        """
        logger.info(f"Validating schema of {file_path}")
        
        result = {
            'valid': False,
            'missing_columns': [],
            'extra_columns': [],
            'column_count': 0
        }
        
        try:
            df = pd.read_csv(file_path)
            actual_columns = set(df.columns)
            expected_columns_set = set(expected_columns)
            
            result['column_count'] = len(actual_columns)
            result['missing_columns'] = list(expected_columns_set - actual_columns)
            result['extra_columns'] = list(actual_columns - expected_columns_set)
            result['valid'] = len(result['missing_columns']) == 0
            
            if result['valid']:
                logger.info(f"Schema validation passed for {file_path}")
            else:
                logger.warning(f"Schema validation failed for {file_path}: {result}")
            
        except Exception as e:
            logger.error(f"Error validating CSV schema: {e}")
            result['error'] = str(e)
        
        return result
    
    def get_csv_statistics(self, file_path: str) -> Dict[str, Any]:
        """
        Get statistics about a CSV file.
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            Dictionary of statistics
        """
        try:
            df = pd.read_csv(file_path)
            
            stats = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
            }
            
            # Add numeric statistics
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                stats['numeric_summary'] = df[numeric_cols].describe().to_dict()
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting CSV statistics: {e}")
            return {'error': str(e)}
