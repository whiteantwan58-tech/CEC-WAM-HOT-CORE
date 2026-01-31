"""
google_sheets_sync.py
---------------------
Google Sheets integration for two-way synchronization with CEC-WAM-HOT-CORE system.
Enables real-time updates and retrieval from Google Sheets.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

import pandas as pd

from config import Config
from logging_config import get_logger

logger = get_logger('google_sheets')


class GoogleSheetsSync:
    """Handles two-way synchronization with Google Sheets."""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Sheets sync.
        
        Args:
            credentials_path: Path to service account credentials JSON
        """
        if not GOOGLE_API_AVAILABLE:
            logger.error("Google API libraries not available. Install with: pip install google-auth google-api-python-client")
            self.service = None
            return
        
        self.credentials_path = credentials_path or Config.GOOGLE_SHEETS_CREDENTIALS_PATH
        self.service = None
        
        if Path(self.credentials_path).exists():
            try:
                creds = service_account.Credentials.from_service_account_file(
                    self.credentials_path, 
                    scopes=self.SCOPES
                )
                self.service = build('sheets', 'v4', credentials=creds)
                logger.info("Google Sheets service initialized")
            except Exception as e:
                logger.error(f"Error initializing Google Sheets service: {e}")
        else:
            logger.warning(f"Credentials file not found: {self.credentials_path}")
    
    def read_sheet(
        self, 
        spreadsheet_id: str, 
        range_name: str = 'Sheet1!A:Z'
    ) -> Optional[pd.DataFrame]:
        """
        Read data from a Google Sheet.
        
        Args:
            spreadsheet_id: Google Sheets ID
            range_name: Range to read (e.g., 'Sheet1!A:Z')
        
        Returns:
            DataFrame with sheet data or None on error
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return None
        
        try:
            logger.info(f"Reading from sheet {spreadsheet_id}, range {range_name}")
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("No data found in sheet")
                return pd.DataFrame()
            
            # First row as headers
            headers = values[0]
            data = values[1:]
            
            df = pd.DataFrame(data, columns=headers)
            logger.info(f"Read {len(df)} rows from Google Sheet")
            
            return df
            
        except HttpError as e:
            logger.error(f"HTTP error reading sheet: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading sheet: {e}")
            return None
    
    def write_sheet(
        self,
        spreadsheet_id: str,
        range_name: str,
        data: pd.DataFrame,
        include_headers: bool = True
    ) -> bool:
        """
        Write data to a Google Sheet.
        
        Args:
            spreadsheet_id: Google Sheets ID
            range_name: Range to write (e.g., 'Sheet1!A1')
            data: DataFrame to write
            include_headers: Whether to include column headers
        
        Returns:
            True if write successful
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return False
        
        try:
            logger.info(f"Writing to sheet {spreadsheet_id}, range {range_name}")
            
            # Prepare values
            values = []
            if include_headers:
                values.append(data.columns.tolist())
            values.extend(data.values.tolist())
            
            body = {'values': values}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            updated_cells = result.get('updatedCells', 0)
            logger.info(f"Updated {updated_cells} cells in Google Sheet")
            
            return True
            
        except HttpError as e:
            logger.error(f"HTTP error writing sheet: {e}")
            return False
        except Exception as e:
            logger.error(f"Error writing sheet: {e}")
            return False
    
    def append_to_sheet(
        self,
        spreadsheet_id: str,
        range_name: str,
        data: pd.DataFrame
    ) -> bool:
        """
        Append data to a Google Sheet.
        
        Args:
            spreadsheet_id: Google Sheets ID
            range_name: Range to append to (e.g., 'Sheet1!A:Z')
            data: DataFrame to append
        
        Returns:
            True if append successful
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return False
        
        try:
            logger.info(f"Appending to sheet {spreadsheet_id}, range {range_name}")
            
            values = data.values.tolist()
            body = {'values': values}
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            updated_cells = result.get('updates', {}).get('updatedCells', 0)
            logger.info(f"Appended {len(data)} rows, updated {updated_cells} cells")
            
            return True
            
        except HttpError as e:
            logger.error(f"HTTP error appending to sheet: {e}")
            return False
        except Exception as e:
            logger.error(f"Error appending to sheet: {e}")
            return False
    
    def sync_csv_to_sheet(
        self,
        csv_path: str,
        spreadsheet_id: str,
        range_name: str = 'Sheet1!A1',
        clear_existing: bool = False
    ) -> bool:
        """
        Sync a CSV file to a Google Sheet.
        
        Args:
            csv_path: Path to CSV file
            spreadsheet_id: Google Sheets ID
            range_name: Range to write to
            clear_existing: Whether to clear existing data first
        
        Returns:
            True if sync successful
        """
        logger.info(f"Syncing {csv_path} to Google Sheet {spreadsheet_id}")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            
            # Clear existing data if requested
            if clear_existing:
                self.clear_sheet(spreadsheet_id, range_name)
            
            # Write to sheet
            success = self.write_sheet(spreadsheet_id, range_name, df, include_headers=True)
            
            if success:
                logger.info(f"Successfully synced {len(df)} rows to Google Sheet")
            
            return success
            
        except Exception as e:
            logger.error(f"Error syncing CSV to sheet: {e}")
            return False
    
    def sync_sheet_to_csv(
        self,
        spreadsheet_id: str,
        range_name: str,
        csv_path: str
    ) -> bool:
        """
        Sync a Google Sheet to a CSV file.
        
        Args:
            spreadsheet_id: Google Sheets ID
            range_name: Range to read from
            csv_path: Path to save CSV file
        
        Returns:
            True if sync successful
        """
        logger.info(f"Syncing Google Sheet {spreadsheet_id} to {csv_path}")
        
        try:
            # Read from sheet
            df = self.read_sheet(spreadsheet_id, range_name)
            
            if df is None:
                return False
            
            # Save to CSV
            df.to_csv(csv_path, index=False)
            logger.info(f"Successfully synced {len(df)} rows to {csv_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error syncing sheet to CSV: {e}")
            return False
    
    def clear_sheet(self, spreadsheet_id: str, range_name: str) -> bool:
        """
        Clear data from a Google Sheet range.
        
        Args:
            spreadsheet_id: Google Sheets ID
            range_name: Range to clear
        
        Returns:
            True if clear successful
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return False
        
        try:
            logger.info(f"Clearing sheet {spreadsheet_id}, range {range_name}")
            
            self.service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                body={}
            ).execute()
            
            logger.info("Sheet range cleared successfully")
            return True
            
        except HttpError as e:
            logger.error(f"HTTP error clearing sheet: {e}")
            return False
        except Exception as e:
            logger.error(f"Error clearing sheet: {e}")
            return False
    
    def get_sheet_metadata(self, spreadsheet_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata about a Google Sheet.
        
        Args:
            spreadsheet_id: Google Sheets ID
        
        Returns:
            Dictionary with sheet metadata or None on error
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return None
        
        try:
            logger.info(f"Getting metadata for sheet {spreadsheet_id}")
            
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            metadata = {
                'title': spreadsheet.get('properties', {}).get('title', ''),
                'sheets': []
            }
            
            for sheet in spreadsheet.get('sheets', []):
                sheet_props = sheet.get('properties', {})
                metadata['sheets'].append({
                    'title': sheet_props.get('title', ''),
                    'sheetId': sheet_props.get('sheetId', ''),
                    'index': sheet_props.get('index', 0),
                    'rowCount': sheet_props.get('gridProperties', {}).get('rowCount', 0),
                    'columnCount': sheet_props.get('gridProperties', {}).get('columnCount', 0)
                })
            
            logger.info(f"Retrieved metadata for {len(metadata['sheets'])} sheets")
            return metadata
            
        except HttpError as e:
            logger.error(f"HTTP error getting metadata: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting metadata: {e}")
            return None
