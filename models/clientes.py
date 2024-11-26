from typing import Optional, Union, List
from fastapi import FastAPI
from pydantic import BaseModel, Field


class getClientes(BaseModel):
    class Cliente(BaseModel):
        id: Union[int, None] = Field(0)
        cpf: str = Field("")
        nome: str = Field("")
        idade: int = Field(0)
    clientes: Optional[List[Cliente]] = Field([Cliente()])


class setCliente(BaseModel):
    id: Union[int, None] = Field(0)
    cpf: str = Field("")
    name: str = Field("")
    age: int = Field(0)
