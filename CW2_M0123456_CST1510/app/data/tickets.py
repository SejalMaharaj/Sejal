# app/data/tickets.py

import pandas as pd
from app.data.db import connect_database


def create_it_tickets_table(conn):
    """Create it_tickets table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            priority TEXT,
            status TEXT,
            category TEXT,
            subject TEXT NOT NULL,
            description TEXT,
            created_date TEXT,
            resolved_date TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("it_tickets table created successfully.")

def insert_ticket(conn, ticket_id, subject, priority=None, status=None, category=None, description=None, created_date=None, resolved_date=None, assigned_to=None):
    """Insert a new IT ticket."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))
    conn.commit()
    return cursor.lastrowid

def get_all_tickets(conn):
    """Retrieve all tickets as a DataFrame."""
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    return df

def update_ticket(conn, ticket_id, **kwargs):
    """Update ticket fields. kwargs can include: priority, status, category, subject, description, created_date, resolved_date, assigned_to."""
    cursor = conn.cursor()
    fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values())
    values.append(ticket_id)
    cursor.execute(f"UPDATE it_tickets SET {fields} WHERE ticket_id = ?", values)
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """Delete a ticket by ticket_id."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount
