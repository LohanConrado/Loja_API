from typing import Optional, Union, List
from fastapi import Body, FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.pedidos_itens import getPedidosItens
from bd import DataBase
from models.pedidos import getPedidos, setPedidos
from psycopg.sql import SQL, Identifier, Placeholder, Composed, Literal
import json


class Pedidos():
    def __init__(self) -> None:
        self.pedidos_router = APIRouter(prefix='\pedidos',
                                        tags=['Pedidos']
                                        )
        self.pedidos_router.add_api_route(
            '',
            self.getPedidos,
        )

    def getPedidos(self):
        try:
            model_list_pedidos = getPedidos.model_construct()
            model_list_pedidos.pedidos.clear()

            queryPedidos = """
                SELECT
                p.id,
                c.cpf AS cpf_cliente,
                c.name AS nome_cliente,
                p.subtotal,
                p.desconto,
                p.taxa,
                p.total
                FROM pedidos p
                LEFT JOIN cliente c ON (p.id_cliente = c.id)
            """

            queryPedidosItens = getPedidosItens(self)
