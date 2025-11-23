# app/data/schema.py

from .users import create_users_table
from .incidents import create_cyber_incidents_table
from .datasets import create_datasets_metadata_table
from .tickets import create_it_tickets_table


def create_all_tables(conn):
    """
    Create all tables in the database.

    This calls each module's table creation function.
    """
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

    print("All tables created successfully!")
