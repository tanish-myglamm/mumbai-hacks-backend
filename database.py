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
        state_region TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def load_data_from_csv(csv_file):
    import json  # Import json module to handle JSON serialization

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        events_data = []
        for row in csvreader:
            event_name = row['event_name']
            start_date = row['start_date']
            description = row['description']
            states = row['state'].split(', ')
            # Convert the list of states to a JSON string
            state_json = json.dumps(states)
            events_data.append((event_name, start_date, state_json, description))

    cursor.executemany('''
    INSERT INTO festivities_event (event_name, start_date, state_region, description)
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