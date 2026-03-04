#!/usr/bin/env python
"""Test script to verify the query parsing fix"""

import sys
import os

# Add the backend directory to the path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from realestate.utils.text_parsing import parse_query

# Test the problematic query
print("=" * 60)
print("Testing Query Parsing Fix")
print("=" * 60)

test_queries = [
    'show prices in wakad',
    'Compare Aundh Wakad Ambegaon',
    'Analyze Wakad',
    'What about demand in Kharadi',
    'Price trend in Baner'
]

for query in test_queries:
    result = parse_query(query)
    print(f"\nQuery: {query}")
    print(f"  Type: {result['query_type']}")
    print(f"  Areas: {result['areas']}")
    print(f"  Years: {result['years']}")
