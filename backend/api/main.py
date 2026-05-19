from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import numpy as np
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RevenueRadar — Financial Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ── JWT Config ─────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("JWT_SECRET", "revenueradar_secret_key_shreya_2024")
ALGORITHM  = "HS256"
security   = HTTPBearer()

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ── Load Data ──────────────────────────────────────────────────────────────────
def get_df():
    return pd.read_csv('exports/financials.csv')

def get_forecast():
    return pd.read_csv('exports/forecast.csv')

# ── Auth Models ────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "RevenueRadar Financial Analytics API", "status": "running"}

# Login
@app.post("/login")
def login(req: LoginRequest):
    if req.username == "admin" and req.password == "radar2024":
        token = create_token(req.username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# KPIs
@app.get("/kpis")
def get_kpis(user=Depends(verify_token)):
    df = get_df()
    total_revenue  = round(df['revenue'].sum(), 2)
    total_expense  = round(df['expense'].sum(), 2)
    total_profit   = round(df['profit'].sum(), 2)
    avg_margin     = round(df['profit_margin'].mean(), 2)
    best_dept      = df.groupby('department')['profit'].sum().idxmax()
    latest_year    = df['year'].max()
    latest_revenue = round(df[df['year'] == latest_year]['revenue'].sum(), 2)
    return {
        "total_revenue": total_revenue,
        "total_expense": total_expense,
        "total_profit": total_profit,
        "avg_profit_margin": avg_margin,
        "best_department": best_dept,
       "latest_year_revenue": latest_revenue,
    }

# Revenue by department
@app.get("/revenue-by-dept")
def revenue_by_dept(year: Optional[int] = None, user=Depends(verify_token)):
    df = get_df()
    if year:
        df = df[df['year'] == year]
    result = df.groupby('department').agg(
        revenue=('revenue', 'sum'),
        expense=('expense', 'sum'),
        profit=('profit', 'sum'),
        avg_margin=('profit_margin', 'mean')
    ).reset_index().round(2)
    return result.to_dict(orient='records')

# Monthly trends
@app.get("/monthly-trends")
def monthly_trends(year: Optional[int] = None, user=Depends(verify_token)):
    df = get_df()
    if year:
        df = df[df['year'] == year]
    result = df.groupby(['year', 'month', 'month_name']).agg(
        revenue=('revenue', 'sum'),
        expense=('expense', 'sum'),
        profit=('profit', 'sum')
    ).reset_index().sort_values(['year', 'month']).round(2)
    return result.to_dict(orient='records')

# Budget vs actual
@app.get("/budget-vs-actual")
def budget_vs_actual(user=Depends(verify_token)):
    df = get_df()
    result = df.groupby('department').agg(
        actual_revenue=('revenue', 'sum'),
        budget_revenue=('budget_revenue', 'sum'),
        actual_expense=('expense', 'sum'),
        budget_expense=('budget_expense', 'sum'),
    ).reset_index().round(2)
    result['revenue_variance'] = (result['actual_revenue'] - result['budget_revenue']).round(2)
    result['variance_pct'] = ((result['revenue_variance'] / result['budget_revenue']) * 100).round(2)
    return result.to_dict(orient='records')

# Revenue forecast
@app.get("/forecast")
def get_forecast_data(user=Depends(verify_token)):
    df = get_forecast()
    return df.to_dict(orient='records')

# YoY growth
@app.get("/yoy-growth")
def yoy_growth(user=Depends(verify_token)):
    df = get_df()
    yearly = df.groupby('year').agg(
        revenue=('revenue', 'sum'),
        expense=('expense', 'sum'),
        profit=('profit', 'sum')
    ).reset_index().round(2)
    yearly['revenue_growth'] = yearly['revenue'].pct_change().round(4) * 100
    yearly['profit_growth']  = yearly['profit'].pct_change().round(4) * 100
    return yearly.to_dict(orient='records')

# Generate report
@app.get("/generate-report")
def generate_report(user=Depends(verify_token)):
    from backend.reports.excel_report import generate_excel_report
    generate_excel_report()
    return {"message": "Report generated", "path": "exports/excel/RevenueRadar_Financial_Report.xlsx"}