from typing import Optional, Union, List
from fastapi import Body, FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bd import DataBase
from models.pedidos import getPedidos, setPedidos
from psycopg.sql import SQL, Identifier, Placeholder, Composed, Literal
import json


class PedidosItens():
    def __init__(self) -> None:
        self.pedidositens_router = APIRouter(prefix="/pedidosItens",
                                             tags=["pedidosItens"]
                                             )

        self.pedidositens_router.add_api_route(
            '',
            self.getPedidosItens,
        )

    def getPedidosItens(self):
        try:
            queryItens = """
            SELECT 
            pe.id AS id_pedidos,
            pi.id AS id_peditos_itens,
            po.id AS id_produto,
            po.nome,
            pi.valor,
            pi.quantidade,
            pi.total 
            FROM pedidos_itens pi
            INNER JOIN pedidos pe ON (pi.id_pedidos = pe.id)
            LEFT JOIN produto po ON (pi.id_produto = po.id)
            """
