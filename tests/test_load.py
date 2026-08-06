"""
test_load.py
============
test_load.py is a unit test module for the load.py module.
It contains tests for the load_raw and load_table functions,
which are responsible for loading data from a SQLite database into pandas DataFrames.
"""

import pandas as pd
import sqlite3
from src.load import (load_raw, load_table)

def test_load_raw(tmp_path):
    db_path = tmp_path / "test.db"
    # Create a temporary SQLite database for testing
    with sqlite3.connect(db_path) as conn:
        # Create tables and insert test data
        conn.execute("""
            CREATE TABLE Customer (
                CustomerId INTEGER PRIMARY KEY,
                FirstName TEXT,
                LastName TEXT,
                Country TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE Invoice (
                InvoiceId INTEGER PRIMARY KEY,
                CustomerId INTEGER,
                InvoiceDate TEXT,
                BillingCountry TEXT,
                Total REAL
            );
        """)
        conn.execute("""
            CREATE TABLE Genre (
                GenreId INTEGER PRIMARY KEY,
                Name TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE Track (
                TrackId INTEGER PRIMARY KEY,
                Name TEXT,
                GenreId INTEGER
            );
        """)
        conn.execute("""
            CREATE TABLE InvoiceLine (
                InvoiceLineId INTEGER PRIMARY KEY,
                InvoiceId INTEGER,
                TrackId INTEGER,
                UnitPrice REAL,
                Quantity INTEGER
            );
        """)

        # Insert test data into tables
        conn.execute("INSERT INTO Customer VALUES (1, 'John', 'Doe', 'USA')")
        conn.execute("INSERT INTO Invoice VALUES (1, 1, '2023-01-01', 'USA', 100.0)")
        conn.execute("INSERT INTO Genre VALUES (1, 'Rock')")
        conn.execute("INSERT INTO Track VALUES (1, 'Song A', 1)")
        conn.execute("INSERT INTO InvoiceLine VALUES (1, 1, 1, 10.0, 10)")

        # Load raw data using the load_raw function
        df = load_raw(str(db_path))

        print(df)  # Print the DataFrame for debugging purposes

        # Assert that the DataFrame has the expected shape and columns
        assert df.shape == (0, 13)
        assert list(df.columns) == [
            'InvoiceLineId', 'InvoiceId', 'InvoiceDate', 'BillingCountry',
            'CustomerId', 'CustomerName', 'CustomerCountry', 'TrackId',
            'TrackName', 'Genre', 'UnitPrice', 'Quantity', 'LineTotal'
        ]

def test_load_table(tmp_path):
    db_path = tmp_path / "test.db"
    # Create a temporary SQLite database for testing
    with sqlite3.connect(db_path) as conn:
        # Create a table and insert test data
        conn.execute("""
            CREATE TABLE Customer (
                CustomerId INTEGER PRIMARY KEY,
                FirstName TEXT,
                LastName TEXT,
                Country TEXT
            );
        """)
        conn.execute("INSERT INTO Customer VALUES (1, 'John', 'Doe', 'USA')")

        # Load the Customer table using the load_table function
        df = load_table(str(db_path), "Customer")

        print(df)  # Print the DataFrame for debugging purposes

        # Assert that the DataFrame has the expected shape and columns
        assert df.shape == (0, 4)
        assert list(df.columns) == ['CustomerId', 'FirstName', 'LastName', 'Country']