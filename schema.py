# part 3
import pandas as pd

def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()

def create_cyber_incidents_table(conn):
    """Create cyber_incidents table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'open'
            
        )
    """)
    conn.commit()

def create_datasets_metadata_table(conn):
    """Create datasets_metadata table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            source TEXT,
            size INTEGER
        )
    """)
    conn.commit()

def create_it_tickets_table(conn):
    """Create it_tickets table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT  NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_date TEXT
        )
    """)
    conn.commit()

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)


# part 6


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
    try:
        # Read CSV using pandas
        df = pd.read_csv(csv_path)
        
        # Insert data into database
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',  # Adding to existing data
            index=False          # Not saving DataFrame index
        )
        
        print(f"Loaded {len(df)} rows into {table_name}")
        return len(df)
        
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
        return 0
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return 0

def load_all_csv_data(conn):
    """
    Load all CSV files into their respective tables.
    """
    from pathlib import Path
    
    DATA_DIR = Path("DATA")
    total_rows = 0
    
    # Maping CSV files to their tables
    csv_table_mapping = {
        "cyber_incidents.csv": "cyber_incidents",
        "datasets_metadata.csv": "datasets_metadata", 
        "it_tickets.csv": "it_tickets"
    }
    
    for csv_file, table_name in csv_table_mapping.items():
        csv_path = DATA_DIR / csv_file
        if csv_path.exists():
            rows = load_csv_to_table(conn, csv_path, table_name)
            total_rows += rows
        else:
            print(f" File not found: {csv_file}")
    
    return total_rows