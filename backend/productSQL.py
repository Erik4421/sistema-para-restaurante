import sqlite3 as sqlite

def create_table():
    conn = sqlite.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT NOT NULL,
            preco DECIMAL(5,2) NOT NULL,
            categoriaId INTEGER NOT NULL,
            FOREIGN KEY (categoriaId) REFERENCES category(id) ON DELETE CASCADE
        );
    ''')
    conn.commit()
    conn.close()

create_table()

def insert(name, description, price, category):
    conn = sqlite.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (nome, descricao, preco, categoriaId) VALUES (?, ?, ?, ?)
    ''', (name, description, price, category))
    conn.commit()
    conn.close()

def insert_category(name):
    conn = sqlite.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO category (nome) VALUES (?)
    ''', (name,))
    conn.commit()
    conn.close()
# insert_category('Bebidas')
# insert_category('Entradas')
# insert_category('Pratos Principais')
# insert_category('Sobremesas')

def list():
    conn = sqlite.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT products.*, category.nome FROM products, category WHERE products.categoriaId = category.id ORDER BY products.id DESC;')
    data = cursor.fetchall()
    products = []
    for i in data:
        products.append(i)
    conn.close()
    return products

def list_category():
    conn = sqlite.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM category order by id ASC')
    data = cursor.fetchall()
    category = []
    for i in data:
        category.append(i)
    conn.close()
    return category

def delete(id):
    conn = sqlite.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
def alter(name, description, price, id):
    conn = sqlite.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET nome = ?, descricao = ?, preco = ? WHERE id = ?', 
                   (name, description, price, id))
    conn.commit()
    conn.close()

