from typing import List, Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel, Field

class getProdutos(BaseModel):
    class Produto(BaseModel):
        id: Union[int, None] = Field(0)
        nome: str = Field("")
        valor: float = Field(0.00)
        active: int = Field(1)
    produtos: Optional[List[Produto]] = Field([Produto])