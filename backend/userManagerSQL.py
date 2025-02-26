import sqlite3 as sqlite

def create_table():
    conn = sqlite.connect('userManagerSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            login VARCHAR(250) UNIQUE NOT NULL,
            senha VARCHAR(250) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

def insert(name, login, password):
    conn = sqlite.connect('userManagerSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (nome, login, senha) VALUES (?, ?, ?)
    ''', (name, login, password))
    conn.commit()
    conn.close()
# insert('admin', 'admin', 'admin')
def list():
    conn = sqlite.connect('userManagerSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users order by id desc')
    data = cursor.fetchall()
    users = []
    for i in data:
        users.append(i)
    conn.close()
    return users

def get_user_by_login(login):
    conn = sqlite.connect('userManagerSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
    user = cursor.fetchone()
    conn.close()
    return user

def login(login, password):
    conn = sqlite.connect('userManagerSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE login = ? AND senha = ?', (login, password))
    user = cursor.fetchone()
    conn.close()
    return user