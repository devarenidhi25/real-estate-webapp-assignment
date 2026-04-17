"""
realestate/services/analysis.py

Module for analyzing real estate data and generating structured responses
for the frontend (summary stats, chart data, and table data).
"""

import pandas as pd
from typing import Optional
from django.db.models import Max
from realestate.models import RealEstateData
from django.db.models import Q

def analyze_price_growth(area_name: str, years: Optional[int] = None) -> dict:
    """
    Analyze price growth trends for a single area.

    Args:
        area_name: Name of the area to analyze
        years: Optional number of recent years to analyze (e.g., 5 for last 5 years)

    Returns:
        dict: Structure with summaryData, chart, and table
    """
    data = RealEstateData.objects.filter(area__iexact=area_name)
    df = pd.DataFrame(list(data.values()))

    if df.empty:
        return _empty_response(f"No data found for area: {area_name}")

    # Filter by years if specified
    if years:
        latest_year = RealEstateData.objects.aggregate(Max('year'))['year__max']
        cutoff_year = latest_year - years + 1
        df = df[df["year"] >= cutoff_year]
    
    # Sort by year
    df = df.sort_values("year")
    
    # Get price column (handle potential variations in column name)
    price_col = _get_price_column(df)
    demand_col = _get_demand_column(df)
    
    # Group by year and calculate average price
    agg_dict = {}

    if demand_col:
        agg_dict[demand_col] = "sum"

    if price_col:
        agg_dict[price_col] = "mean"

    yearly_data = df.groupby("year").agg(agg_dict).reset_index()
    
    yearly_data.columns = ["year", "avg_price", "total_demand"]
    yearly_data = yearly_data.sort_values("year")
    
    # Calculate summary statistics
    first_year = int(yearly_data.iloc[0]["year"])
    last_year = int(yearly_data.iloc[-1]["year"])
    first_price = float(yearly_data.iloc[0]["avg_price"])
    last_price = float(yearly_data.iloc[-1]["avg_price"])
    
    price_change = last_price - first_price
    price_growth_percent = (price_change / first_price * 100) if first_price > 0 else 0
    
    # Calculate year-over-year growth rates
    yoy_growth_rates = []
    for i in range(1, len(yearly_data)):
        prev_price = yearly_data.iloc[i-1]["avg_price"]
        curr_price = yearly_data.iloc[i]["avg_price"]
        if prev_price > 0:
            yoy_rate = ((curr_price - prev_price) / prev_price) * 100
            yoy_growth_rates.append(yoy_rate)
    
    avg_yoy_growth = sum(yoy_growth_rates) / len(yoy_growth_rates) if yoy_growth_rates else 0
    
    summary_data = {
        "area": area_name,
        "firstYear": first_year,
        "lastYear": last_year,
        "firstYearPrice": round(first_price, 2),
        "lastYearPrice": round(last_price, 2),
        "priceChange": round(price_change, 2),
        "priceGrowthPercent": round(price_growth_percent, 2),
        "avgYoYGrowth": round(avg_yoy_growth, 2),
        "yearsAnalyzed": len(yearly_data)
    }
    
    # Chart data
    chart_data = {
        "labels": [int(year) for year in yearly_data["year"].tolist()],
        "datasets": [
            {
                "label": f"Average Price - {area_name}",
                "data": [round(price, 2) for price in yearly_data["avg_price"].tolist()]
            }
        ]
    }
    
    # Table data
    table_data = [
        {
            "year": int(row["year"]),
            "location": area_name,
            "price": round(float(row["avg_price"]), 2),
            "demand": int(row["total_demand"]) if pd.notna(row["total_demand"]) else None
        }
        for _, row in yearly_data.iterrows()
    ]
    
    return {
        "summaryData": summary_data,
        "chart": chart_data,
        "table": table_data
    }


