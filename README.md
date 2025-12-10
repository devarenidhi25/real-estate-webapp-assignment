# Real Estate Analysis Chatbot 🏠

A sophisticated AI-powered chatbot for analyzing and comparing real estate market data across multiple areas in Pune, India. The application uses natural language processing to understand user queries and provides detailed insights on price trends, demand patterns, and area comparisons.

## 🎯 Project Overview

The Real Estate Analysis Chatbot is a full-stack web application that enables users to query real estate data using natural language. It processes queries about property prices, market demand, and area comparisons, then visualizes the data through interactive charts and detailed tables.

### Key Features

- **Natural Language Processing**: Understand complex queries without strict syntax requirements
- **Price Growth Analysis**: Track historical price trends for specific areas
- **Area Comparisons**: Compare multiple areas side-by-side with grouped bar charts
- **Demand Analytics**: Analyze sales trends and market demand patterns
- **Voice Integration**: 
  - 🎤 Speech-to-text input for queries
  - 🔊 Text-to-speech output for chatbot responses
- **Interactive Visualizations**: Real-time charts and sortable data tables
- **Currency Formatting**: Automatic ₹ (Rupee) formatting for prices
- **Real-time Data**: Analysis based on actual Excel data (20 rows, 5 years)

## 📊 Tech Stack

### Backend
- **Framework**: Django 5.2.8
- **API**: Django REST Framework (DRF)
- **Language**: Python 3.11+
- **Data Processing**: Pandas, NumPy
- **Data Format**: Excel (.xlsx)
- **Server**: Django Development Server (Gunicorn for production)

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Create React App (CRA)
- **Styling**: Bootstrap 5.3.0 + Custom CSS
- **Icons**: Font Awesome 6.4.0, Bootstrap Icons
- **State Management**: React Context API
- **HTTP Client**: Fetch API with custom axios-like client
- **Voice APIs**: Web Speech API (SpeechRecognition, SpeechSynthesis)
- **Charting**: Canvas-based custom chart renderer

### Database
- **SQLite3** (default Django database)

### DevOps & Tools
- **Version Control**: Git & GitHub
- **Task Automation**: start.bat (Windows batch script)
- **API Testing**: cURL, Postman-compatible

## 📁 Project Structure

```
RealEstate_assignment/
├── backend/                          # Django Backend
│   ├── manage.py
│   ├── db.sqlite3
│   ├── backend/
│   │   ├── settings.py              # Django configuration
│   │   ├── urls.py                  # API routes
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── realestate/                  # Main app
│   │   ├── models.py
│   │   ├── views.py                 # API endpoints
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   ├── data/
│   │   │   └── Sample_data.xlsx     # Real estate data (20 rows)
│   │   ├── migrations/
│   │   ├── services/
│   │   │   ├── data_loader.py       # Excel data loading
│   │   │   └── analysis.py          # Business logic
│   │   └── utils/
│   │       └── text_parsing.py      # NLP query parsing
│   └── requirements.txt
│
├── frontend/                         # React Frontend
│   ├── package.json
│   ├── public/
│   │   ├── index.html               # Entry HTML
│   │   └── images/
│   │       └── logo.png             # Website logo & favicon
│   ├── src/
│   │   ├── index.js
│   │   ├── App.jsx
│   │   ├── api/
│   │   │   └── apiClient.js         # API communication
│   │   ├── components/
│   │   │   ├── ChatInput.jsx        # Input with mic
│   │   │   ├── ChatMessage.jsx      # Message display
│   │   │   ├── VoiceListener.jsx    # Text-to-speech
│   │   │   ├── TrendChart.jsx       # Canvas-based charts
│   │   │   ├── DataTable.jsx        # Data visualization
│   │   │   └── ResponseSummary.jsx  # Summary display
│   │   ├── context/
│   │   │   └── QueryContext.jsx     # Global state
│   │   ├── hooks/
│   │   │   └── useChatQuery.js      # Chat logic
│   │   ├── pages/
│   │   │   └── ChatPage.jsx         # Main page
│   │   ├── styles/
│   │   │   ├── chatpage.css         # Main styles
│   │   │   └── global.css           # Global styles
│   │   └── utils/
│   │       └── formatters.js        # Data formatting
│   └── .env.local                   # Environment config
│
├── start.bat                         # Quick start script
├── README.md                         # This file
├── .gitignore
└── LICENSE

```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/devarenidhi25/real-estate-webapp-assignment.git
   cd RealEstate_assignment
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py runserver
   ```
   Backend will run on `http://localhost:8000`

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   Frontend will run on `http://localhost:3000`

### Quick Start (Windows)
   ```bash
   start.bat
   ```
   This will automatically start both backend and frontend servers.

## 💼 Business Value & Applications

### Real Estate Industry
- **Market Intelligence**: Understand pricing trends across different areas
- **Investment Analysis**: Compare multiple locations for real estate investments
- **Demand Forecasting**: Analyze market demand to identify growth opportunities
- **Competitive Analysis**: Compare area performance metrics

