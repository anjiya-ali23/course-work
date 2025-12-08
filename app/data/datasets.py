import pandas as pd
from app.data.db import connect_database

def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Insert new dataset metadata."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

def get_all_datasets():
    """Get all datasets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def get_datasets_by_category(category):
    """Get datasets by category."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM datasets_metadata WHERE category = ?",
        (category,)
    )
    datasets = cursor.fetchall()
    conn.close()
    return datasets

def update_dataset_record_count(dataset_id, new_record_count):
    """Update dataset record count."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE datasets_metadata SET record_count = ?, last_updated = DATE('now') WHERE id = ?",
        (new_record_count, dataset_id)
    )
    conn.commit()
    updated_count = cursor.rowcount
    conn.close()
    return updated_count

def delete_dataset(dataset_id):
    """Delete dataset by ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    return deleted_count