def compare_areas(area_names: list[str], years: Optional[int] = None) -> dict:
    """
    Compare price trends across multiple areas.

    Args:
        area_names: List of area names to compare
        years: Optional number of recent years to analyze

    Returns:
        dict: Structure with summaryData, chart, and table
    """
    area_names = [a.strip().title() for a in area_names]
    if not area_names or len(area_names) < 2:
        return _empty_response("At least 2 areas required for comparison")

    query = Q()
    for area in area_names:
        query |= Q(area__iexact=area.strip())

    data = RealEstateData.objects.filter(query)
    df = pd.DataFrame(list(data.values()))
    
    if df.empty:
        return _empty_response(f"No data found for areas: {', '.join(area_names)}")
    
    # Filter by years if specified
    if years:
        latest_year = RealEstateData.objects.aggregate(Max('year'))['year__max']
        cutoff_year = latest_year - years + 1
        df = df[df["year"] >= cutoff_year]
    
    price_col = _get_price_column(df)
    demand_col = _get_demand_column(df)
    
    # Group by year and location
    agg_dict = {price_col: "mean"}

    if demand_col:
        agg_dict[demand_col] = "sum"
    else:
        df["dummy"] = 1
        agg_dict["dummy"] = "count"

    yearly_area_data = df.groupby(["year", "area"]).agg(agg_dict).reset_index()
    
    yearly_area_data.columns = ["year", "location", "avg_price", "total_demand"]
    yearly_area_data = yearly_area_data.sort_values(["year", "location"])
    
    # Get all unique years (sorted)
    all_years = sorted(yearly_area_data["year"].unique())
    
    # Calculate summary for each area
    area_summaries = []
    datasets = []
    
    for area in area_names:
        area_data = yearly_area_data[yearly_area_data["location"].str.lower() == area.lower()]
        
        if area_data.empty:
            continue

        area_data = area_data.sort_values("year")
        first_price = float(area_data.iloc[0]["avg_price"])
        last_price = float(area_data.iloc[-1]["avg_price"])
        price_growth = ((last_price - first_price) / first_price * 100) if first_price > 0 else 0
            
        area_summaries.append({
            "area": area,
            "firstYearPrice": round(first_price, 2),
            "lastYearPrice": round(last_price, 2),
            "priceGrowthPercent": round(price_growth, 2),
            "avgPrice": round(float(area_data["avg_price"].mean()), 2)
        })
            
            # Add dataset for chart
        data_points = []

        for year in all_years:
            year_rows = area_data[area_data["year"] == year]

            if not year_rows.empty:
                value = round(float(year_rows["avg_price"].iloc[0]), 2)
            else:
                value = None

            data_points.append(value)

        datasets.append({
           "label": area,
            "data": data_points
        })

    # Overall summary
    summary_data = {
        "areas": area_names,
        "yearsAnalyzed": len(all_years),
        "firstYear": int(all_years[0]) if all_years else None,
        "lastYear": int(all_years[-1]) if all_years else None,
        "areaComparison": area_summaries
    }
    
    # Chart data
    chart_data = {
        "labels": [int(year) for year in all_years],
        "datasets": datasets
    }
    
    # Table data
    table_data = [
        {
            "year": int(row["year"]),
            "location": row["location"],
            "price": round(float(row["avg_price"]), 2),
            "demand": int(row["total_demand"]) if pd.notna(
                row["total_demand"]
            ) else None
        }
        for _, row in yearly_area_data.iterrows()
    ]
    
    return {
        "summaryData": summary_data,
        "chart": chart_data,
        "table": table_data
    }


