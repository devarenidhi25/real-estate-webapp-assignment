# Backend-Frontend Integration Guide

## Overview
Your Django backend is now fully connected to your React frontend. The backend runs on port 8000 and the frontend runs on port 3000.

---

## API Endpoint Details

### Backend (Django)
- **Base URL:** `http://localhost:8000`
- **API Endpoint:** `POST /api/query/`
- **Port:** 8000

### Request Format
```json
{
  "message": "Show me price growth in Baner over last 5 years"
}
```

### Response Format
```json
{
  "summary": "Price analysis for Baner over the last 5 years: Prices increased from ₹45L to ₹62L, showing a growth of 37.8%.",
  "action": "price_growth",
  "areas": ["Baner"],
  "chart": {
    "labels": ["2019", "2020", "2021", "2022", "2023"],
    "datasets": [
      {
        "label": "Price Trend",
        "data": [45, 48, 52, 58, 62]
      }
    ]
  },
  "table": [
    { "Year": 2019, "Area": "Sq.ft", "Price": "₹45L", "Demand": "High", "Growth": "0%" },
    { "Year": 2020, "Area": "Sq.ft", "Price": "₹48L", "Demand": "High", "Growth": "6.7%" },
    ...
  ],
  "summaryData": {
    "firstYearPrice": 4500000,
    "lastYearPrice": 6200000,
    "priceGrowthPercent": 37.8,
    "firstYear": "2019",
    "lastYear": "2023"
  }
}
```

---

## Files Modified

### Backend Files
1. **`backend/backend/settings.py`**
   - Updated `ALLOWED_HOSTS` to accept localhost connections
   - Already has CORS and REST framework configured

### Frontend Files
1. **`frontend/src/api/apiClient.js`** - API client (no changes needed, already configured)
2. **`frontend/src/hooks/useChatQuery.js`** - Now uses real API instead of mock data
3. **`frontend/src/context/QueryContext.jsx`** - Removed Next.js "use client" directive
4. **`frontend/src/components/TrendChart.jsx`** - Removed Next.js "use client" directive
5. **`frontend/.env.local`** - New file with API URL configuration
6. **`frontend/package.json`** - Uses Create React App (not Vite)

---

## How to Run

### 1. Start Backend
```bash
cd backend
python manage.py runserver
```
- Backend will run on: `http://localhost:8000`
- API endpoint: `http://localhost:8000/api/query/`

### 2. Start Frontend (in a new terminal)
```bash
cd frontend
npm install  # Only needed first time
npm start
```
- Frontend will run on: `http://localhost:3000`
- Automatically opens in browser

---

## Data Flow

1. **User enters query in ChatInput component**
2. **Query sent to useChatQuery hook**
3. **Hook calls apiClient.query()**
4. **APIClient makes POST request to Django backend**
5. **Django processes query using:**
   - `parse_query()` - Parse natural language
   - `analyze_price_growth()`, `compare_areas()`, `analyze_demand_trend()` - Get analysis
   - Generates natural language summary
6. **Backend returns formatted response**
7. **Frontend displays:**
   - Summary text in ResponseSummary component
   - Chart in TrendChart component
   - Table in DataTable component

---

## Supported Query Types

1. **Price Growth Analysis**
   - "Show me price growth in Baner"
   - "Analyze price trends in Hinjewadi"
   - Action: `price_growth`

2. **Area Comparison**
   - "Compare Baner and Hinjewadi"
   - "Which area has better growth - Wakad or Aundh?"
   - Action: `compare`

3. **Demand Trend Analysis**
   - "Show demand trend in Baner"
   - "Analyze demand for Hinjewadi"
   - Action: `demand_trend`

---

## Environment Variables

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:8000
```

For production, update to:
```
REACT_APP_API_URL=https://your-domain.com
```

### Backend (backend/settings.py)
- DEBUG = True (development)
- Change to False for production
- Add your production domain to ALLOWED_HOSTS

---

## CORS Configuration

Your backend already has CORS configured for:
- `http://localhost:3000` (React frontend)

For production, update in `backend/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]
```

---

## Error Handling

### Frontend
- All API errors are caught and displayed to user
- Check browser console for detailed error logs
- Error messages appear in chat interface

### Backend
- Returns 400 for missing/invalid request data
- Returns 500 for server errors
- All errors include helpful error messages

---

## Testing

### Test with curl (Backend API)
```bash
curl -X POST http://localhost:8000/api/query/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me price growth in Baner"}'
```

### Manual Testing Steps
1. Start both backend and frontend
2. Type a query in the chat input
3. Verify response appears in chat
4. Check chart displays data
5. Verify table shows analysis

---

## Troubleshooting

### "API Error" in frontend
- Check backend is running on port 8000
- Verify REACT_APP_API_URL in .env.local is correct
- Check browser console for detailed error

### CORS Error
- Verify `http://localhost:3000` is in CORS_ALLOWED_ORIGINS
- Restart Django backend after settings change

### No data displayed
- Check backend response format matches expected structure
- Verify chart data has labels and datasets
- Check table data is properly formatted

---

## Next Steps for Deployment

1. **Frontend Build:**
   ```bash
   cd frontend
   npm run build
   ```
   Creates `build/` folder ready for deployment

2. **Backend Production:**
   - Set DEBUG = False
   - Use production-grade server (Gunicorn)
   - Set appropriate ALLOWED_HOSTS
   - Use environment variables for SECRET_KEY

3. **Deploy to:**
   - Vercel (Frontend)
   - Heroku/Railway/PythonAnywhere (Backend)
   - Or use Docker containers

---

## API Response Data Structure

The backend returns data tailored to each analysis type:

### Price Growth Response
```json
{
  "summaryData": {
    "firstYearPrice": 4500000,
    "lastYearPrice": 6200000,
    "priceGrowthPercent": 37.8,
    "firstYear": "2019",
    "lastYear": "2023"
  }
}
```

### Area Comparison Response
```json
{
  "summaryData": {
    "areaComparison": [
      {
        "area": "Baner",
        "priceGrowthPercent": 37.8
      },
      {
        "area": "Hinjewadi",
        "priceGrowthPercent": 28.5
      }
    ],
    "firstYear": "2019",
    "lastYear": "2023"
  }
}
```

### Demand Trend Response
```json
{
  "summaryData": {
    "totalDemand": 1250,
    "demandChangePercent": 15.3,
    "firstYear": "2019",
    "lastYear": "2023"
  }
}
```
