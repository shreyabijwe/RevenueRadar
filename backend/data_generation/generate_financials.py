import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, date
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

fake = Faker()
random.seed(42)
np.random.seed(42)

load_dotenv()

DEPARTMENTS = [
    'Sales', 'Marketing', 'Operations', 'IT', 'HR',
    'Finance', 'Legal', 'Customer Service', 'Logistics', 'Management'
]

REVENUE_CATEGORIES = [
    'Product Sales', 'Service Revenue', 'Subscription', 'Consulting', 'Licensing'
]

EXPENSE_CATEGORIES = [
    'Salaries', 'Rent', 'Marketing', 'Technology', 'Travel',
    'Utilities', 'Supplies', 'Training', 'Insurance', 'Maintenance'
]

# Base monthly revenue and expense by department (AED)
DEPT_BASE_REVENUE = {
    'Sales': 500000, 'Marketing': 150000, 'Operations': 200000,
    'IT': 180000, 'HR': 50000, 'Finance': 120000,
    'Legal': 80000, 'Customer Service': 100000,
    'Logistics': 250000, 'Management': 300000
}

DEPT_BASE_EXPENSE = {
    'Sales': 200000, 'Marketing': 120000, 'Operations': 150000,
    'IT': 140000, 'HR': 80000, 'Finance': 90000,
    'Legal': 60000, 'Customer Service': 70000,
    'Logistics': 180000, 'Management': 100000
}


def generate_monthly_financials():
    records = []
    record_id = 1

    # Generate 3 years of monthly data (2022, 2023, 2024)
    for year in [2022, 2023, 2024]:
        for month in range(1, 13):
            for dept in DEPARTMENTS:
                # Add growth trend — 5% yearly growth
                growth = 1 + (year - 2022) * 0.05

                # Add seasonality — Q4 higher, Q1 lower
                seasonality = 1.0
                if month in [10, 11, 12]:
                    seasonality = 1.15
                elif month in [1, 2]:
                    seasonality = 0.90

                # Revenue with noise
                base_rev = DEPT_BASE_REVENUE[dept]
                revenue = round(base_rev * growth * seasonality * random.uniform(0.85, 1.15), 2)

                # Expense with noise
                base_exp = DEPT_BASE_EXPENSE[dept]
                expense = round(base_exp * growth * random.uniform(0.90, 1.10), 2)

                # Budget (set at start of year, slightly optimistic)
                budget_revenue = round(base_rev * growth * 1.05, 2)
                budget_expense = round(base_exp * growth * 0.95, 2)

                profit = round(revenue - expense, 2)
                profit_margin = round((profit / revenue) * 100, 2) if revenue > 0 else 0

                records.append({
                    'id': record_id,
                    'year': year,
                    'month': month,
                    'month_name': date(year, month, 1).strftime('%B'),
                    'department': dept,
                    'revenue': revenue,
                    'expense': expense,
                    'profit': profit,
                    'profit_margin': profit_margin,
                    'budget_revenue': budget_revenue,
                    'budget_expense': budget_expense,
                    'revenue_category': random.choice(REVENUE_CATEGORIES),
                    'expense_category': random.choice(EXPENSE_CATEGORIES),
                })
                record_id += 1

    return pd.DataFrame(records)


def save_to_csv(df):
    os.makedirs('exports', exist_ok=True)
    path = 'exports/financials.csv'
    df.to_csv(path, index=False)
    print(f"Saved to {path}")


def save_to_postgres(df):
    db_url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(db_url)

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS financials (
                id INTEGER PRIMARY KEY,
                year INTEGER,
                month INTEGER,
                month_name VARCHAR(20),
                department VARCHAR(50),
                revenue NUMERIC(15,2),
                expense NUMERIC(15,2),
                profit NUMERIC(15,2),
                profit_margin NUMERIC(6,2),
                budget_revenue NUMERIC(15,2),
                budget_expense NUMERIC(15,2),
                revenue_category VARCHAR(50),
                expense_category VARCHAR(50)
            )
        """))
        conn.commit()
        print("Table created successfully.")

    df.to_sql('financials', engine, if_exists='replace', index=False)
    print("Data loaded into PostgreSQL successfully.")


if __name__ == "__main__":
    print("Generating financial records...")
    df = generate_monthly_financials()
    print(f"Generated {len(df)} records.")
    print(f"Years: 2022-2024 | Departments: {len(DEPARTMENTS)} | Months: 36")
    save_to_csv(df)
    save_to_postgres(df)
    print("ETL complete.")