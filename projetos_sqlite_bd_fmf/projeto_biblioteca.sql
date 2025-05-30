
-- Projeto 1: Biblioteca

CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    ano INTEGER,
    id_autor INTEGER,
    FOREIGN KEY(id_autor) REFERENCES autores(id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT
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
