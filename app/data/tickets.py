import pandas as pd
from app.data.db import connect_database

def insert_ticket(ticket_id, priority, category, subject, description, created_date, assigned_to=None):
    """Insert new IT ticket."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets 
        (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
        VALUES (?, ?, 'Open', ?, ?, ?, ?, ?)
    """, (ticket_id, priority, category, subject, description, created_date, assigned_to))
    conn.commit()
    ticket_db_id = cursor.lastrowid
    conn.close()
    return ticket_db_id

def get_all_tickets():
    """Get all tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY created_date DESC",
        conn
    )
    conn.close()
    return df

def get_ticket_by_id(ticket_id):
    """Get ticket by ticket ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    ticket = cursor.fetchone()
    conn.close()
    return ticket

def update_ticket_status(ticket_id, new_status, resolved_date=None):
    """Update ticket status."""
    conn = connect_database()
    cursor = conn.cursor()
    
    if resolved_date:
        cursor.execute(
            "UPDATE it_tickets SET status = ?, resolved_date = ? WHERE ticket_id = ?",
            (new_status, resolved_date, ticket_id)
        )
    else:
        cursor.execute(
            "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
            (new_status, ticket_id)
        )
    
    conn.commit()
    updated_count = cursor.rowcount
    conn.close()
    return updated_count

def delete_ticket(ticket_id):
    """Delete ticket by ticket ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    return deleted_count

def get_tickets_by_priority(priority):
    """Get tickets by priority."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE priority = ?",
        (priority,)
    )
    tickets = cursor.fetchall()
    conn.close()
    return tickets