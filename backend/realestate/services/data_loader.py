"""
realestate/services/data_loader.py

Module for loading real estate data from Django ORM.
Replaces Excel-based data loading with database queries.
"""

import pandas as pd
from typing import Optional
from ..models import RealEstateData
from django.db.models import Q, F


def get_full_dataframe() -> pd.DataFrame:
    """
    Get the complete dataset as a DataFrame.
    
    Returns:
        pd.DataFrame: All RealEstateData records
    """
    data = RealEstateData.objects.all().values()
    df = pd.DataFrame(data)
    
    if df.empty:
        return df
    
    # Rename fields to match expected column names
    df = df.rename(columns={
        'area': 'final location',
        'price': 'flat - weighted average rate',
        'demand': 'total units'
    })
    
    return df


def get_area_data(area_name: str) -> pd.DataFrame:
    """
    Get data for a specific area (case-insensitive).
    
    Args:
        area_name: The name of the area to filter by
        
    Returns:
        pd.DataFrame: Rows where area matches the area name
    """
    data = RealEstateData.objects.filter(
        area__iexact=area_name
    ).values()
    
    df = pd.DataFrame(data)
    
    if df.empty:
        return df
    
    # Rename fields to match expected column names
    df = df.rename(columns={
        'area': 'final location',
        'price': 'flat - weighted average rate',
        'demand': 'total units'
    })
    
    return df


def get_areas_data(area_names: list[str]) -> pd.DataFrame:
    """
    Get data for multiple areas (case-insensitive).
    
    Args:
        area_names: List of area names to filter by
        
    Returns:
        pd.DataFrame: Rows where area is in the given list
    """
    # Build Q object for case-insensitive matching
    query = Q()
    for area_name in area_names:
        query |= Q(area__iexact=area_name)
    
    data = RealEstateData.objects.filter(query).values()
    
    df = pd.DataFrame(data)
    
    if df.empty:
        return df
    
    # Rename fields to match expected column names
    df = df.rename(columns={
        'area': 'final location',
        'price': 'flat - weighted average rate',
        'demand': 'total units'
    })
    
    return df


def get_latest_year() -> int:
    """
    Get the most recent year in the dataset.
    
    Returns:
        int: The maximum year value
    """
    max_year = RealEstateData.objects.values_list('year', flat=True).order_by('-year').first()
    return int(max_year) if max_year is not None else 0