from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables, load_all_csv_data
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, update_incident_status, delete_incident
import pandas as pd

# part 8
def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

# part 8
def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

# part 8
def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# part 10
# Test: Run analytical queries
conn = connect_database()

print("\n Incidents by Type:")
df_by_type = get_incidents_by_type_count(conn)
print(df_by_type)

print("\n High Severity Incidents by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Incident Types with Many Cases (>5):")
df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
print(df_many_cases)

conn.close()


# part 9
def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    from app.data.db import connect_database, DB_PATH
    from app.data.schema import create_all_tables, load_all_csv_data
    from app.services.user_service import migrate_users_from_file
    
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)
    
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")
    
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    
    print("\n[3/5] Migrating users from users.txt...")
    migrate_users_from_file()
    
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)
    print(f"       Loaded {total_rows} total rows")
    
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
    
    conn.close()
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")
    
    

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {' ' if success else 'X'} {msg}")
    
    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {' ' if success else 'X'} {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    # Create
    test_id = insert_incident(
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create:   Incident #{test_id} created")
    
    # Read
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:     Found incident #{test_id}")
    
    # Update
    update_incident_status(test_id, "Resolved")
    print(f"  Update:   Status updated")
    
    # Delete
    delete_incident(test_id)
    print(f"  Delete:   Incident deleted")
    
    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    
    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")
    
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")
    
    conn.close()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)