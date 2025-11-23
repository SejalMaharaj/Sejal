# app/data/datasets.py

import pandas as pd
from app.data.db import connect_database

def create_datasets_metadata_table(conn):
    """Create datasets_metadata table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            category TEXT,
            source TEXT,
            last_updated TEXT,
            record_count INTEGER,
            file_size_mb REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("datasets_metadata table created successfully.")

def insert_dataset(conn, dataset_name, category=None, source=None, last_updated=None, record_count=None, file_size_mb=None):
    """Insert a new dataset record."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    return cursor.lastrowid

def get_all_datasets(conn):
    """Retrieve all datasets as a DataFrame."""
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    return df

def update_dataset(conn, dataset_id, **kwargs):
    """Update dataset fields. kwargs can include: dataset_name, category, source, last_updated, record_count, file_size_mb."""
    cursor = conn.cursor()
    fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values())
    values.append(dataset_id)
    cursor.execute(f"UPDATE datasets_metadata SET {fields} WHERE id = ?", values)
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    """Delete a dataset by ID."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    return cursor.rowcount
