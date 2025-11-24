#!/usr/bin/env python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from realestate.utils.text_parsing import parse_query

test_messages = [
    'compare aundh wakad ambegoan',
    'Compare Aundh Wakad Ambegaon',
    'Show me price in aundh wakad and ambegoan'
]

for msg in test_messages:
    result = parse_query(msg)
    print(f"Query: {msg}")
    print(f"  Type: {result['query_type']}")
    print(f"  Areas: {result['areas']}")
    print()
