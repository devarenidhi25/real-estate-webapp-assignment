# 🎯 Integration Overview - Visual Guide

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│                    REACT FRONTEND (Port 3000)                   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    ChatPage.jsx                           │   │
│  │  ┌────────────┐  ┌────────────────┐  ┌──────────────┐   │   │
│  │  │ ChatInput  │→ │ useChatQuery   │→ │ apiClient    │   │   │
│  │  │            │  │ (Real API!)    │  │ (Fetch)      │   │   │
│  │  └────────────┘  └────────────────┘  └──────────────┘   │   │
│  │                                              ↓             │   │
│  │  ┌────────────────────────────────────────────────────┐   │   │
│  │  │         QueryContext (State Management)            │   │   │
│  │  │  - Messages                                        │   │   │
│  │  │  - currentResponse (chart, table, summary)         │   │   │
│  │  └────────────────────────────────────────────────────┘   │   │
│  │                          ↓                                  │   │
│  │  ┌──────────────┬──────────────────┬──────────────────┐   │   │
│  │  │ResponseSummary
 │ TrendChart   │ DataTable    │   │   │
│  │  │(Summary text)│ (Price chart)  │ (Analysis table) │   │   │
│  │  └──────────────┴──────────────────┴──────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           ↑                                       │
│                           │ HTTP POST                             │
│                      /api/query/                                  │
│                           │                                       │
└───────────────────────────┼───────────────────────────────────────┘
                            │
                            │
┌───────────────────────────┼───────────────────────────────────────┐
│                           ↓                                        │
│              DJANGO BACKEND (Port 8000)                           │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    views.py                                │  │
│  │                 query_view (@api_view)                     │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           ↓                                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                  utils/text_parsing.py                     │  │
│  │                    parse_query()                           │  │
│  │  Extracts: query_type, areas, years                        │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           ↓                                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              services/analysis.py                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │  │
│  │  │analyze_price │  │compare_areas │  │analyze_demand   │ │  │
│  │  │_growth()     │  │_()           │  │_trend()         │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           ↓                                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              services/data_loader.py                       │  │
│  │  Loads real estate data from CSV/database                 │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           ↓                                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                  _generate_summary()                       │  │
│  │  Creates natural language response summary                │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           ↓                                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              Response (JSON)                               │  │
│  │  {                                                         │  │
│  │    "summary": "...",                                       │  │
│  │    "action": "price_growth",                              │  │
│  │    "areas": ["Baner"],                                    │  │
│  │    "chart": {...},                                        │  │
│  │    "table": [...],                                        │  │
│  │    "summaryData": {...}                                   │  │
│  │  }                                                         │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           ↓                                        │
│                    HTTP Response                                  │
└───────────────────────────┼───────────────────────────────────────┘
                            │
                            ↓ Back to Frontend
```

---

## Data Flow - Step by Step

```
1. USER ACTION
   └─→ Types "Show me price growth in Baner"

2. FRONTEND - ChatInput Component
   └─→ Sends query to useChatQuery hook

3. FRONTEND - useChatQuery Hook
   └─→ Calls apiClient.query(queryText)
   └─→ apiClient makes HTTP POST to backend

4. FRONTEND - HTTP Request Sent
   POST http://localhost:8000/api/query/
   Headers: Content-Type: application/json
   Body: { "message": "Show me price growth in Baner" }

5. BACKEND - views.py (query_view)
   └─→ Receives request
   └─→ Validates message field
   └─→ Calls parse_query(message)

6. BACKEND - text_parsing.py
   └─→ Extracts from natural language:
       • query_type: "price_growth"
       • areas: ["Baner"]
       • years: null (full history)

7. BACKEND - Routing Logic
   └─→ Determines action: price_growth
   └─→ Calls analyze_price_growth("Baner", None)

8. BACKEND - analysis.py
   └─→ Loads data from CSV/database
   └─→ Filters for Baner area
   └─→ Calculates growth metrics:
       • First year price: ₹45L
       • Last year price: ₹62L
       • Growth: 37.8%

9. BACKEND - Chart Data Generation
   └─→ Creates chart with:
       • labels: ["2019", "2020", "2021", "2022", "2023"]
       • datasets: [{ label: "Price Trend", data: [45, 48, 52, 58, 62] }]

10. BACKEND - Table Data Generation
    └─→ Creates rows with year, price, growth data

11. BACKEND - Summary Generation
    └─→ _generate_summary() creates:
        "Price analysis for Baner over the last 5 years: 
         Prices increased from ₹45L to ₹62L, 
         showing a growth of 37.8%."

12. BACKEND - Response Created
    └─→ Returns JSON with summary, action, areas, chart, table

13. FRONTEND - Response Received
    └─→ useChatQuery receives response
    └─→ Stores in QueryContext

