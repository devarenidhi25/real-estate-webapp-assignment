"""
realestate/utils/text_parsing.py

Module for parsing natural language queries about real estate data.
Extracts query type, area names, and time range from user messages.
"""

import re
from typing import Optional


def parse_query(message: str) -> dict:
    """
    Parse a natural language query and extract structured information.
    
    Args:
        message: The user's natural language query
        
    Returns:
        dict: A dictionary containing:
            - query_type: str - One of: "price_growth", "compare_areas", "analyze_area", "demand_trend", "unknown"
            - areas: list[str] - List of area names mentioned (empty list if none)
            - years: Optional[int] - Number of years requested (e.g., "last 3 years" -> 3)
            - raw_message: str - The original message for reference
    
    Examples:
        >>> parse_query("Show me price growth in Baner over the last 5 years")
        {
            'query_type': 'price_growth',
            'areas': ['Baner'],
            'years': 5,
            'raw_message': '...'
        }
        
        >>> parse_query("Compare Hinjewadi and Wakad")
        {
            'query_type': 'compare_areas',
            'areas': ['Hinjewadi', 'Wakad'],
            'years': None,
            'raw_message': '...'
        }
    """
    message_lower = message.lower().strip()
    
    result = {
        'query_type': 'unknown',
        'areas': [],
        'years': None,
        'raw_message': message
    }
    
    # Extract number of years
    result['years'] = _extract_years(message_lower)
    
    # Extract area names FIRST (needed for better type detection)
    result['areas'] = _extract_areas(message)
    
    # Detect query type (now with areas available)
    result['query_type'] = _detect_query_type(message_lower, result['areas'])
    
    return result


