import sqlite3
import pandas as pd
import sys
from pathlib import Path

# Local onde o banco será persistido (ao lado do .exe ou do projeto)
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.resolve()

DB_PATH = str(BASE_DIR / "estoque_setor.db")

def get_connection():
    """Cria e retorna uma conexão com o SQLite."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    """Cria a tabela se não existir."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                estado TEXT NOT NULL,
                localizacao TEXT NOT NULL
            )
        """)
        conn.commit()

def listar_itens() -> pd.DataFrame:
    """Retorna todos os registros em formato DataFrame."""
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM itens ORDER BY id DESC", conn)

def adicionar_item(descricao: str, quantidade: int, estado: str, localizacao: str):
    """Adiciona um novo item ao estoque."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO itens (descricao, quantidade, estado, localizacao)
            VALUES (?, ?, ?, ?)
        """, (descricao, quantidade, estado, localizacao))
        conn.commit()
        return True

def atualizar_item(id_item: int, descricao: str, quantidade: int, estado: str, localizacao: str):
    """Atualiza um registro existente."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE itens
            SET descricao = ?, quantidade = ?, estado = ?, localizacao = ?
            WHERE id = ?
        """, (descricao, quantidade, estado, localizacao, id_item))
        conn.commit()

def deletar_item(id_item: int):
    """Remove um registro pelo ID."""
    with get_connection() as conn:
        conn.execute("DELETE FROM itens WHERE id = ?", (id_item,))
        conn.commit()

def incrementar_item(id_item: int, quantidade: int):
    """Incrementa a quantidade de um item pelo ID."""
    with get_connection() as conn:
        conn.execute("UPDATE itens SET quantidade = quantidade + ? WHERE id = ?", (quantidade, id_item))
        conn.commit()

def decrementar_item(id_item: int, quantidade: int):
    """Decrementa a quantidade de um item pelo ID (garantindo saldo mínimo zero)."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE itens 
            SET quantidade = MAX(0, quantidade - ?) 
            WHERE id = ?
        """, (quantidade, id_item))
        conn.commit()