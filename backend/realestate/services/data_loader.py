"""
realestate/services/data_loader.py

Module for loading and caching the real estate Excel dataset.
Loads once at startup and provides query functions for the DataFrame.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
import boto3
from io import BytesIO
# Global variable to store the cached DataFrame
_dataframe: Optional[pd.DataFrame] = None


def _load_excel() -> pd.DataFrame:
    """
    Internal function to load the Excel file from disk.
    
    Returns:
        pd.DataFrame: The loaded dataset
        
    Raises:
        FileNotFoundError: If the Excel file doesn't exist
        Exception: If there's an error reading the Excel file
    """
    # Get the path to the Excel file
    current_dir = Path(__file__).resolve().parent.parent
    excel_path = current_dir / "data" / "Sample_data.xlsx"
    
    if not excel_path.exists():
        raise FileNotFoundError(
            f"Excel file not found at: {excel_path}\n"
            f"Please ensure Sample_data.xlsx exists in realestate/data/"
        )
    
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id="YOUR_ACCESS_KEY",
            aws_secret_access_key="YOUR_SECRET_KEY",
            region_name="eu-north-1"
        )

        response = s3.get_object(
            Bucket="real-estate-fa1-bucket",
            Key="Sample_data.xlsx"
        )

        df = pd.read_excel(BytesIO(response["Body"].read()))
        
        # Verify required columns exist
        required_columns = ["final location", "year"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(
                f"Missing required columns in Excel file: {missing_columns}\n"
                f"Available columns: {list(df.columns)}"
            )
        
        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()
        
        # Strip whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
        
        return df
        
    except Exception as e:
        raise Exception(f"Error loading Excel file from {excel_path}: {str(e)}")


def _get_cached_dataframe() -> pd.DataFrame:
    """
    Get the cached DataFrame, loading it if necessary.
    
    Returns:
        pd.DataFrame: The cached dataset
    """
    global _dataframe
    
    if _dataframe is None:
        _dataframe = _load_excel()
    
    return _dataframe


def get_full_dataframe() -> pd.DataFrame:
    """
    Get the complete DataFrame.
    
    Returns:
        pd.DataFrame: A copy of the full dataset
    """
    return _get_cached_dataframe().copy()


def get_area_data(area_name: str) -> pd.DataFrame:
    """
    Get data for a specific area (case-insensitive).
    
    Args:
        area_name: The name of the area to filter by
        
    Returns:
        pd.DataFrame: Rows where 'final location' matches the area name
    """
    df = _get_cached_dataframe()
    
    # Case-insensitive matching
    mask = df["final location"].str.lower() == area_name.lower()
    
    return df[mask].copy()


def get_areas_data(area_names: list[str]) -> pd.DataFrame:
    """
    Get data for multiple areas (case-insensitive).
    
    Args:
        area_names: List of area names to filter by
        
    Returns:
        pd.DataFrame: Rows where 'final location' is in the given list
    """
    df = _get_cached_dataframe()
    
    # Convert all area names to lowercase for case-insensitive matching
    area_names_lower = [name.lower() for name in area_names]
    
    # Case-insensitive matching
    mask = df["final location"].str.lower().isin(area_names_lower)
    
    return df[mask].copy()


def get_latest_year() -> int:
    """
    Get the most recent year in the dataset.
    
    Returns:
        int: The maximum year value
    """
    df = _get_cached_dataframe()
    
    return int(df["year"].max())


# Load the DataFrame immediately when this module is imported
try:
    _dataframe = _load_excel()
    print(f"✓ Real estate data loaded successfully: {len(_dataframe)} rows")
except Exception as e:
    print(f"✗ Error loading real estate data: {str(e)}")
    # Re-raise so Django startup fails if data can't be loaded
    raise