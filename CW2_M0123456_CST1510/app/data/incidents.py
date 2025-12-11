# app/data/incidents.py


import pandas as pd

def create_cyber_incidents_table(conn):
    """Create the cyber_incidents table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("cyber_incidents table created successfully.")


def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.

    Args:
        conn: Database connection
        date: Incident date (YYYY-MM-DD)
        incident_type: Type of incident
        severity: Severity level
        status: Current status
        description: Incident description
        reported_by: Username of reporter (optional)

    Returns:
        int: ID of the inserted incident
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (date, incident_type, severity, status, description, reported_by)
    )
    conn.commit()
    return cursor.lastrowid


def get_all_incidents(conn):
    """
    Retrieve all incidents from the database.

    Args:
        conn: Database connection

    Returns:
        pandas.DataFrame: All incidents ordered by id descending
    """
    return pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )


def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    return cursor.rowcount


def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    """
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
    return cursor.rowcount


def get_incidents_by_type_count(conn):
    """Count incidents by type."""
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_high_severity_by_status(conn):
    """Count high severity incidents by status."""
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_incident_types_with_many_cases(conn, min_count=5):
    """Find incident types with more than min_count cases."""
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn, params=(min_count,))
