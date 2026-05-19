from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, Image, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
from datetime import datetime

# ── Colors ─────────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor('#1B3A6B')
GOLD    = colors.HexColor('#F18F01')
DARK    = colors.HexColor('#0a0e1a')
LIGHT   = colors.HexColor('#D6E4F0')
RED     = colors.HexColor('#e74c3c')
GREEN   = colors.HexColor('#27ae60')
WHITE   = colors.white
GRAY    = colors.HexColor('#888888')

os.makedirs('exports/pdf', exist_ok=True)
os.makedirs('exports/charts', exist_ok=True)

# ── Generate Charts ────────────────────────────────────────────────────────────
def generate_charts(df):
    # Revenue by dept
    dept = df.groupby('department')['revenue'].sum().sort_values()
    plt.figure(figsize=(8, 4))
    dept.plot(kind='barh', color='#F18F01')
    plt.title('Total Revenue by Department (AED)')
    plt.xlabel('Revenue (AED)')
    plt.tight_layout()
    plt.savefig('exports/charts/pdf_revenue.png', dpi=150)
    plt.close()

    # YoY
    yearly = df.groupby('year').agg(
        Revenue=('revenue', 'sum'),
        Expense=('expense', 'sum'),
        Profit=('profit', 'sum')
    ).reset_index()

    x = yearly['year'].astype(str)
    width = 0.25
    x_pos = range(len(x))

    plt.figure(figsize=(8, 4))
    plt.bar([p - width for p in x_pos], yearly['Revenue'] / 1e6, width, label='Revenue', color='#F18F01')
    plt.bar(x_pos,                      yearly['Expense'] / 1e6, width, label='Expense', color='#e74c3c')
    plt.bar([p + width for p in x_pos], yearly['Profit'] / 1e6,  width, label='Profit',  color='#27ae60')
    plt.xticks(list(x_pos), list(x))
    plt.title('Year over Year — Revenue, Expense, Profit (AED Millions)')
    plt.ylabel('AED Millions')
    plt.legend()
    plt.tight_layout()
    plt.savefig('exports/charts/pdf_yoy.png', dpi=150)
    plt.close()

    print("Charts generated for PDF.")

# ── Executive Summary ──────────────────────────────────────────────────────────
def generate_summary(df):
    total_revenue = round(df['revenue'].sum(), 0)
    total_expense = round(df['expense'].sum(), 0)
    total_profit  = round(df['profit'].sum(), 0)
    avg_margin    = round(df['profit_margin'].mean(), 1)
    best_dept     = df.groupby('department')['profit'].sum().idxmax()
    worst_dept    = df.groupby('department')['profit'].sum().idxmin()

    summary = (
        f"RevenueRadar Financial Analytics report for the period 2022–2024. "
        f"The organization generated total revenue of AED {total_revenue:,.0f} "
        f"against total expenses of AED {total_expense:,.0f}, "
        f"yielding a net profit of AED {total_profit:,.0f}. "
        f"\n\n"
        f"The average profit margin across all departments stands at {avg_margin}%. "
        f"The {best_dept} department delivered the strongest profitability, "
        f"while {worst_dept} recorded the lowest profit contribution and warrants "
        f"immediate management attention. "
        f"\n\n"
        f"Key recommendations: Investigate cost drivers in underperforming departments, "
        f"replicate the revenue strategies of top-performing units, and target "
        f"a profit margin improvement of 5% over the next fiscal year through "
        f"expense optimization and revenue diversification."
    )
    return summary

