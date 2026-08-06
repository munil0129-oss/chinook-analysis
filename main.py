"""
main.py
=======
end-to-end entrypoint: load -> clean -> analyze -> visualize -> save.
"""

import pandas as pd
import sqlite3
from src.clean import clean_data
from src.analyze import (analyze_customer_tiers, analyze_monthly_growth, analyze_purchase_cadence, analyze_revenue_pareto)
from src.visualize import (visualize_customer_tiers, visualize_monthly_growth, visualize_purchase_cadence, visualize_revenue_pareto)
from src.load import (load_raw, load_table)


def main () -> None:
    # Load the raw data
    raw_df = load_raw("data/raw/Chinook_Sqlite.sqlite")

    # Clean the data
    clean_df = clean_data(raw_df)

    # connect to the database
    conn = sqlite3.connect('data/raw/Chinook_Sqlite.sqlite')

    # Analyze (sql-based) the data + visualize the results
    # Q1: Aggregation & Mapping -> Customer Spend Tiers
    customer_tiers = analyze_customer_tiers(conn)
    fig1 = visualize_customer_tiers(customer_tiers)
    fig1.savefig("outputs/q1_customer_tiers.png")

    # Q2: Time-Based Trend -> Month-over-Month Growth
    monthly_growth = analyze_monthly_growth(conn)
    fig2 = visualize_monthly_growth(monthly_growth)
    fig2.savefig("outputs/q2_monthly_growth.png")

    # Q3: Date Distribution -> Purchase Cadence
    purchase_cadence = analyze_purchase_cadence(conn)
    fig3 = visualize_purchase_cadence(purchase_cadence)
    fig3.savefig("outputs/q3_purchase_cadence.png")

    # Q4: Advanced Comparison -> Revenue Pareto Curve
    revenue_pareto = analyze_revenue_pareto(conn)
    fig4 = visualize_revenue_pareto(revenue_pareto)
    fig4.savefig("outputs/q4_revenue_pareto.png")

if __name__ == "__main__":
    main()