14. FRONTEND - Components Update
    └─→ ResponseSummary displays summary text
    └─→ TrendChart displays the chart
    └─→ DataTable displays the table data

15. USER SEES
    └─→ Chat message with their query
    └─→ Bot's summary response
    └─→ Visual chart of price trends
    └─→ Detailed data table
```

---

## Files Connection Map

```
REQUEST CHAIN:
ChatInput.jsx
    ↓
useChatQuery.js (hooks/useChatQuery.js) ⭐ MAIN CONNECTION
    ↓ calls
apiClient.query() (api/apiClient.js)
    ↓ HTTP POST
query_view() (backend/realestate/views.py) ⭐ ENTRY POINT
    ↓ calls
parse_query() (backend/realestate/utils/text_parsing.py)
    ↓ returns query_type, areas, years
    ↓
if price_growth: analyze_price_growth() (backend/realestate/services/analysis.py)
if compare: compare_areas() (backend/realestate/services/analysis.py)
if demand: analyze_demand_trend() (backend/realestate/services/analysis.py)
    ↓ calls
load_data() (backend/realestate/services/data_loader.py)
    ↓
_generate_summary() (backend/realestate/views.py)
    ↓
Return JSON Response
    ↓ HTTP Response
useChatQuery.js
    ↓ updates
QueryContext.jsx (setResponse)
    ↓ triggers re-render
ResponseSummary.jsx (displays summary)
TrendChart.jsx (displays chart)
DataTable.jsx (displays table)
    ↓
USER SEES RESULTS
```

---

## Configuration Points

```
BACKEND CONFIGURATION (backend/settings.py)
├─ ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
├─ CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
├─ INSTALLED_APPS includes 'rest_framework', 'corsheaders'
└─ REST_FRAMEWORK configuration

FRONTEND CONFIGURATION (.env.local)
├─ REACT_APP_API_URL=http://localhost:8000
└─ Used by: apiClient.js

API ROUTE CONFIGURATION (backend/realestate/urls.py)
├─ path('query/', query_view, name='query')
└─ Full URL: http://localhost:8000/api/query/

REACT ENTRY (frontend/public/index.html)
├─ <div id="root"></div>
└─ Root element for React app

REACT STARTUP (frontend/src/index.js)
├─ ReactDOM.createRoot(document.getElementById("root"))
└─ Renders <App /> component
```

---

## Key Integration Points

### 1. API Client Setup ✅
```
apiClient.js:
- Takes REACT_APP_API_URL from .env.local
- Defaults to http://localhost:8000
- Exports query() method for useChatQuery to call
```

### 2. Hook Integration ✅
```
useChatQuery.js:
- Removed mock data
- Now calls: await apiClient.query(queryText)
- Passes response to setResponse() in QueryContext
- Displays messages via addMessage()
```

### 3. State Management ✅
```
QueryContext.jsx:
- Stores messages array
- Stores currentResponse (chart, table, summary)
- Provides hooks for components to access state
```

### 4. Backend Endpoint ✅
```
views.py:
- Receives POST /api/query/
- Body must have: { "message": "..." }
- Returns: { summary, action, areas, chart, table, summaryData }
```

### 5. CORS Setup ✅
```
settings.py:
- corsheaders.middleware.CorsMiddleware enabled
- CORS_ALLOWED_ORIGINS includes http://localhost:3000
- Allows cross-origin requests from frontend
```

---

## Response Format Mapping

```
BACKEND RESPONSE → FRONTEND USE
├─ summary → ResponseSummary.jsx displays
├─ chart → TrendChart.jsx displays (chart.labels, chart.datasets)
├─ table → DataTable.jsx displays
├─ action → Used for conditional rendering
├─ areas → Displayed in summary context
└─ summaryData → Contains metadata (priceGrowthPercent, etc.)
```

---

## Environment Setup

```
.env.local (Frontend)
└─ REACT_APP_API_URL=http://localhost:8000

settings.py (Backend)
├─ DEBUG = True (development)
├─ ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
└─ CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
```

---

## Ready to Run! 🚀

```
TERMINAL 1:
cd backend && python manage.py runserver
→ Server on http://localhost:8000

TERMINAL 2:
cd frontend && npm start
→ Server on http://localhost:3000

→ Open http://localhost:3000 in browser
→ Type a query
→ See results! ✨
```

---

## Troubleshooting Quick Links

| Problem | Check |
|---------|-------|
| API not responding | Backend running on :8000? |
| CORS error | ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS correct? |
| Blank response | Query format valid? Areas recognized? |
| Chart missing | Browser console for JavaScript errors? |
| API timeout | Backend processable? Data files loaded? |

---

**Integration Complete! ✅**
All systems connected and ready to go!
