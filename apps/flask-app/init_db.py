import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'clusters.db')

clusters = [
    {"name": "hub", "environment": "prod", "status": "Healthy"},
    {"name": "spoke-1", "environment": "staging", "status": "Healthy"},
    {"name": "spoke-2", "environment": "dev", "status": "Degraded"},
    {"name": "spoke-3", "environment": "prod", "status": "Unreachable"}
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Clusters table
    c.execute('DROP TABLE IF EXISTS clusters')
    c.execute('''
        CREATE TABLE clusters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            environment TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    for cluster in clusters:
        c.execute('INSERT INTO clusters (name, environment, status) VALUES (?, ?, ?)',
                  (cluster['name'], cluster['environment'], cluster['status']))
    # Users table
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    # Demo users: admin/adminpass, viewer/viewerpass
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', ('admin', 'adminpass', 'admin'))
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', ('viewer', 'viewerpass', 'viewer'))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database initialized at', DB_PATH)
