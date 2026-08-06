"""
analyze.py
==========
Analyze the cleaned Chinook data.
"""
import sqlite3
import pandas as pd

def analyze_customer_tiers(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q1 - Aggregation and Mapping: customer spend tiers.
    
    """
    query = """
        SELECT 
            CASE
                WHEN TotalRevenue >= 45 THEN 'VIP ($45+)'
                WHEN TotalRevenue >= 40 THEN 'High ($40-45)'
                WHEN TotalRevenue >= 38 THEN 'Mid ($38-40)'
                ELSE 'Standard (<$38)'
            END AS CustomerTier,
            COUNT(*) AS CustomerCount,
            ROUND(SUM(TotalRevenue), 2) AS tier_revenue,
            ROUND(AVG(TotalRevenue), 2) AS avg_revenue_per_customer
        FROM (
            SELECT
                c.CustomerId,
                SUM(i.Total) AS TotalRevenue
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            GROUP BY c.CustomerId
        ) AS customer_totals
        GROUP BY CustomerTier
        ORDER BY avg_revenue_per_customer DESC
    """
    df = pd.read_sql_query(query, conn)
    total_customers = df["CustomerCount"].sum()
    total_revenue = df["tier_revenue"].sum()
    df["PctOfCustomers"] = (df["CustomerCount"] / total_customers *
    100).round(1)
    df["PctOfRevenue"] = (df["tier_revenue"] / total_revenue * 100).round(1)
    return df

def analyze_monthly_growth(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q2 - Time Series Analysis: monthly revenue growth.

    """
    query = """
        SELECT
            strftime('%Y-%m-01', InvoiceDate) AS Month,
            ROUND(SUM(Total), 2) AS MonthlyRevenue
        FROM Invoice
        GROUP BY Month
        ORDER BY Month
    """
    df = pd.read_sql_query(query, conn)
    df["MonthlyGrowthPct"] = df["MonthlyRevenue"].pct_change().fillna(0) * 100
    df["MonthlyGrowthPct"] = df["MonthlyGrowthPct"].round(1)
    return df

def analyze_purchase_cadence(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q3 - Distribution Analysis: purchase cadence.

    """
    query = """
            WITH invoice_gaps AS (
                SELECT
                    CustomerId,
                    InvoiceDate,
                    LAG(InvoiceDate) OVER(
                        PARTITION BY CustomerId
                        ORDER BY InvoiceDate
                    ) AS PrevInvoiceDate
                FROM Invoice
            ),
            customer_cadence AS (
                SELECT
                    CustomerId,
                    AVG(JULIANDAY(InvoiceDate) - JULIANDAY(PrevInvoiceDate))
                        AS AvgDaysBetweenPurchases
                FROM invoice_gaps
                WHERE PrevInvoiceDate IS NOT NULL
                GROUP BY CustomerId
            )
            SELECT
                CASE
                    WHEN AvgDaysBetweenPurchases < 220 THEN 'Frequent (<220 days)'
                    WHEN AvgDaysBetweenPurchases < 250 THEN 'Regular (220-250 days)'
                    WHEN AvgDaysBetweenPurchases < 280 THEN 'Occasional (250-280 days)'
                    ELSE 'Infrequent (280+ days)'
                END AS PurchaseCadence,
                COUNT(*) AS CustomerCount,
                ROUND(AVG(AvgDaysBetweenPurchases), 1) AS AvgDaysBetween
            FROM customer_cadence
            GROUP BY PurchaseCadence
            ORDER BY MIN(AvgDaysBetweenPurchases)
        """
    return pd.read_sql_query(query, conn)

def analyze_revenue_pareto(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q4 - Pareto Analysis: cumulative revenue contribution by customers.

    """
    query = """
            WITH customer_revenue AS (
                SELECT
                    c.CustomerId,
                    c.FirstName || ' ' || c.LastName AS CustomerName,
                    SUM(i.Total) AS TotalRevenue
                FROM Customer c
                JOIN Invoice i ON c.CustomerId = i.CustomerId
                GROUP BY c.CustomerId
            ),
            ranked AS (
                SELECT
                    CustomerName,
                    TotalRevenue,
                    ROW_NUMBER() OVER (ORDER BY TotalRevenue DESC) AS CustomerRank,
                    SUM(TotalRevenue) OVER (
                        ORDER BY TotalRevenue DESC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) AS CumulativeRevenue,
                    SUM(TotalRevenue) OVER () AS GrandTotalRevenue
                FROM customer_revenue
            )
            SELECT
                CustomerRank,
                CustomerName,
                TotalRevenue,
                ROUND(CumulativeRevenue, 2) AS CumulativeRevenue,
                ROUND(CumulativeRevenue * 100.0 / GrandTotalRevenue, 1) AS CumulativeRevenuePct,
                ROUND(CustomerRank * 100.0 / (SELECT COUNT(*) FROM ranked), 1) AS CumulativePctCustomers
            FROM ranked
            ORDER BY CustomerRank
        """
    return pd.read_sql_query(query, conn)