"""
realestate/views.py

API views for real estate query endpoint.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import QueryLog
from .utils.text_parsing import parse_query
from .services.analysis import (
    analyze_price_growth,
    compare_areas,
    analyze_demand_trend,
    get_top_growing_area
)


@api_view(['POST'])
def query_view(request):
    """
    Handle natural language queries about real estate data.
    
    Request body:
        {
            "message": "Show me price growth in Baner over last 5 years"
        }
    
    Response:
        {
            "summary": "Natural language summary",
            "action": "price_growth",
            "areas": ["Baner"],
            "chart": {...},
            "table": [...]
        }
    """
    # Validate request
    message = request.data.get('message')
    
    if not message:
        return Response(
            {
                "error": "Missing 'message' field in request body",
                "summary": "Please provide a query message."
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not isinstance(message, str) or not message.strip():
        return Response(
            {
                "error": "Invalid message format",
                "summary": "Message must be a non-empty string."
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Log the query silently
        QueryLog.objects.create(query_text=message)
        
        # Parse the query
        parsed = parse_query(message)
        
        query_type = parsed.get('query_type', 'unknown')
        areas = parsed.get('areas', [])
        years = parsed.get('years')
        
        # Route to appropriate analysis function
        analysis_result = None
        action = 'unknown'
        
        if query_type == 'price_growth' and areas:
            action = 'price_growth'
            analysis_result = analyze_price_growth(
                area_name=areas[0],
                years=years
            )
        
        elif query_type == 'compare_areas' and len(areas) >= 2:
            action = 'compare'
            analysis_result = compare_areas(
                area_names=areas,
                years=years
            )
        
        elif query_type == 'demand_trend' and areas:
            action = 'demand_trend'
            analysis_result = analyze_demand_trend(
                area_name=areas[0],
                years=years
            )
        
        elif query_type == 'analyze_area' and areas:
            # Default to price growth for general area analysis
            action = 'price_growth'
            analysis_result = analyze_price_growth(
                area_name=areas[0],
                years=years
            )
        
        else:
            # Unable to process query
            return Response(
                {
                    "error": "Unable to process query",
                    "summary": _get_error_summary(query_type, areas),
                    "action": "unknown",
                    "areas": areas,
                    "chart": {"labels": [], "datasets": []},
                    "table": []
                },
                status=status.HTTP_200_OK
            )
        
        # Check if analysis returned an error
        if analysis_result and 'summaryData' in analysis_result:
            if 'error' in analysis_result['summaryData']:
                return Response(
                    {
                        "error": analysis_result['summaryData']['error'],
                        "summary": analysis_result['summaryData']['error'],
                        "action": action,
                        "areas": areas,
                        "chart": analysis_result.get('chart', {"labels": [], "datasets": []}),
                        "table": analysis_result.get('table', [])
                    },
                    status=status.HTTP_200_OK
                )
        
        # Generate natural language summary
        summary = _generate_summary(action, analysis_result, areas, years)
        
        # Build response
        response_data = {
            "summary": summary,
            "action": action,
            "areas": areas,
            "chart": analysis_result.get('chart', {"labels": [], "datasets": []}),
            "table": analysis_result.get('table', [])
        }
        
        # Include summary data for frontend to use if needed
        if 'summaryData' in analysis_result:
            response_data['summaryData'] = analysis_result['summaryData']
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {
                "error": f"Internal server error: {str(e)}",
                "summary": "An error occurred while processing your query. Please try again.",
                "action": "error",
                "areas": [],
                "chart": {"labels": [], "datasets": []},
                "table": []
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _generate_summary(action: str, analysis_result: dict, areas: list, years: int = None) -> str:
    """
    Generate a natural language summary based on the analysis results.
    
    Args:
        action: Type of analysis performed
        analysis_result: Result dictionary from analysis function
        areas: List of area names
        years: Number of years analyzed
        
    Returns:
        str: Natural language summary
    """
    summary_data = analysis_result.get('summaryData', {})
    
    if action == 'price_growth':
        area = areas[0] if areas else "the area"
        first_year_price = summary_data.get('firstYearPrice', 0)
        last_year_price = summary_data.get('lastYearPrice', 0)
        growth_percent = summary_data.get('priceGrowthPercent', 0)
        first_year = summary_data.get('firstYear', '')
        last_year = summary_data.get('lastYear', '')
        
        time_period = f"from {first_year} to {last_year}"
        if years:
            time_period = f"over the last {years} years"
        
        if growth_percent > 0:
            return (
                f"Price analysis for {area} {time_period}: "
                f"Prices increased from ₹{first_year_price:,.0f} to ₹{last_year_price:,.0f}, "
                f"showing a growth of {growth_percent:.1f}%."
            )
        elif growth_percent < 0:
            return (
                f"Price analysis for {area} {time_period}: "
                f"Prices decreased from ₹{first_year_price:,.0f} to ₹{last_year_price:,.0f}, "
                f"showing a decline of {abs(growth_percent):.1f}%."
            )
        else:
            return (
                f"Price analysis for {area} {time_period}: "
                f"Prices remained relatively stable at around ₹{last_year_price:,.0f}."
            )
    
    elif action == 'compare':
        area_comparison = summary_data.get('areaComparison', [])
        if area_comparison:
            # Find best and worst performing areas
            sorted_areas = sorted(area_comparison, key=lambda x: x.get('priceGrowthPercent', 0), reverse=True)
            best = sorted_areas[0]
            worst = sorted_areas[-1]
            
            time_period = f"from {summary_data.get('firstYear', '')} to {summary_data.get('lastYear', '')}"
            if years:
                time_period = f"over the last {years} years"
            
            return (
                f"Comparison of {len(areas)} areas {time_period}: "
                f"{best['area']} showed the highest growth at {best['priceGrowthPercent']:.1f}%, "
                f"while {worst['area']} had {worst['priceGrowthPercent']:.1f}% growth."
            )
        else:
            return f"Comparison analysis for {', '.join(areas)}."
    
    elif action == 'demand_trend':
        area = areas[0] if areas else "the area"
        total_demand = summary_data.get('totalDemand', 0)
        demand_change_percent = summary_data.get('demandChangePercent', 0)
        first_year = summary_data.get('firstYear', '')
        last_year = summary_data.get('lastYear', '')
        
        time_period = f"from {first_year} to {last_year}"
        if years:
            time_period = f"over the last {years} years"
        
        if demand_change_percent > 0:
            return (
                f"Demand analysis for {area} {time_period}: "
                f"Total demand was {total_demand:,} units with an increase of {demand_change_percent:.1f}%."
            )
        elif demand_change_percent < 0:
            return (
                f"Demand analysis for {area} {time_period}: "
                f"Total demand was {total_demand:,} units with a decrease of {abs(demand_change_percent):.1f}%."
            )
        else:
            return (
                f"Demand analysis for {area} {time_period}: "
                f"Total demand was {total_demand:,} units with stable trends."
            )
    
    return "Analysis complete. Please review the chart and table for detailed insights."


def _get_error_summary(query_type: str, areas: list) -> str:
    """
    Generate an error summary message based on what went wrong.
    
    Args:
        query_type: The detected query type
        areas: List of detected areas
        
    Returns:
        str: Error message
    """
    if query_type == 'unknown':
        return (
            "I couldn't understand your query. Please try asking about price growth, "
            "area comparisons, or demand trends. For example: "
            "'Show me price growth in Baner' or 'Compare Hinjewadi and Wakad'."
        )
    
    if not areas:
        return (
            "I couldn't identify which area(s) you're asking about. "
            "Please mention specific area names in your query."
        )
    
    if query_type == 'compare_areas' and len(areas) < 2:
        return (
            "For area comparison, please mention at least 2 areas. "
            "For example: 'Compare Baner and Hinjewadi'."
        )
    
    return "Unable to process your query. Please try rephrasing or providing more details."


@api_view(['GET'])
def top_growth_view(request):
    """
    Get top 3 growing areas by price growth percentage.
    
    Response:
        {
            "top_areas": [
                {"area": "Aundh", "growth": 32.5, "min_price": 100000, "max_price": 132500},
                ...
            ]
        }
    """
    try:
        result = get_top_growing_area(limit=3)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {
                "error": f"Error retrieving top growing areas: {str(e)}",
                "top_areas": []
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )