
import sqlite3

def conectar():
    return sqlite3.connect("biblioteca.db")

def criar_tabelas():
    with conectar() as con:
        con.executescript(open("projeto_biblioteca.sql", encoding="utf-8").read())

def adicionar_livro():
    titulo = input("Título do livro: ")
    ano = input("Ano: ")
    id_autor = input("ID do autor: ")
    with conectar() as con:
        con.execute("INSERT INTO livros (titulo, ano, id_autor) VALUES (?, ?, ?)", (titulo, ano, id_autor))
        print("Livro adicionado com sucesso.")

def listar_livros():
    with conectar() as con:
        for row in con.execute("SELECT livros.id, titulo, ano FROM livros"):
            print(row)
def adicionar_autor():
    nome = input("Nome do autor: ")
    with sqlite3.connect("biblioteca.db") as con:
        con.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
        print("Autor adicionado com sucesso.")

def adicionar_usuario():
    nome = input("Nome do usuário: ")
    email = input("Email do usuário: ")
    with sqlite3.connect("biblioteca.db") as con:
        con.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        print("Usuário adicionado com sucesso.")

def adicionar_emprestimo():
    id_livro = input("ID do livro: ")
    id_usuario = input("ID do usuário: ")
    data_emprestimo = input("Data de empréstimo (AAAA-MM-DD): ")
    data_devolucao = input("Data de devolução (AAAA-MM-DD): ")
    with sqlite3.connect("biblioteca.db") as con:
        con.execute("""
            INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_devolucao)
            VALUES (?, ?, ?, ?)
        """, (id_livro, id_usuario, data_emprestimo, data_devolucao))
        print("Empréstimo registrado com sucesso.")


def menu():
    criar_tabelas()
    while True:
        print("\\n--- MENU BIBLIOTECA ---")
        print("1. Adicionar autor")
        print("2. Adicionar usuário")
        print("3. Adicionar livro")
        print("4. Registrar empréstimo")
        print("5. Listar livros")
        print("6. Sair")
        opcao = input("Escolha: ")
        if opcao == "1":
            adicionar_autor()
        elif opcao == "2":
            adicionar_usuario()
        elif opcao == "3":
            adicionar_livro()
        elif opcao == "4":
            adicionar_emprestimo()
        elif opcao == "5":
            listar_livros()
        elif opcao == "6":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
