from typing import Optional, Union, List
from fastapi import FastAPI
from pydantic import BaseModel, Field

class getPedidos(BaseModel):
    class Pedido(BaseModel):
        pedido_id: Union[int, None] = Field(0)
        cpf_cliente: Union[str, None] = Field('')
        nome_cliente: Union[str, None] = Field('')
        subtotal_pedido: float = Field(0.00)
        desconto_pedido: Union[int, None] = Field(0)
        taxa_pedido: int = Field(0)
        total_pedido: float = Field(0)
    pedidos: Optional[List[Pedido]] = Field(List[Pedido()])

class setPedidos(BaseModel):
    class Pedido(BaseModel):
        id: Union[int, None] = Field(0)
        id_cliente: Union[int, None] = Field(0)
        subtotal: float = Field(0.00)
        desconto: Union[int, None] = Field(0)
        taxa: int = Field(0)
        total: float = Field(0)