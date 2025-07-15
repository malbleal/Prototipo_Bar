import tkinter as tk
from tkinter import ttk, font
import sqlite3
from datetime import datetime, timedelta
import threading
import time
from playsound import playsound  # Instale com: pip install playsound

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Agora o import deve funcionar
from backend.database import *

criar_banco()

class DisplayCliente(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("DISPLAY CLIENTE - Bar do Omar")
        self.attributes('-fullscreen', True)  # Tela cheia
        
        # Configuração do display
        self.label_titulo = tk.Label(
            self, text="PEDIDOS PRONTOS", 
            font=('Arial', 40, 'bold'), fg='white', bg='black'
        )
        self.label_titulo.pack(fill='x', pady=20)
        
        self.lista_prontos = tk.Listbox(
            self, font=('Arial', 24), 
            bg='black', fg='yellow', height=15
        )
        self.lista_prontos.pack(fill='both', expand=True, padx=50, pady=20)
        
        self.atualizar_display()
    
    def atualizar_display(self):
        pedidos_prontos = listar_pedidos_prontos()
        self.lista_prontos.delete(0, tk.END)
        
        agora = datetime.now()
        for pedido in pedidos_prontos:
            hora_pronto = datetime.strptime(pedido[4], "%Y-%m-%d %H:%M:%S")
            if agora - hora_pronto < timedelta(minutes=3):  # Mostra por 3 minutos
                texto = f"Pedido {pedido[0]} - {pedido[1]} ({pedido[2]})"
                self.lista_prontos.insert(tk.END, texto)
            else:
                remover_pedido(pedido[0])  # Remove automaticamente
        
        self.after(30000, self.atualizar_display)  # Atualiza a cada 30 segundos

class AppFuncionario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CONTROLE FUNCIONÁRIO - Bar do Omar")
        
        # Frame para novos pedidos
        frame_novo = ttk.LabelFrame(self, text="Novo Pedido")
        frame_novo.pack(padx=10, pady=10, fill='x')
        
        tk.Label(frame_novo, text="Cliente:").grid(row=0, column=0)
        self.entry_cliente = tk.Entry(frame_novo, width=30)
        self.entry_cliente.grid(row=0, column=1)
        
        tk.Label(frame_novo, text="Detalhes:").grid(row=1, column=0)
        self.entry_detalhes = tk.Entry(frame_novo, width=50)
        self.entry_detalhes.grid(row=1, column=1)
        
        btn_adicionar = tk.Button(
            frame_novo, text="Adicionar Pedido", 
            command=self.adicionar_pedido, bg='green', fg='white'
        )
        btn_adicionar.grid(row=2, columnspan=2, pady=5)
        
        # Frame para pedidos em preparo
        frame_pedidos = ttk.LabelFrame(self, text="Pedidos em Preparo")
        frame_pedidos.pack(padx=10, pady=10, fill='both', expand=True)
        
        colunas = ("id", "cliente", "detalhes")
        self.tree = ttk.Treeview(frame_pedidos, columns=colunas, show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("detalhes", text="Detalhes")
        self.tree.pack(fill='both', expand=True)
        
        btn_pronto = tk.Button(
            frame_pedidos, text="Marcar como Pronto", 
            command=self.marcar_pronto, bg='blue', fg='white'
        )
        btn_pronto.pack(pady=5)
        
        self.carregar_pedidos()
    
    def adicionar_pedido(self):
        cliente = self.entry_cliente.get()
        detalhes = self.entry_detalhes.get()
        if cliente and detalhes:
            adicionar_pedido(cliente, detalhes)
            self.entry_cliente.delete(0, tk.END)
            self.entry_detalhes.delete(0, tk.END)
            self.carregar_pedidos()
    
    def carregar_pedidos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect("pedidos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, detalhes FROM pedidos WHERE status = 'em preparo'")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()
    
    def marcar_pronto(self):
        item_selecionado = self.tree.focus()
        if item_selecionado:
            pedido_id = self.tree.item(item_selecionado)['values'][0]
            marcar_pronto(pedido_id)
            self.carregar_pedidos()

if __name__ == "__main__":
    criar_banco()
    app_funcionario = AppFuncionario()
    display_cliente = DisplayCliente(app_funcionario)
    app_funcionario.mainloop()