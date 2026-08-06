"""
load,py
=======
Load the Chinook database from a sqlite.
"""

import sqlite3
import pandas as pd

def load_raw(db_path:str) -> pd.DataFrame:
    """
    Load the raw from Chinook SQLite database.
    """
    query = """
            SELECT
                il.InvoiceLineId,
                i.InvoiceId,
                i.InvoiceDate,
                i.BillingCountry,
                c.CustomerId,
                c.FirstName || ' ' || c.LastName AS CustomerName,
                c.Country AS CustomerCountry,
                t.TrackId,
                t.Name AS TrackName,
                g.Name AS Genre,
                il.UnitPrice,
                il.Quantity,
                (il.UnitPrice * il.Quantity) AS LineTotal
            FROM InvoiceLine il
            JOIN Invoice i  ON il.InvoiceId = i.InvoiceId
            JOIN Customer c ON i.CustomerId = c.CustomerId
            JOIN Track t    ON il.TrackId = t.TrackId
            LEFT JOIN Genre g ON t.GenreId = g.GenreId
        """
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn)
    return df

def load_table(db_path:str,table_name:str) -> pd.DataFrame:
    """
    Load a single Chinook table verbatim, no joins.
    """
    query = f"SELECT * FROM {table_name}"
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query,conn)
    return df