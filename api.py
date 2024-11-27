from typing import Union
from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel, Field
from routes.clientes import Clientes
from routes.produtos import Produtos

try:
    app = FastAPI(#docs_url=None,
                  #redoc_url=None,
                  title='Loja',
                  description='API de comunicação com o banco de dados',
                  version='0.2')
    clientesRoutes = Clientes()
    app.include_router(clientesRoutes.ClientesRouter)
    produtosRoutes = Produtos()
    app.include_router(produtosRoutes.produtosRouter)
except:
    print("n")