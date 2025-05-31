import sqlite3

conn = sqlite3.connect("exercicios_banco_dados.db")
cursor = conn.cursor()


cursor.execute("DROP TABLE IF EXISTS clientes;")
cursor.execute("""
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE,
    idade INTEGER
);
""")


clientes = [
    ("Ana Silva", "ana@gmail.com", 30),
    ("Bruno Costa", "bruno@gmail.com", 22),
    ("Carlos Souza", "carlos@gmail.com", 28),
    ("Daniela Lima", "daniela@gmail.com", 19),
    ("Eduardo Rocha", "eduardo@gmail.com", 45),
    ("Fernanda Alves", "fernanda@gmail.com", 35),
    ("Gustavo Pereira", "gustavo@gmail.com", 40),
    ("Helena Dias", "helena@gmail.com", 24),
    ("Igor Nunes", "igor@gmail.com", 33),
    ("Juliana Castro", "juliana@gmail.com", 27),
]
cursor.executemany("INSERT INTO clientes (nome, email, idade) VALUES (?, ?, ?);", clientes)


print("\nTodos os clientes:")
cursor.execute("SELECT * FROM clientes;")
for row in cursor.fetchall():
    print(row)


print("\nClientes com idade maior que 25:")
cursor.execute("SELECT * FROM clientes WHERE idade > 25;")
for row in cursor.fetchall():
    print(row)


print("\nClientes ordenados por nome:")
cursor.execute("SELECT * FROM clientes ORDER BY nome ASC;")
for row in cursor.fetchall():
    print(row)


cursor.execute("UPDATE clientes SET email = 'ana_silva_novo@gmail.com' WHERE id = 1;")
print("\nEmail do cliente 1 atualizado.")


cursor.execute("DELETE FROM clientes WHERE id = 4;")
print("\nCliente com ID 4 removido.")


cursor.execute("DROP TABLE IF EXISTS pedidos;")
cursor.execute("""
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    valor REAL NOT NULL,
    data_pedido DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
""")


pedidos = [
    (1, 150.00, "2024-05-01"),
    (2, 90.50, "2024-05-02"),
    (3, 200.00, "2024-05-03"),
    (5, 300.00, "2024-05-04"),
    (6, 75.25, "2024-05-05"),
    (7, 110.00, "2024-05-06"),
    (8, 50.00, "2024-05-07"),
    (9, 180.30, "2024-05-08"),
    (10, 250.00, "2024-05-09"),
    (1, 130.00, "2024-05-10"),
]
cursor.executemany("INSERT INTO pedidos (cliente_id, valor, data_pedido) VALUES (?, ?, ?);", pedidos)

print("\n10 pedidos foram inseridos na tabela 'pedidos'.")


conn.commit()
conn.close()
print("\nTodas as operações da Parte 1 foram executadas com sucesso!")
