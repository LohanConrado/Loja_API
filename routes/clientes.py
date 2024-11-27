from typing import Optional, Union, List
from fastapi import Body, FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bd import DataBase
from models.clientes import getClientes, setCliente
from psycopg.sql import SQL, Identifier, Placeholder, Composed, Literal
import json


class Clientes():
    def __init__(self) -> None:

        self.ClientesRouter = APIRouter(prefix='/clientes',
                                        tags=['Clientes'],
                                        )

        self.ClientesRouter.add_api_route('',
                                          self.get_Clientes,
                                          description='Trazer todos os usuários',
                                          name='',
                                          methods=['GET'],
                                          response_model=getClientes,
                                          status_code=200
                                          )
        self.ClientesRouter.add_api_route('',
                                          self.set_Cliente,
                                          description="Alocar cliente no bd",
                                          name='',
                                          methods=['POST'],
                                          response_model=setCliente,
                                          status_code=200
                                          )
        self.ClientesRouter.add_api_route('',
                                          self.deletar_cliente,
                                          description="Deletar cliente do bd",
                                          name='',
                                          methods=['DELETE'],
                                          status_code=200
                                          )
        self.ClientesRouter.add_api_route('',
                                          self.alterar_cliente,
                                          description="Alterar cliente do bd",
                                          name='',
                                          methods=['PATCH'],
                                          response_model=setCliente,
                                          status_code=200
                                          )

    def get_Clientes(self):
        try:
            model_list_clientes = getClientes.model_construct()
            model_list_clientes.clientes.clear()
            with DataBase() as banco:
                queryClientes = f""" SELECT * FROM cliente """
                resultado = banco.query(queryClientes)
                if resultado:
                    for cpf in resultado:
                        model_list_clientes.clientes.append(model_list_clientes.Cliente.model_construct().model_validate(cpf))

            return JSONResponse(json.loads(model_list_clientes.model_dump_json()), 200)

        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))

    def set_Cliente(self, clienteInfo: setCliente = Body(...)):
        try:
            with DataBase() as banco:
                if not banco.queryone('SELECT id FROM cliente WHERE cpf = %s', [clienteInfo.cpf]):
                    queryStr = SQL("INSERT INTO cliente ({fields}) VALUES ({values}) RETURNING id").format(
                        fields=SQL(', ').join(map(Identifier, clienteInfo.model_dump(
                            exclude={'id'}))),
                        values=SQL(', ').join(map(Placeholder, clienteInfo.model_dump(
                            exclude={'id'})))
                    ).as_string(banco.connection)
                    result = banco.queryone(
                        queryStr, clienteInfo.model_dump())
                    if result:
                        clienteInfo.id = result['id']
                        banco.commit()
                    return JSONResponse(json.loads(clienteInfo.model_dump_json()), 201)
                else:
                    raise HTTPException(409, 'Cliente já existe!')
        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))
            
    def deletar_cliente(self, cliente_info: setCliente):
        try:
            with DataBase() as banco:
                banco.execute('DELETE FROM cliente WHERE id = %s', [cliente_info.id])
                banco.commit()
                return JSONResponse({'detail':'sucess'}, 200)
        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))
            
    def alterar_cliente(self, cliente_info: setCliente = Body(...)):
        try:
            with DataBase() as banco:
                if not banco.queryone("SELECT FROM cliente WHERE id = %s", [cliente_info.id]):
                    raise HTTPException(404,"Cliente não existe!")
                else:
                    query_cliente = SQL('UPDATE cliente SET {data} WHERE id = %(id)s').format(
                                        data=SQL(', ').join(Composed([Identifier(field), SQL(' = '), Placeholder(field)]) for field in cliente_info.model_dump(
                                            exclude={'id', 'cpf'}))
                                    ).as_string(banco.connection)
                    banco.execute(query_cliente, cliente_info.model_dump())
                    banco.commit()
                    return JSONResponse(json.loads(cliente_info.model_dump_json()), 200)
        except Exception as E:
            if isinstance(E,HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))