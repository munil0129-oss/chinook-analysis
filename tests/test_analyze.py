"""
test_analysis.py
===============
Unit tests for the analysis module.
"""

from src.analyze import (analyze_customer_tiers, analyze_monthly_growth, analyze_purchase_cadence, analyze_revenue_pareto)
import sqlite3
import pandas as pd

def test_analyze_customer_tiers():
    with sqlite3.connect("data/raw/Chinook_Sqlite.sqlite") as conn:
        df = analyze_customer_tiers(conn)
    assert isinstance(df, pd.DataFrame)
    assert "CustomerTier" in df.columns
    assert "CustomerCount" in df.columns
    assert "tier_revenue" in df.columns
    assert "avg_revenue_per_customer" in df.columns
    assert "PctOfCustomers" in df.columns
    assert "PctOfRevenue" in df.columns

def test_analyze_monthly_growth():
    with sqlite3.connect("data/raw/Chinook_Sqlite.sqlite") as conn:
        df = analyze_monthly_growth(conn)
    assert isinstance(df, pd.DataFrame)
    assert "Month" in df.columns
    assert "MonthlyRevenue" in df.columns
    assert "MonthlyGrowthPct" in df.columns

def test_analyze_purchase_cadence():
    with sqlite3.connect("data/raw/Chinook_Sqlite.sqlite") as conn:
        df = analyze_purchase_cadence(conn)
    assert isinstance(df, pd.DataFrame)
    assert "PurchaseCadence" in df.columns
    assert "CustomerCount" in df.columns
    assert "AvgDaysBetween" in df.columns
    assert not df.empty
    assert df["CustomerCount"].sum() > 0
    assert df["AvgDaysBetween"].mean() > 0
    assert df["AvgDaysBetween"].min() >= 0
    assert df["AvgDaysBetween"].max() <= 365
    assert df["AvgDaysBetween"].std() >= 0

def test_analyze_revenue_pareto():
    with sqlite3.connect("data/raw/Chinook_Sqlite.sqlite") as conn:
        df = analyze_revenue_pareto(conn)
    assert isinstance(df, pd.DataFrame)
    assert "CustomerRank" in df.columns
    assert "CustomerName" in df.columns
    assert "TotalRevenue" in df.columns
    assert "CumulativeRevenue" in df.columns
    assert "CumulativeRevenuePct" in df.columns
    assert "CumulativePctCustomers" in df.columns
    assert not df.empty
    assert "TotalRevenue" in df.columns
    assert "CumulativeRevenue" in df.columns
    assert "CumulativeRevenuePct" in df.columns
