from typing import Optional, Union, List
from fastapi import Body, FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bd import DataBase
from models.clientes import getClientes, setCliente
from psycopg.sql import SQL, Identifier, Placeholder, Composed, Literal
import json


class Pedidos():
    def __init__(self) -> None:
        self.PedidosRouter = APIRouter(prefix='\pedidos',
                                       tags=['Pedidos'])