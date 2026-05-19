import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('exports/charts', exist_ok=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv('exports/financials.csv')
    return df

# ── 1. Profit Margin Analysis ─────────────────────────────────────────────────
def profit_margin_analysis(df):
    dept_margin = df.groupby('department').agg(
        Total_Revenue=('revenue', 'sum'),
        Total_Expense=('expense', 'sum'),
        Total_Profit=('profit', 'sum'),
        Avg_Margin=('profit_margin', 'mean')
    ).reset_index().round(2)

    dept_margin['ROI'] = ((dept_margin['Total_Profit'] / dept_margin['Total_Expense']) * 100).round(2)
    dept_margin['Cost_Ratio'] = ((dept_margin['Total_Expense'] / dept_margin['Total_Revenue']) * 100).round(2)

    print("\n── Financial Ratios by Department ────────────────")
    print(dept_margin[['department', 'Avg_Margin', 'ROI', 'Cost_Ratio']].to_string(index=False))

    # Bar chart
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    dept_margin.sort_values('Avg_Margin').plot(
        kind='barh', x='department', y='Avg_Margin',
        ax=axes[0], color='#1B3A6B', legend=False
    )
    axes[0].set_title('Avg Profit Margin % by Department')
    axes[0].set_xlabel('Profit Margin %')

    dept_margin.sort_values('ROI').plot(
        kind='barh', x='department', y='ROI',
        ax=axes[1], color='#2E86AB', legend=False
    )
    axes[1].set_title('ROI % by Department')
    axes[1].set_xlabel('ROI %')

    dept_margin.sort_values('Cost_Ratio').plot(
        kind='barh', x='department', y='Cost_Ratio',
        ax=axes[2], color='#e74c3c', legend=False
    )
    axes[2].set_title('Cost Ratio % by Department')
    axes[2].set_xlabel('Cost Ratio %')

    plt.tight_layout()
    plt.savefig('exports/charts/financial_ratios.png', dpi=150)
    plt.close()
    print("Financial ratios chart saved.")
    return dept_margin

# ── 2. Year over Year Growth ──────────────────────────────────────────────────
def yoy_growth(df):
    yearly = df.groupby('year').agg(
        Revenue=('revenue', 'sum'),
        Expense=('expense', 'sum'),
        Profit=('profit', 'sum')
    ).reset_index()

    yearly['Revenue_Growth_%'] = yearly['Revenue'].pct_change() * 100
    yearly['Expense_Growth_%'] = yearly['Expense'].pct_change() * 100
    yearly['Profit_Growth_%']  = yearly['Profit'].pct_change() * 100
    yearly = yearly.round(2)

    print("\n── Year over Year Growth ─────────────────────────")
    print(yearly.to_string(index=False))

    plt.figure(figsize=(10, 5))
    x = yearly['year'].astype(str)
    width = 0.25
    x_pos = np.arange(len(x))

    plt.bar(x_pos - width, yearly['Revenue'] / 1e6, width, label='Revenue (M)', color='#1B3A6B')
    plt.bar(x_pos,         yearly['Expense'] / 1e6, width, label='Expense (M)', color='#e74c3c')
    plt.bar(x_pos + width, yearly['Profit'] / 1e6,  width, label='Profit (M)',  color='#27ae60')

    plt.xticks(x_pos, x)
    plt.title('Year over Year — Revenue, Expense, Profit (AED Millions)')
    plt.ylabel('Amount (AED Millions)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('exports/charts/yoy_growth.png', dpi=150)
    plt.close()
    print("YoY growth chart saved.")
    return yearly

# ── 3. Correlation Analysis ───────────────────────────────────────────────────
def correlation_analysis(df):
    cols = ['revenue', 'expense', 'profit', 'profit_margin', 'budget_revenue', 'budget_expense']
    corr = df[cols].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Financial Metrics Correlation Matrix')
    plt.tight_layout()
    plt.savefig('exports/charts/correlation_matrix.png', dpi=150)
    plt.close()

    r, p = stats.pearsonr(df['revenue'], df['profit'])
    print(f"\nPearson Correlation (Revenue vs Profit): r={r:.4f}, p={p:.4f}")
    print("Correlation matrix saved.")

# ── 4. Revenue Distribution ───────────────────────────────────────────────────
def revenue_distribution(df):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    sns.histplot(df['revenue'], bins=30, kde=True, color='#1B3A6B')
    plt.title('Revenue Distribution')
    plt.xlabel('Revenue (AED)')

    plt.subplot(1, 2, 2)
    sns.histplot(df['profit_margin'], bins=30, kde=True, color='#27ae60')
    plt.title('Profit Margin Distribution')
    plt.xlabel('Profit Margin %')

    plt.tight_layout()
    plt.savefig('exports/charts/revenue_distribution.png', dpi=150)
    plt.close()
    print("Revenue distribution chart saved.")

# ── 5. Save Analysis CSV ──────────────────────────────────────────────────────
def save_analysis(dept_margin, yearly):
    dept_margin.to_csv('exports/financial_ratios.csv', index=False)
    yearly.to_csv('exports/yoy_growth.csv', index=False)
    print("Analysis saved to exports/financial_ratios.csv and exports/yoy_growth.csv")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading data...")
    df = load_data()

    print("Running profit margin analysis...")
    dept_margin = profit_margin_analysis(df)

    print("Running YoY growth analysis...")
    yearly = yoy_growth(df)

    print("Running correlation analysis...")
    correlation_analysis(df)

    print("Running revenue distribution analysis...")
    revenue_distribution(df)

    save_analysis(dept_margin, yearly)

    print("\nPhase 4 complete.")