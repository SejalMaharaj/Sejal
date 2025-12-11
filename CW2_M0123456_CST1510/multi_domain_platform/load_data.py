# load_data.py
from database.db import connect_database


from db import connect_database, load_csv_to_table
from pathlib import Path

# DATA folder is outside the 'my_app' folder
DATA_DIR = Path("../DATA")

# Mapping CSV filenames → database table names
CSV_FILES = {
    "cyber_incidents.csv": "cyber_incidents",
    "datasets_metadata.csv": "datasets",   # updated to match your actual file
    "it_tickets.csv": "it_tickets"
}

# ---------------- CONNECT TO DATABASE ----------------
conn = connect_database()

# ---------------- LOAD CSV FILES ----------------
for csv_file, table_name in CSV_FILES.items():
    csv_path = DATA_DIR / csv_file
    rows_loaded = load_csv_to_table(conn, csv_path, table_name)
    print(f"{rows_loaded} rows loaded into '{table_name}' table.")

# ---------------- CLOSE CONNECTION ----------------
conn.close()
print("All CSV files have been loaded into the database successfully!")

