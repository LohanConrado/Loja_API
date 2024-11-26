from typing import Union
from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel, Field
from routes.clientes import Clientes

try:
    app = FastAPI(#docs_url=None,
                  #redoc_url=None,
                  title='Loja',
                  description='API de comunicação com o banco de dados',
                  version='0.2')
    clientesRoutes = Clientes()
    app.include_router(clientesRoutes.ClientesRouter)
except:
    print("n")