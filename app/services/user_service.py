import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

# part 5
def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

# part 5
def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."

# part 4
def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    # Create users table first
    conn = connect_database()
    create_users_table(conn)
    
    # Check if file exists
    file_path = Path(filepath)
    if not file_path.exists():
        print(f" File not found: {filepath}")
        print("   No users to migrate.")
        conn.close()
        return
    
    cursor = conn.cursor()
    migrated_count = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Skip header if exists
            if line.startswith('username'):
                continue
            
            # Parse line: username,password_hash,role
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) > 2 else 'user'
                
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except Exception as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Migrated {migrated_count} users from {file_path.name}")