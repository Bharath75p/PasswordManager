import sqlite3

def create_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_password(website, username, password):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO passwords (website, username, password) 
    VALUES (?, ?, ?)''', (website, username, password))
    conn.commit()
    conn.close()

def get_passwords():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT website, username, password FROM passwords")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def delete_password(website, username, password):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE website = ? AND username = ? AND password = ?", (website, username, password))
    conn.commit()
    
    conn.close()

def search_password(website):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT website, username, password FROM passwords WHERE website LIKE ?", ('%' + website + '%',))
    rows = cursor.fetchall()
    
    conn.close()
    return rows