def analyze_demand_trend(area_name: str, years: Optional[int] = None) -> dict:
    """
    Analyze demand/sales trends for a single area.
    
    Args:
        area_name: Name of the area to analyze
        years: Optional number of recent years to analyze
        
    Returns:
        dict: Structure with summaryData, chart, and table
    """
    data = RealEstateData.objects.filter(area__iexact=area_name)
    df = pd.DataFrame(list(data.values()))

    if df.empty:
        return _empty_response(f"No data found for area: {area_name}")

    # Filter by years if specified
    if years:
        latest_year = RealEstateData.objects.aggregate(Max('year'))['year__max']
        cutoff_year = latest_year - years + 1
        df = df[df["year"] >= cutoff_year]

    # Sort by year
    df = df.sort_values("year")

    demand_col = _get_demand_column(df)
    price_col = _get_price_column(df)

    if not demand_col:
        return _empty_response(f"No demand data available for area: {area_name}")

    # Group by year
    agg_dict = {}

    if price_col:
        agg_dict[price_col] = "mean"
    else:
        return _empty_response("Price column not found")

    if demand_col:
        agg_dict[demand_col] = "sum"
    else:
        df["dummy"] = 1
        agg_dict["dummy"] = "count"

    yearly_data = df.groupby("year").agg(agg_dict).reset_index()
    
    yearly_data.columns = ["year", "total_demand", "avg_price"]
    yearly_data = yearly_data.sort_values("year")
    
    # Calculate summary statistics
    first_year = int(yearly_data.iloc[0]["year"])
    last_year = int(yearly_data.iloc[-1]["year"])
    total_demand_all_years = int(yearly_data["total_demand"].sum())
    avg_demand_per_year = int(yearly_data["total_demand"].mean())
    
    first_year_demand = int(yearly_data.iloc[0]["total_demand"])
    last_year_demand = int(yearly_data.iloc[-1]["total_demand"])
    
    demand_change = last_year_demand - first_year_demand
    demand_change_percent = (demand_change / first_year_demand * 100) if first_year_demand > 0 else 0
    
    summary_data = {
        "area": area_name,
        "firstYear": first_year,
        "lastYear": last_year,
        "totalDemand": total_demand_all_years,
        "avgDemandPerYear": avg_demand_per_year,
        "firstYearDemand": first_year_demand,
        "lastYearDemand": last_year_demand,
        "demandChange": demand_change,
        "demandChangePercent": round(demand_change_percent, 2),
        "yearsAnalyzed": len(yearly_data)
    }
    
    # Chart data (dual axis: demand and price)
    chart_data = {
        "labels": [int(year) for year in yearly_data["year"].tolist()],
        "datasets": [
            {
                "label": f"Total Demand - {area_name}",
                "data": [int(demand) for demand in yearly_data["total_demand"].tolist()]
            },
            {
                "label": f"Average Price - {area_name}",
                "data": [round(price, 2) for price in yearly_data["avg_price"].tolist()]
            }
        ]
    }
    
    # Table data
    table_data = [
        {
            "year": int(row["year"]),
            "location": area_name,
            "price": round(float(row["avg_price"]), 2),
            "demand": int(row["total_demand"]) if pd.notna(row["total_demand"]) else None
        }
        for _, row in yearly_data.iterrows()
    ]
    
    return {
        "summaryData": summary_data,
        "chart": chart_data,
        "table": table_data
    }


# Helper functions

def _get_price_column(df: pd.DataFrame) -> str:
    """Find the price column in the dataframe."""
    possible_names = [
        "flat - weighted average rate",
        "flat-weighted average rate",
        "weighted average rate",
        "price",
        "rate"
    ]
    
    for col in df.columns:
        if col.lower() in [name.lower() for name in possible_names]:
            return col
    
    # Return first column with 'rate' or 'price' in name
    for col in df.columns:
        if 'rate' in col.lower() or 'price' in col.lower():
            return col
    
    return None

def _get_demand_column(df: pd.DataFrame) -> Optional[str]:
    """Find the demand column in the dataframe."""
    possible_names = [
        "total units",
        "total_sales - igr",
        "total_sales-igr",
        "total sales",
        "units",
        "demand"
    ]
    
    for col in df.columns:
        if col.lower() in [name.lower() for name in possible_names]:
            return col
    
    # Return first column with 'unit' or 'sales' in name
    for col in df.columns:
        if 'unit' in col.lower() or 'sales' in col.lower():
            return col
    
    return None


def _empty_response(message: str) -> dict:
    """Return an empty response structure with an error message."""
    return {
        "summaryData": {
            "error": message
        },
        "chart": {
            "labels": [],
            "datasets": []
        },
        "table": []
    }