# database.py connects to week 7 and 8 
import sqlite3
import pandas as pd
from schema import create_all_tables, load_all_csv_data

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("intelligence.db")
        self.cursor = self.conn.cursor()
        create_all_tables(self.conn)  #from week 8
        
    #for Login using week 7 users.txt
    def check_login(self, username, password):
        """Simple login check"""
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if user and user[2] == password:  #user[2]is password
            return True
        return False
    
    #for Cybersecurity Dashboard
    def get_cyber_incidents(self):
        self.cursor.execute("SELECT * FROM cyber_incidents")
        return self.cursor.fetchall()
    
    #for Data Science Dashboard
    def get_datasets(self):
        self.cursor.execute("SELECT * FROM datasets_metadata")
        return self.cursor.fetchall()
    
    #for IT Operations Dashboard
    def get_it_tickets(self):
        self.cursor.execute("SELECT * FROM it_tickets")
        return self.cursor.fetchall()

#Creating database once
db = DatabaseManager()
load_all_csv_data(db.conn)  # Loading CSV files