### Target Users
- **Real Estate Agents**: Quick property market analysis
- **Investors**: Investment decision making with data-driven insights
- **Developers**: Market research before launching new projects
- **Property Buyers**: Area comparison before purchasing
- **Market Analysts**: Trend identification and forecasting

### Key Business Applications
1. **Price Trend Analysis**: Historical price movements (2020-2024)
2. **Market Comparisons**: Side-by-side area performance metrics
3. **Demand Insights**: Sales volume and demand trends
4. **Growth Metrics**: Year-over-year growth calculations
5. **Data-Driven Decision Making**: Excel-based, verifiable data source

## 🔧 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### 1. Query Endpoint
**POST** `/api/query/`

Request:
```json
{
  "message": "Compare Aundh Wakad Ambegaon"
}
```

Response:
```json
{
  "summary": "Comparison summary text...",
  "action": "compare",
  "areas": ["Aundh", "Wakad", "Ambegaon Budruk"],
  "chart": {
    "labels": [2020, 2021, 2022, 2023, 2024],
    "datasets": [
      {
        "label": "Aundh",
        "data": [8888.99, 9366.13, 9443.87, 10426.22, 11774.09]
      }
    ]
  },
  "table": [
    {
      "year": 2020,
      "location": "Aundh",
      "price": 8888.99,
      "demand": 598
    }
  ]
}
```

### Query Types
- **Price Growth**: "Show price growth in Wakad" → Analyzes price trends
- **Area Comparison**: "Compare Aundh Wakad Ambegaon" → Compares multiple areas
- **Demand Analysis**: "Show demand in Aundh" → Analyzes sales/demand trends
- **Greetings**: "Hi", "Hello" → Interactive greeting
- **Farewells**: "Bye", "Thanks" → Closing message

## 📊 Data Source

- **File**: `Sample_data.xlsx`
- **Location**: `backend/realestate/data/`
- **Rows**: 20 (4 areas × 5 years)
- **Years**: 2020-2024
- **Areas**: Akurdi, Aundh, Ambegaon Budruk, Wakad
- **Metrics**: Price (₹), Demand (units), Growth rate (%)

## 🎤 Voice Features

### Speech-to-Text (Input)
- Click the **microphone icon** in the input field
- Speak your query naturally
- Automatically filled in the input field
- Supported languages: English (US)

### Text-to-Speech (Output)
- Click the **volume icon** on any chatbot response
- Listen to the response read aloud
- Adjustable playback (standard rate/pitch/volume)

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark-friendly Theming**: Professional blue gradient header
- **Real-time Visualization**: Interactive charts and tables
- **Currency Formatting**: Automatic ₹ symbol with proper comma separation
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages

## 🔐 Security

- CORS enabled for localhost development
- Environment-based configuration (.env.local)
- Input validation and sanitization
- No sensitive data in repository

## 📈 Performance

- **Response Time**: < 500ms for typical queries
- **Data Loading**: 20 rows cached at startup
- **Chart Rendering**: Smooth canvas-based rendering
- **Memory**: Efficient pandas-based data processing

## 🚀 Deployment

### Backend (Django)
```bash
# Production settings in settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Use Gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (React)
```bash
npm run build
# Deploy build/ folder to static hosting (Vercel, Netlify, etc.)
```

## 📝 Example Queries

```
1. "Show me price growth in Wakad over last 5 years"
2. "Compare Aundh Wakad Ambegaon"
3. "What's the demand trend in Akurdi?"
4. "Analyze price movement in Aundh 2020 to 2024"
5. "Which area has highest growth - Wakad or Aundh?"
```

## 🛠️ Development

### Adding New Features

1. **New Query Type**: Edit `text_parsing.py` and `analysis.py`
2. **New Chart Type**: Extend `TrendChart.jsx`
3. **New Data Column**: Update `Sample_data.xlsx` and analysis functions

### Testing
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

## 📚 Technologies Used in Detail

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Natural Language Understanding | Custom Regex Parser | Query interpretation |
| Data Analysis | Pandas/NumPy | Time-series analysis |
| Visualization | Canvas API | Dynamic charting |
| Voice Input | Web Speech API | Speech recognition |
| Voice Output | Speech Synthesis API | Text-to-speech |
| State Management | React Context | Global state |
| Styling | CSS3 + Bootstrap | Responsive UI |
| Icons | Font Awesome 6 | Professional icons |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**Nidhi** - Real Estate Chatbot Assignment
- GitHub: [@devarenidhi25](https://github.com/devarenidhi25)
- Repository: [real-estate-webapp-assignment](https://github.com/devarenidhi25/real-estate-webapp-assignment)

## 📞 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include screenshots/error messages if applicable

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

## 🗺️ Roadmap

- [ ] Database integration (PostgreSQL)
- [ ] User authentication & profiles
- [ ] Data export (CSV/PDF)
- [ ] Advanced analytics (predictions, forecasting)
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Real-time data updates
- [ ] API rate limiting & caching

---

**Last Updated**: December 2025
**Status**: ✅ Production Ready
**Version**: 1.0.0
