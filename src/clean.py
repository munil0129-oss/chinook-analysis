"""
clean.py
=======
Clean the raw Chinook data.
"""
import pandas as pd
import sqlite3

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw Chinook data by performing the following operations:
    - Remove rows with missing values in critical columns.
    - Convert data types to appropriate formats.
    - Standardize column names to lowercase.
    """
    # doesn't blow up on an empty frame.
    if df.empty:
        return df.copy()

    df = df.copy()
    # Remove rows with missing values in critical columns
    critical_columns = ['InvoiceId', 'CustomerId', 'TrackId', 'UnitPrice', 'Quantity']
    df = df.dropna(subset=critical_columns)

    # Convert data types
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['UnitPrice'] = df['UnitPrice'].astype(float)
    df['Quantity'] = df['Quantity'].astype(int)

    # Standardize column names to lowercase
    df.columns = [col.lower() for col in df.columns]

    with sqlite3.connect('data/cleaned/Chinook_cleaned.sqlite') as conn:
        df.to_sql('cleaned_data', conn, index=False, if_exists='replace')

    return df