from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, Field
from psycopg.rows import dict_row
import psycopg
class DataBase():

    def __init__(self) -> None:
        DB_HOST = "localhost"
        DB_PORT = "5433"
        DB_NAME = "Loja"
        DB_USER = "postgres"  # Usuário do banco
        DB_PASSWORD = "root"  # Senha do banco
        
        try:
            self._conn = psycopg.connect(
                f"""host='{DB_HOST}'
                port={DB_PORT}
                dbname='{DB_NAME}'
                user='{DB_USER}'
                password='{DB_PASSWORD}'
                """)
            self._cursor = self._conn.cursor(row_factory=dict_row)
        except Exception as E:
            raise Exception(f'Não foi possível conectar com o banco{"Error: ", E}' )
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(False)

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def queryone(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchone()