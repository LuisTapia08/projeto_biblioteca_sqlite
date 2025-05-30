import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import csv

def exportar_relatorio_pdf():
    caminho_csv = "relatorio_vendas.csv"
    caminho_pdf = "relatorio_vendas.pdf"

    try:
        with open(caminho_csv, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            dados = list(reader)

        c = canvas.Canvas(caminho_pdf, pagesize=A4)
        largura, altura = A4
        y = altura - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Relatório de Vendas")
        y -= 30

        c.setFont("Helvetica", 10)
        for linha in dados:
            texto = " | ".join(linha)
            c.drawString(50, y, texto)
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = altura - 50

        c.save()
        messagebox.showinfo("PDF Criado", "Relatório exportado como relatorio_vendas.pdf")
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo relatorio_vendas.csv não foi encontrado.")


def conectar():
    basedir = os.path.dirname(os.path.abspath(__file__))
    caminho_db = os.path.join(basedir, "vendas.db")
    return sqlite3.connect(caminho_db)

def criar_tabelas():
    with conectar() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER
            );
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT
            );
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                data TEXT,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id)
            );
            CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venda INTEGER,
                id_produto INTEGER,
                quantidade INTEGER,
                FOREIGN KEY (id_venda) REFERENCES vendas(id),
                FOREIGN KEY (id_produto) REFERENCES produtos(id)
            );
        """)

# Adicionar produto
def salvar_produto():
    nome = entrada_nome_produto.get()
    preco = entrada_preco.get()
    estoque = entrada_estoque.get()
    if nome and preco and estoque:
        try:
            with conectar() as con:
                con.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
                            (nome, float(preco), int(estoque)))
            messagebox.showinfo("Sucesso", "Produto adicionado!")
            entrada_nome_produto.delete(0, tk.END)
            entrada_preco.delete(0, tk.END)
            entrada_estoque.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar produto: {e}")
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")

# Listar produtos
def mostrar_produtos():
    for row in tabela.get_children():
        tabela.delete(row)
    with conectar() as con:
        rows = con.execute("SELECT * FROM produtos").fetchall()
        for row in rows:
            tabela.insert("", tk.END, values=row)

# Adicionar cliente
def salvar_cliente():
    nome = entrada_nome_cliente.get()
    email = entrada_email.get()
    if nome and email:
        with conectar() as con:
            con.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
        messagebox.showinfo("Sucesso", "Cliente adicionado!")
        entrada_nome_cliente.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")

# Mostrar clientes cadastrados
def mostrar_clientes():
    for row in tabela_clientes.get_children():
        tabela_clientes.delete(row)
    with conectar() as con:
        rows = con.execute("SELECT * FROM clientes").fetchall()
        for row in rows:
            tabela_clientes.insert("", tk.END, values=row)

# Mostrar vendas registradas
def mostrar_vendas():
    janela_vendas = tk.Toplevel()
    janela_vendas.title("Vendas Registradas")
    janela_vendas.geometry("800x400")

    colunas = ("ID Venda", "Cliente", "Data", "Produto", "Quantidade", "Total")
    tabela_vendas = ttk.Treeview(janela_vendas, columns=colunas, show="headings")
    for col in colunas:
        tabela_vendas.heading(col, text=col)
    tabela_vendas.pack(fill="both", expand=True)

    with conectar() as con:
        vendas = con.execute("""
            SELECT v.id, c.nome, v.data, p.nome, iv.quantidade, (iv.quantidade * p.preco)
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id
            JOIN itens_venda iv ON iv.id_venda = v.id
            JOIN produtos p ON p.id = iv.id_produto
        """).fetchall()
        for venda in vendas:
            tabela_vendas.insert("", tk.END, values=venda)

# Interface de Vendas
def interface_vendas():
    janela_venda = tk.Toplevel()
    janela_venda.title("Registrar Venda")

    tk.Label(janela_venda, text="ID do Cliente:").grid(row=0, column=0)
    entrada_cliente = tk.Entry(janela_venda)
    entrada_cliente.grid(row=0, column=1)

    tk.Label(janela_venda, text="ID do Produto:").grid(row=1, column=0)
    entrada_produto = tk.Entry(janela_venda)
    entrada_produto.grid(row=1, column=1)

    tk.Label(janela_venda, text="Quantidade:").grid(row=2, column=0)
    entrada_qtd = tk.Entry(janela_venda)
    entrada_qtd.grid(row=2, column=1)

    def registrar_venda():
        id_cliente = entrada_cliente.get()
        id_produto = entrada_produto.get()
        qtd = entrada_qtd.get()
        data = datetime.now().strftime("%Y-%m-%d")
        if id_cliente and id_produto and qtd:
            with conectar() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO vendas (id_cliente, data) VALUES (?, ?)", (id_cliente, data))
                id_venda = cur.lastrowid
                cur.execute("INSERT INTO itens_venda (id_venda, id_produto, quantidade) VALUES (?, ?, ?)",
                            (id_venda, id_produto, qtd))
                cur.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (qtd, id_produto))
            messagebox.showinfo("Sucesso", f"Venda registrada com ID {id_venda}")
            janela_venda.destroy()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    tk.Button(janela_venda, text="Confirmar Venda", command=registrar_venda).grid(row=3, columnspan=2, pady=5)

# Exportar relatório
def exportar_relatorio():
    with conectar() as con:
        vendas = con.execute("""
            SELECT v.id, c.nome, v.data, p.nome, iv.quantidade, p.preco, (iv.quantidade * p.preco) as total
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id
            JOIN itens_venda iv ON iv.id_venda = v.id
            JOIN produtos p ON p.id = iv.id_produto
        """).fetchall()
    with open("relatorio_vendas.csv", "w", encoding="utf-8") as f:
        f.write("ID Venda,Cliente,Data,Produto,Quantidade,Preço Unitário,Total\n")
        for row in vendas:
            f.write(",".join(map(str, row)) + "\n")
    messagebox.showinfo("Exportado", "Relatório exportado como relatorio_vendas.csv")

# Janela principal com rolagem
janela = tk.Tk()
janela.title("Sistema de Vendas")
janela.geometry("800x600")

canvas = tk.Canvas(janela)
scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
frame_scroll = tk.Frame(canvas)

frame_scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_produtos = tk.LabelFrame(frame_scroll, text="Cadastrar Produto", padx=10, pady=10)
frame_produtos.pack(padx=10, pady=5, fill="x")

entrada_nome_produto = tk.Entry(frame_produtos)
tk.Label(frame_produtos, text="Nome:").grid(row=0, column=0)
entrada_nome_produto.grid(row=0, column=1)

entrada_preco = tk.Entry(frame_produtos)
tk.Label(frame_produtos, text="Preço:").grid(row=1, column=0)
entrada_preco.grid(row=1, column=1)

entrada_estoque = tk.Entry(frame_produtos)
tk.Label(frame_produtos, text="Estoque:").grid(row=2, column=0)
entrada_estoque.grid(row=2, column=1)

tk.Button(frame_produtos, text="Salvar Produto", command=salvar_produto).grid(row=3, columnspan=2, pady=5)

frame_clientes = tk.LabelFrame(frame_scroll, text="Cadastrar Cliente", padx=10, pady=10)
frame_clientes.pack(padx=10, pady=5, fill="x")

entrada_nome_cliente = tk.Entry(frame_clientes)
tk.Label(frame_clientes, text="Nome:").grid(row=0, column=0)
entrada_nome_cliente.grid(row=0, column=1)

entrada_email = tk.Entry(frame_clientes)
tk.Label(frame_clientes, text="Email:").grid(row=1, column=0)
entrada_email.grid(row=1, column=1)

tk.Button(frame_clientes, text="Salvar Cliente", command=salvar_cliente).grid(row=2, columnspan=2, pady=5)

frame_lista = tk.LabelFrame(frame_scroll, text="Produtos Cadastrados", padx=10, pady=10)
frame_lista.pack(padx=10, pady=5, fill="both", expand=True)

colunas = ("ID", "Nome", "Preço", "Estoque")
tabela = ttk.Treeview(frame_lista, columns=colunas, show="headings")
for col in colunas:
    tabela.heading(col, text=col)
tabela.pack(fill="both", expand=True)

tk.Button(frame_scroll, text="Atualizar Produtos", command=mostrar_produtos).pack(pady=5)

frame_clientes_lista = tk.LabelFrame(frame_scroll, text="Clientes Cadastrados", padx=10, pady=10)
frame_clientes_lista.pack(padx=10, pady=5, fill="both", expand=True)

colunas_clientes = ("ID", "Nome", "Email")
tabela_clientes = ttk.Treeview(frame_clientes_lista, columns=colunas_clientes, show="headings")
for col in colunas_clientes:
    tabela_clientes.heading(col, text=col)
tabela_clientes.pack(fill="both", expand=True)

tk.Button(frame_scroll, text="Atualizar Clientes", command=mostrar_clientes).pack(pady=5)

criar_tabelas()
mostrar_produtos()
mostrar_clientes()

frame_botoes = tk.Frame(frame_scroll)
frame_botoes.pack(pady=10)
tk.Button(frame_botoes, text="Registrar Venda", command=interface_vendas).pack(side="left", padx=10)
tk.Button(frame_botoes, text="Exportar PDF", command=exportar_relatorio_pdf).pack(side="left", padx=10)
tk.Button(frame_botoes, text="Ver Vendas", command=mostrar_vendas).pack(side="left", padx=10)

janela.mainloop()
