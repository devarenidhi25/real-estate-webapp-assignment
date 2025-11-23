# ⚡ QUICK START REFERENCE

## 🚀 Start in 30 Seconds

### Windows (Automatic)
```bash
start.bat
```

### macOS/Linux (Manual - 2 Terminals)

**Terminal 1:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2:**
```bash
cd frontend
npm install  # First time only
npm start
```

### Result:
```
✅ Backend: http://localhost:8000
✅ Frontend: http://localhost:3000 (auto-opens)
✅ Ready to use!
```

---

## 🧪 Test It

1. Go to `http://localhost:3000`
2. Type: `Show me price growth in Baner`
3. See: Summary + Chart + Table

---

## 📝 Sample Queries

```
"Show me price growth in Baner"
"Compare Baner and Hinjewadi"
"Analyze demand for Wakad"
"What's the price trend in Aundh?"
```

---

## 🔗 API Endpoints

```
POST http://localhost:8000/api/query/

Request:
{"message": "Your query here"}

Response:
{
  "summary": "...",
  "action": "price_growth|compare|demand_trend",
  "areas": ["Area name"],
  "chart": {...},
  "table": [...],
  "summaryData": {...}
}
```

---

## 📁 Project Structure

```
RealEstate_assignment/
├── backend/          → Django API (port 8000)
├── frontend/         → React app (port 3000)
├── start.bat         → Quick start script
├── INTEGRATION_GUIDE.md
├── INTEGRATION_STATUS.md
├── CHECKLIST.md
├── ARCHITECTURE.md
└── README_INTEGRATION.md (this file)
```

---

## 🔧 Key Files

| File | Purpose |
|------|---------|
| `frontend/src/api/apiClient.js` | API communication |
| `frontend/src/hooks/useChatQuery.js` | Real API integration |
| `frontend/.env.local` | API URL config |
| `backend/backend/settings.py` | CORS & Hosts config |
| `backend/realestate/views.py` | Query endpoint |

---

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| "Cannot reach API" | Check backend running on :8000 |
| CORS error | Verify .env.local and settings.py |
| Blank response | Check browser console for errors |
| npm not found | Install Node.js |
| python not found | Install Python 3.8+ |

---

## 📚 Documentation

- **INTEGRATION_GUIDE.md** - Full integration details
- **ARCHITECTURE.md** - Data flow & diagrams
- **CHECKLIST.md** - Verification steps
- **INTEGRATION_STATUS.md** - Status summary

---

## 🎯 What's Integrated

✅ Frontend calls real Django backend (not mock)
✅ CORS configured for cross-origin requests
✅ API returns analysis data with charts & tables
✅ Chat interface displays responses
✅ Error handling implemented
✅ Both servers ready to run

---

## 🚀 Ready to Go!

Everything is connected and ready. Just run `start.bat` or manually start both servers.

**Enjoy your Real Estate Analysis Chatbot! 🏠**

---

**Questions?** Check the documentation files or browser console for error details.
