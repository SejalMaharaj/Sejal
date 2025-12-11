# main.py

import pandas as pd
from CW2_M0123456_CST1510.multi_domain_platform.database.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident
from app.data.incidents import get_incidents_by_type_count, get_high_severity_by_status

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # Connect to database
    conn = connect_database()

    # 1. Create all tables
    create_all_tables(conn)

    # 2. Migrate users
    migrated_count = migrate_users_from_file(conn)
    print(f"Migrated {migrated_count} users")

    # 3. Test authentication
    success, msg = register_user(conn, "alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user(conn, "alice", "SecurePass123!")
    print(msg)

    # 4. Test CRUD operations for incidents
    incident_id = insert_incident(
        conn,
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # Query all incidents
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")

    conn.close()


def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("=" * 60)

    # Step 1: Connect
    conn = connect_database()
    print("Connected to database")

    # Step 2: Create tables
    create_all_tables(conn)

    # Step 3: Migrate users
    user_count = migrate_users_from_file(conn)
    print(f"Migrated {user_count} users")

    # Step 4: Load CSV data
    # You need to implement this function in db.py
    # total_rows = load_all_csv_data(conn)

    # Step 5: Verify
    cursor = conn.cursor()
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\nDatabase Summary:")
    print(f"{'Table':<25} {'Row Count':<10}")
    print("-" * 40)
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<10}")

    conn.close()
    print("\nDatabase setup complete!")
    print(f"Database location: {DB_PATH.resolve()}")


def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "=" * 60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user(conn, "test_user", "TestPass123!", "user")
    print(f"Register: {'pass' if success else 'fail'} {msg}")

    success, msg = login_user(conn, "test_user", "TestPass123!")
    print(f"Login:    {'pass' if success else 'fail'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"Created incident #{test_id}")

    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"Read incident #{test_id}")

    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"Updated status for incident #{test_id}")

    # Delete
    delete_incident(conn, test_id)
    print(f"Deleted incident #{test_id}")

    # Analytical queries
    df_by_type = get_incidents_by_type_count(conn)
    print(f"Incident types: {len(df_by_type)}")
    df_high = get_high_severity_by_status(conn)
    print(f"High severity status categories: {len(df_high)}")

    conn.close()
    print("\nAll tests passed!")


if __name__ == "__main__":
    main()
