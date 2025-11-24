#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from realestate.services.analysis import compare_areas

result = compare_areas(['Wakad', 'Aundh', 'Ambegaon Budruk'])
print("Table data (first 3 rows):")
for row in result['table'][:3]:
    print(f"  {row['year']} {row['location']}: Price={row['price']}, Demand={row.get('demand')}")