def _extract_years(message_lower: str) -> Optional[int]:
    """
    Extract the number of years from phrases like "last 3 years" or "past 5 years".
    
    Args:
        message_lower: Lowercase message string
        
    Returns:
        Optional[int]: Number of years, or None if not found
    """
    # Patterns for time ranges
    patterns = [
        r'(?:last|past|previous)\s+(\d+)\s+years?',
        r'(\d+)\s+years?(?:\s+(?:period|trend|data))?',
        r'over\s+(?:the\s+)?(?:last|past)?\s*(\d+)\s+years?',
        r'in\s+(?:the\s+)?(?:last|past)?\s*(\d+)\s+years?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                continue
    
    return None


def _detect_query_type(message_lower: str, areas: list[str] = None) -> str:
    """
    Detect the type of query based on keywords and patterns.
    
    Args:
        message_lower: Lowercase message string
        areas: Optional list of extracted areas for better detection
        
    Returns:
        str: Query type identifier
    """
    # Price growth indicators
    price_growth_keywords = [
        'price growth', 'price trend', 'price increase', 'price change',
        'appreciation', 'growth rate', 'how much has price',
        'price over time', 'price evolution', 'pricing trend',
        'show price', 'show prices', 'price in '
    ]
    
    # Compare areas indicators
    compare_keywords = [
        'compare', 'comparison', 'versus', 'vs', 'difference between',
        'better investment', 'which area', 'or', 'between'
    ]
    
    # Demand/sales trend indicators
    demand_keywords = [
        'demand', 'sales', 'units sold', 'supply', 'inventory',
        'market activity', 'transaction', 'buying activity'
    ]
    
    # Analysis indicators (general area analysis)
    analysis_keywords = [
        'analyze', 'analysis', 'tell me about', 'information about',
        'show me', 'show', 'what about', 'how is', 'overview', 'insights'
    ]
    
    # Check for price growth
    if any(keyword in message_lower for keyword in price_growth_keywords):
        return 'price_growth'
    
    # Check for demand trends
    if any(keyword in message_lower for keyword in demand_keywords):
        return 'demand_trend'
    
    # Check for comparison (needs multiple areas)
    if any(keyword in message_lower for keyword in compare_keywords):
        # Look for multiple area indicators (and, or, vs, comma)
        # OR check if we have 2+ areas (will be checked in parse_query)
        if re.search(r'\b(?:and|or|vs|versus)\b|,', message_lower):
            return 'compare_areas'
        # If we have 2+ areas and comparison keyword, it's a comparison
        if areas and len(areas) >= 2:
            return 'compare_areas'
    
    # Check for general analysis
    if any(keyword in message_lower for keyword in analysis_keywords):
        return 'analyze_area'
    
    return 'unknown'


def _extract_areas(message: str) -> list[str]:
    """
    Extract area names from the message.
    
    This is a challenging task because area names can vary in format.
    We look for capitalized words that might be area names and common patterns.
    
    Args:
        message: The original message (with original casing)
        
    Returns:
        list[str]: List of potential area names
    """
    areas = []
    
    # Common Pune area names (expand this list based on your dataset)
    known_areas = [
        'Baner', 'Hinjewadi', 'Wakad', 'Kharadi', 'Viman Nagar', 'Viman nagar',
        'Hadapsar', 'Pimpri', 'Chinchwad', 'Aundh', 'Kalyani Nagar',
        'Koregaon Park', 'Bavdhan', 'Pashan', 'Kalyani nagar', 'koregaon park',
        'Shivaji Nagar', 'Kondhwa', 'Undri', 'Wagholi', 'Manjri',
        'Magarpatta', 'Fursungi', 'Pimple Saudagar', 'Pimple Nilakh',
        'Sus', 'Talegaon', 'Bhosari', 'Dighi', 'Ravet', 'Tathawade',
        'Akurdi', 'Ambegaon Budruk'  # Add actual dataset areas
    ]
    
    # Create case-insensitive pattern for known areas
    for area in known_areas:
        # Use word boundaries to match whole area names
        pattern = r'\b' + re.escape(area) + r'\b'
        if re.search(pattern, message, re.IGNORECASE):
            # Add the area name with its original casing from known_areas
            if area not in areas:
                areas.append(area)
    
    # Try partial matching for remaining areas
    # For example: "ambegoan" -> "Ambegaon Budruk"
    message_lower = message.lower()
    for area in known_areas:
        if area not in areas:  # Only try to match if not already found
            area_lower = area.lower()
            # Check if any word in the area name is mentioned (case-insensitive)
            # Use substring matching to handle spelling variations
            words = area_lower.split()
            if any(len(word) > 3 and word in message_lower
                   for word in words):
                areas.append(area)
            # Also check for substring matches (e.g., "ambe" -> "ambegaon")
            elif any(len(word) > 4 and word[:4] in message_lower
                     for word in words):
                areas.append(area)
    
    # If no known areas found, try to extract capitalized words
    # (might be area names not in our list)
    if not areas:
        # Look for capitalized words that might be locations
        capitalized_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', message)
        
        # Filter out common words that aren't locations
        exclude_words = [
            'Show', 'Tell', 'Compare', 'What', 'How', 'Where', 'When',
            'Which', 'The', 'And', 'Or', 'Price', 'Growth', 'Trend',
            'Area', 'Years', 'Last', 'Past', 'Over', 'In'
        ]
        
        for word in capitalized_words:
            if word not in exclude_words and word not in areas:
                areas.append(word)
    
    # Look for patterns like "in <area>" or "at <area>"
    in_pattern = r'(?:in|at|around|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    matches = re.findall(in_pattern, message)
    for match in matches:
        if match not in areas:
            areas.append(match)
    
    return areas


def get_query_intent_description(query_type: str) -> str:
    """
    Get a human-readable description of the query type.
    
    Args:
        query_type: The query type identifier
        
    Returns:
        str: Human-readable description
    """
    descriptions = {
        'price_growth': 'Analyzing price growth trends',
        'compare_areas': 'Comparing multiple areas',
        'analyze_area': 'Providing area analysis',
        'demand_trend': 'Analyzing demand and sales trends',
        'unknown': 'Processing general query'
    }
    
    return descriptions.get(query_type, 'Processing query')