# ── Build PDF ──────────────────────────────────────────────────────────────────
def generate_pdf_report():
    df = pd.read_csv('exports/financials.csv')
    generate_charts(df)

    path = 'exports/pdf/RevenueRadar_Financial_Report.pdf'
    doc  = SimpleDocTemplate(path, pagesize=A4,
                             rightMargin=40, leftMargin=40,
                             topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    story  = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    title_style = ParagraphStyle('title', fontSize=28, textColor=NAVY,
                                  alignment=TA_CENTER, fontName='Helvetica-Bold',
                                  spaceAfter=8)
    sub_style   = ParagraphStyle('sub', fontSize=13, textColor=GOLD,
                                  alignment=TA_CENTER, spaceAfter=4)
    date_style  = ParagraphStyle('date', fontSize=10, textColor=GRAY,
                                  alignment=TA_CENTER)

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("RevenueRadar", title_style))
    story.append(Paragraph("Financial Analytics Report — 2022 to 2024", sub_style))
    story.append(Paragraph(datetime.now().strftime("%B %Y"), date_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD))
    story.append(Spacer(1, 0.3 * inch))

    # ── KPI Table ──────────────────────────────────────────────────────────────
    section_style = ParagraphStyle('section', fontSize=14, textColor=NAVY,
                                    fontName='Helvetica-Bold', spaceAfter=10,
                                    spaceBefore=16)
    story.append(Paragraph("Key Financial Indicators", section_style))

    total_revenue = round(df['revenue'].sum(), 0)
    total_expense = round(df['expense'].sum(), 0)
    total_profit  = round(df['profit'].sum(), 0)
    avg_margin    = round(df['profit_margin'].mean(), 1)
    best_dept     = df.groupby('department')['profit'].sum().idxmax()
    worst_dept    = df.groupby('department')['profit'].sum().idxmin()

    kpi_data = [
        ['Metric', 'Value'],
        ['Total Revenue (3 Years)', f'AED {total_revenue:,.0f}'],
        ['Total Expense (3 Years)', f'AED {total_expense:,.0f}'],
        ['Net Profit (3 Years)', f'AED {total_profit:,.0f}'],
        ['Avg Profit Margin', f'{avg_margin}%'],
        ['Most Profitable Department', best_dept],
        ['Least Profitable Department', worst_dept],
    ]

    kpi_table = Table(kpi_data, colWidths=[3 * inch, 3 * inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, 0), 11),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE',   (0, 1), (-1, -1), 10),
        ('PADDING',    (0, 0), (-1, -1), 8),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Executive Summary ──────────────────────────────────────────────────────
    story.append(Paragraph("Executive Summary", section_style))
    body_style = ParagraphStyle('body', fontSize=10, leading=16,
                                 textColor=colors.black, spaceAfter=8)
    for para in generate_summary(df).split('\n\n'):
        story.append(Paragraph(para.strip(), body_style))
    story.append(Spacer(1, 0.2 * inch))

    # ── Charts ─────────────────────────────────────────────────────────────────
    story.append(Paragraph("Revenue Analysis", section_style))
    story.append(Image('exports/charts/pdf_revenue.png', width=5.5*inch, height=2.8*inch))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Year over Year Performance", section_style))
    story.append(Image('exports/charts/pdf_yoy.png', width=5.5*inch, height=2.8*inch))
    story.append(Spacer(1, 0.2 * inch))

    # ── Dept Table ─────────────────────────────────────────────────────────────
    story.append(Paragraph("Department Performance Summary", section_style))
    dept_df = df.groupby('department').agg(
        Revenue=('revenue', 'sum'),
        Expense=('expense', 'sum'),
        Profit=('profit', 'sum'),
        Margin=('profit_margin', 'mean')
    ).reset_index().round(2)

    dept_data = [['Department', 'Revenue (AED)', 'Expense (AED)', 'Profit (AED)', 'Margin %']]
    for _, row in dept_df.iterrows():
        dept_data.append([
            row['department'],
            f"{row['Revenue']:,.0f}",
            f"{row['Expense']:,.0f}",
            f"{row['Profit']:,.0f}",
            f"{row['Margin']:.1f}%"
        ])

    dept_table = Table(dept_data, colWidths=[1.8*inch, 1.4*inch, 1.4*inch, 1.4*inch, 1*inch])
    dept_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE',   (0, 0), (-1, -1), 9),
        ('PADDING',    (0, 0), (-1, -1), 7),
    ]))
    story.append(dept_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Footer ─────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    footer_style = ParagraphStyle('footer', fontSize=8, textColor=GRAY,
                                   alignment=TA_CENTER, spaceBefore=6)
    story.append(Paragraph(
        f"Generated by RevenueRadar Financial Analytics Platform — {datetime.now().strftime('%d %B %Y')}",
        footer_style
    ))

    doc.build(story)
    print(f"PDF report saved to {path}")
    return path

if __name__ == "__main__":
    generate_pdf_report()