#!/usr/bin/env python3
"""
Data Management Utility for CEC-WAM System
Filters and manages CSV data from Nov 6 to today
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path

def filter_csv_by_date(input_file, output_file=None, cutoff_date=None):
    """
    Filter CSV file to only include data from cutoff_date onwards
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file (optional, defaults to input_file_filtered.csv)
        cutoff_date: Cutoff date (defaults to Nov 6, 2025)
    """
    if cutoff_date is None:
        cutoff_date = datetime(2025, 11, 6)
    
    if output_file is None:
        base = Path(input_file).stem
        ext = Path(input_file).suffix
        output_file = f"{base}_filtered{ext}"
    
    try:
        # Read CSV
        df = pd.read_csv(input_file)
        print(f"✅ Loaded {input_file}: {len(df)} records")
        
        # Find date column
        date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        
        if not date_columns:
            print(f"⚠️  No date column found in {input_file}")
            return df
        
        date_col = date_columns[0]
        print(f"📅 Using date column: {date_col}")
        
        # Convert to datetime
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Filter
        original_count = len(df)
        df_filtered = df[df[date_col] >= cutoff_date]
        filtered_count = len(df_filtered)
        
        print(f"🔍 Filtered: {original_count} → {filtered_count} records ({original_count - filtered_count} removed)")
        
        # Save
        df_filtered.to_csv(output_file, index=False)
        print(f"💾 Saved to {output_file}")
        
        return df_filtered
        
    except Exception as e:
        print(f"❌ Error processing {input_file}: {e}")
        return None

def process_all_csv_files(directory='.', output_dir='filtered_data'):
    """
    Process all CSV files in directory
    
    Args:
        directory: Directory to search for CSV files
        output_dir: Output directory for filtered files
    """
    print("🚀 CEC-WAM Data Filter Utility")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all CSV files
    csv_files = list(Path(directory).glob('*.csv'))
    
    if not csv_files:
        print("⚠️  No CSV files found")
        return
    
    print(f"📊 Found {len(csv_files)} CSV files")
    print()
    
    results = []
    
    for csv_file in csv_files:
        print(f"\n📄 Processing: {csv_file.name}")
        print("-" * 50)
        
        output_file = Path(output_dir) / csv_file.name
        df = filter_csv_by_date(str(csv_file), str(output_file))
        
        if df is not None:
            results.append({
                'file': csv_file.name,
                'records': len(df),
                'output': str(output_file)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    for result in results:
        print(f"✅ {result['file']}: {result['records']} records → {result['output']}")
    
    print(f"\n✨ Total files processed: {len(results)}")
    print(f"📁 Output directory: {output_dir}")

def generate_data_report(directory='.'):
    """
    Generate a report of all data files
    
    Args:
        directory: Directory to analyze
    """
    print("\n" + "=" * 50)
    print("📊 DATA REPORT")
    print("=" * 50)
    
    csv_files = list(Path(directory).glob('*.csv'))
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            print(f"\n📄 {csv_file.name}")
            print(f"   Records: {len(df)}")
            print(f"   Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            
            # Check for date columns
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                print(f"   Date columns: {', '.join(date_cols)}")
                
                # Get date range
                for date_col in date_cols:
                    try:
                        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                        min_date = df[date_col].min()
                        max_date = df[date_col].max()
                        print(f"   Date range ({date_col}): {min_date} to {max_date}")
                    except:
                        pass
            
        except Exception as e:
            print(f"\n❌ Error reading {csv_file.name}: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "report":
            # Generate report
            generate_data_report()
        elif sys.argv[1] == "filter":
            # Filter all files
            output_dir = sys.argv[2] if len(sys.argv) > 2 else 'filtered_data'
            process_all_csv_files(output_dir=output_dir)
        else:
            # Filter single file
            input_file = sys.argv[1]
            output_file = sys.argv[2] if len(sys.argv) > 2 else None
            filter_csv_by_date(input_file, output_file)
    else:
        # Default: filter all files
        print("Usage:")
        print("  python data_manager.py report              # Generate data report")
        print("  python data_manager.py filter [output_dir] # Filter all CSV files")
        print("  python data_manager.py <file> [output]     # Filter single file")
        print()
        
        # Run report by default
        generate_data_report()
