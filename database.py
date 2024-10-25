import sqlite3
import csv

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS festivities_event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        state_region TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def load_data_from_csv(csv_file):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        events_data = [
            (row['Event'], row['Start Date'], row['End Date'], row['State/Region'])
            for row in csvreader
        ]

    cursor.executemany('''
    INSERT INTO festivities_event (event_name, start_date, end_date, state_region)
    VALUES (?, ?, ?, ?)
    ''', events_data)

    conn.commit()
    conn.close()

def execute_query(query):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        conn.close()