import sqlite3
from datetime import datetime, timedelta

def criar_banco():
    conn = sqlite3.connect("pedidos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            detalhes TEXT,
            status TEXT,
            hora_pronto TEXT
        )
    """)
    conn.commit()
    conn.close()

def adicionar_pedido(cliente, detalhes):
    conn = sqlite3.connect("pedidos.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pedidos (cliente, detalhes, status) VALUES (?, ?, ?)",
        (cliente, detalhes, "em preparo")
    )
    conn.commit()
    conn.close()

def marcar_pronto(pedido_id):
    conn = sqlite3.connect("pedidos.db")
    cursor = conn.cursor()
    hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "UPDATE pedidos SET status = ?, hora_pronto = ? WHERE id = ?",
        ("pronto", hora_atual, pedido_id)
    )
    conn.commit()
    conn.close()

def listar_pedidos_prontos():
    conn = sqlite3.connect("pedidos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE status = 'pronto'")
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def remover_pedido(pedido_id):
    conn = sqlite3.connect("pedidos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()