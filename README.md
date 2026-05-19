# RevenueRadar — Financial Analytics Platform

A full-stack financial analytics platform that tracks revenue, expenses, profits, forecasts cash flow, and generates automated Excel + PDF reports.

## 🔗 Live Demo
- **Frontend:** https://revenue-radar-ytus.vercel.app
- **API:** https://revenueradar-api.onrender.com/docs
- **Login:** admin / radar2024

## 🚀 Features
- 360 monthly financial records across 3 years (2022–2024) with ETL pipeline
- Revenue forecasting for next 6 months using Exponential Smoothing
- Expense anomaly detection using statistical analysis
- Financial ratio analysis — profit margin, ROI, cost ratio by department
- Year over Year growth analysis with visualizations
- Auto-generated Excel workbook with 6 sheets — P&L, Budget vs Actual, trends
- Auto-generated PDF report with executive summary and embedded charts
- React dashboard with dark navy + gold theme — KPI cards, 4 interactive charts
- REST API with JWT authentication

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Generation | Python, Faker, pandas |
| Database | PostgreSQL |
| Forecasting | statsmodels, Exponential Smoothing |
| Statistical Analysis | scipy, seaborn |
| Backend API | FastAPI, JWT Auth |
| Excel Reports | openpyxl |
| PDF Reports | reportlab |
| Frontend | React, Recharts |
| Deployment | Render (API), Vercel (Frontend) |

## 📊 Project Modules

### 1. Financial Database & ETL
- 360 monthly records across 10 departments
- Revenue, expense, profit, budget data
- Growth trends and seasonality built in

### 2. Excel Financial Workbook
- P&L Statement by year and month
- Budget vs Actual analysis with variance
- Monthly trends with line chart
- Department cost breakdown with pie chart
- Executive financial dashboard

### 3. Revenue Forecasting Model
- Exponential Smoothing with trend and seasonality
- 6-month revenue forecast
- Confidence intervals
- Expense anomaly detection

### 4. Financial Ratio Analysis
- Profit margin, ROI, cost ratio by department
- Year over Year growth analysis
- Correlation matrix
- Revenue distribution analysis

### 5. FastAPI Backend
- 7 REST endpoints with JWT authentication
- Revenue, KPIs, forecast, budget vs actual

### 6. React Dashboard
- Dark navy + gold theme
- KPI cards — AED 74M revenue, AED 29M profit
- Revenue by department chart
- Budget vs Actual chart
- 6-month forecast line chart

### 7. Automated Report Generator
- One-click PDF financial report
- Auto-written CFO executive summary
- Embedded charts and department table

## 🏃 Run Locally

### Backend
```bash
pip install -r requirements.txt
python backend/data_generation/generate_financials.py
uvicorn backend.api.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure
revenueradar/
├── backend/
│   ├── api/              # FastAPI endpoints
│   ├── data_generation/  # ETL pipeline
│   ├── etl/              # Financial analysis
│   ├── ml_models/        # Forecasting model
│   └── reports/          # Excel & PDF generators
├── frontend/
│   └── src/
│       └── components/   # React components
└── exports/
├── excel/            # Generated Excel reports
└── pdf/              # Generated PDF reports
## 👩‍💻 Author
**Shreya Bijwe**
- GitHub: [@shreyabijwe](https://github.com/shreyabijwe)
- LinkedIn: [Shreya Bijwe](https://www.linkedin.com/in/shreya-bijwe-4a126b299)
## 📄 License
MIT License