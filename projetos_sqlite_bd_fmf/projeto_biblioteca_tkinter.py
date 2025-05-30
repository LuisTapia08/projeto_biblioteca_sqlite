
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect("biblioteca.db")

# Função para criar tabelas (se não existirem)
def criar_tabelas():
    with conectar() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            ano INTEGER,
            id_autor INTEGER,
            FOREIGN KEY(id_autor) REFERENCES autores(id)
        );

        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER,
            id_usuario INTEGER,
            data_emprestimo TEXT,
            data_devolucao TEXT,
            FOREIGN KEY(id_livro) REFERENCES livros(id),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        );
        """)

# Funções para cada ação
def adicionar_autor():
    nome = simpledialog.askstring("Adicionar Autor", "Nome do autor:")
    if nome:
        with conectar() as con:
            con.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
        messagebox.showinfo("Sucesso", "Autor adicionado com sucesso!")

def adicionar_usuario():
    nome = simpledialog.askstring("Adicionar Usuário", "Nome do usuário:")
    email = simpledialog.askstring("Adicionar Usuário", "Email do usuário:")
    if nome and email:
        with conectar() as con:
            con.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")

def adicionar_livro():
    titulo = simpledialog.askstring("Adicionar Livro", "Título do livro:")
    ano = simpledialog.askstring("Adicionar Livro", "Ano de publicação:")
    id_autor = simpledialog.askstring("Adicionar Livro", "ID do autor:")
    if titulo and ano and id_autor:
        with conectar() as con:
            con.execute("INSERT INTO livros (titulo, ano, id_autor) VALUES (?, ?, ?)", (titulo, ano, id_autor))
        messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")

def registrar_emprestimo():
    id_livro = simpledialog.askstring("Registrar Empréstimo", "ID do livro:")
    id_usuario = simpledialog.askstring("Registrar Empréstimo", "ID do usuário:")
    data_emprestimo = simpledialog.askstring("Registrar Empréstimo", "Data de Empréstimo (AAAA-MM-DD):")
    data_devolucao = simpledialog.askstring("Registrar Empréstimo", "Data de Devolução (AAAA-MM-DD):")
    if id_livro and id_usuario and data_emprestimo and data_devolucao:
        with conectar() as con:
            con.execute("""
                INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_devolucao)
                VALUES (?, ?, ?, ?)
            """, (id_livro, id_usuario, data_emprestimo, data_devolucao))
        messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")

def listar_livros():
    with conectar() as con:
        livros = con.execute("SELECT livros.id, titulo, ano, autores.nome FROM livros JOIN autores ON livros.id_autor = autores.id").fetchall()
    janela_lista = tk.Toplevel()
    janela_lista.title("Lista de Livros")
    tree = ttk.Treeview(janela_lista, columns=("ID", "Título", "Ano", "Autor"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.heading("Ano", text="Ano")
    tree.heading("Autor", text="Autor")
    tree.pack(fill=tk.BOTH, expand=True)
    for livro in livros:
        tree.insert("", tk.END, values=livro)

# Construir a interface
def main():
    criar_tabelas()
    root = tk.Tk()
    root.title("Sistema Biblioteca - Tkinter")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    tk.Button(frame, text="📚 Adicionar Autor", width=25, command=adicionar_autor).pack(pady=5)
    tk.Button(frame, text="👤 Adicionar Usuário", width=25, command=adicionar_usuario).pack(pady=5)
    tk.Button(frame, text="📖 Adicionar Livro", width=25, command=adicionar_livro).pack(pady=5)
    tk.Button(frame, text="📑 Registrar Empréstimo", width=25, command=registrar_emprestimo).pack(pady=5)
    tk.Button(frame, text="📚 Listar Livros", width=25, command=listar_livros).pack(pady=5)
    tk.Button(frame, text="❌ Sair", width=25, command=root.quit).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
