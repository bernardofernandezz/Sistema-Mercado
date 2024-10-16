import sqlite3

# Cria e conecta ao banco de dados
conn = sqlite3.connect('mercado.db')
cursor = conn.cursor()

# Criação da tabela de produtos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()
