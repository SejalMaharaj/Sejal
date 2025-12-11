# app/data/db.py
import sqlite3
from pathlib import Path
import pandas as pd
# multi_domain_platform/database/db.py
from pathlib import Path
import sqlite3

# Base folder = multi_domain_platform/
BASE_DIR = Path(__file__).resolve().parent.parent

# Database folder = multi_domain_platform/database/
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

# Database file
DB_PATH = DB_DIR / "intelligence_platform.db"


def connect_database(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """
    Connect to the SQLite database.
    Creates the database file if it does not exist.
    """
    return sqlite3.connect(db_path)

# Database file path
DATA_DIR = Path("DATA")
DATA_DIR.mkdir(exist_ok=True)  # Ensure DATA folder exists
DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.

    Args:
        db_path: Path to the database file

    Returns:
        sqlite3.Connection: Database connection object
    """
    return sqlite3.connect(str(db_path))


def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """
    csv_file = Path(csv_path)
    if not csv_file.is_file():
        print(f" CSV file '{csv_path}' not found!")
        return 0

    # Read CSV
    df = pd.read_csv(csv_file)

    # Load into database
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

    row_count = len(df)
    print(f" Loaded {row_count} rows from '{csv_path}' into table '{table_name}'.")
    return row_count
