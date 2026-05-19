import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
import os
warnings.filterwarnings('ignore')

os.makedirs('exports/charts', exist_ok=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv('exports/financials.csv')
    monthly = df.groupby(['year', 'month']).agg(
        Revenue=('revenue', 'sum'),
        Expense=('expense', 'sum'),
        Profit=('profit', 'sum')
    ).reset_index().sort_values(['year', 'month'])
    monthly['date'] = pd.to_datetime(
        monthly['year'].astype(str) + '-' + monthly['month'].astype(str) + '-01'
    )
    monthly = monthly.set_index('date')
    return monthly

# ── Exponential Smoothing Forecast ────────────────────────────────────────────
def forecast_revenue(monthly):
    revenue = monthly['Revenue']

    # Train on first 30 months, test on last 6
    train = revenue.iloc[:-6]
    test  = revenue.iloc[-6:]

    model = ExponentialSmoothing(
        train,
        trend='add',
        seasonal='add',
        seasonal_periods=12
    ).fit()

    # Forecast next 6 months (test period)
    fitted = model.forecast(6)

    # Evaluate
    mae  = mean_absolute_error(test, fitted)
    rmse = np.sqrt(mean_squared_error(test, fitted))
    print(f"\nModel Evaluation:")
    print(f"  MAE  : AED {mae:,.2f}")
    print(f"  RMSE : AED {rmse:,.2f}")

    # Forecast next 6 months beyond data
    future_model = ExponentialSmoothing(
        revenue,
        trend='add',
        seasonal='add',
        seasonal_periods=12
    ).fit()
    future_forecast = future_model.forecast(6)

    return revenue, fitted, future_forecast, test

# ── Anomaly Detection ─────────────────────────────────────────────────────────
def detect_anomalies(monthly):
    expense = monthly['Expense']
    mean = expense.mean()
    std  = expense.std()

    anomalies = expense[(expense > mean + 2 * std) | (expense < mean - 2 * std)]
    print(f"\nAnomaly Detection:")
    print(f"  Mean Expense : AED {mean:,.2f}")
    print(f"  Std Dev      : AED {std:,.2f}")
    print(f"  Anomalies found: {len(anomalies)}")
    if len(anomalies) > 0:
        print(anomalies)
    return anomalies

# ── Plot Forecast ─────────────────────────────────────────────────────────────
def plot_forecast(revenue, fitted, future_forecast, test):
    plt.figure(figsize=(14, 6))

    plt.plot(revenue.index, revenue.values, label='Actual Revenue', color='#1B3A6B', linewidth=2)
    plt.plot(test.index, fitted.values, label='Fitted (Test)', color='#F18F01', linewidth=2, linestyle='--')
    plt.plot(future_forecast.index, future_forecast.values,
             label='Forecast (Next 6 Months)', color='#27ae60', linewidth=2, linestyle='--', marker='o')

    plt.fill_between(future_forecast.index,
                     future_forecast.values * 0.90,
                     future_forecast.values * 1.10,
                     alpha=0.2, color='#27ae60', label='Confidence Interval (±10%)')

    plt.title('Revenue Forecast — Next 6 Months', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Revenue (AED)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('exports/charts/revenue_forecast.png', dpi=150)
    plt.close()
    print("Revenue forecast chart saved.")

    # Print forecast values
    print("\nRevenue Forecast — Next 6 Months:")
    for date, val in future_forecast.items():
        print(f"  {date.strftime('%B %Y')} : AED {val:,.2f}")

# ── Plot Anomalies ────────────────────────────────────────────────────────────
def plot_anomalies(monthly, anomalies):
    expense = monthly['Expense']
    mean = expense.mean()
    std  = expense.std()

    plt.figure(figsize=(14, 5))
    plt.plot(expense.index, expense.values, label='Monthly Expense', color='#1B3A6B', linewidth=2)
    plt.axhline(mean + 2 * std, color='red', linestyle='--', label='Upper Threshold')
    plt.axhline(mean - 2 * std, color='red', linestyle='--', label='Lower Threshold')

    if len(anomalies) > 0:
        plt.scatter(anomalies.index, anomalies.values, color='red', zorder=5, s=100, label='Anomalies')

    plt.title('Expense Anomaly Detection', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Expense (AED)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('exports/charts/expense_anomalies.png', dpi=150)
    plt.close()
    print("Anomaly detection chart saved.")

# ── Save Forecast CSV ─────────────────────────────────────────────────────────
def save_forecast(future_forecast):
    forecast_df = pd.DataFrame({
        'date': future_forecast.index.strftime('%Y-%m'),
        'forecasted_revenue': future_forecast.values.round(2)
    })
    forecast_df.to_csv('exports/forecast.csv', index=False)
    print("Forecast saved to exports/forecast.csv")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading financial data...")
    monthly = load_data()
    print(f"Data shape: {monthly.shape}")

    print("\nTraining forecasting model...")
    revenue, fitted, future_forecast, test = forecast_revenue(monthly)

    print("\nDetecting anomalies...")
    anomalies = detect_anomalies(monthly)

    print("\nGenerating charts...")
    plot_forecast(revenue, fitted, future_forecast, test)
    plot_anomalies(monthly, anomalies)

    save_forecast(future_forecast)

    print("\nPhase 3 complete.")