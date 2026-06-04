import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = OFF;")

cursor.execute("UPDATE clientes_produto SET fornecedor = NULL;")

cursor.execute("UPDATE clientes_compra SET fornecedor = NULL;")

conn.commit()
conn.close()

print("Fornecedor antigo removido.")