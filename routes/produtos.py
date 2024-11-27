from typing import Optional, Union, List
from fastapi import Body, FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bd import DataBase
from models.produtos import getProdutos, setProdutos
from psycopg.sql import SQL, Identifier, Placeholder, Composed, Literal
import json


class Produtos():
    def __init__(self) -> None:

        self.produtosRouter = APIRouter(prefix='/produtos',
                                        tags=['Produtos'],
                                        )

        self.produtosRouter.add_api_route(
            '',
            self.get_Produtos,
            description='Trazer todos os produtos',
            name='',
            methods=['GET'],
            response_model=getProdutos,
            status_code=200
        )
        self.produtosRouter.add_api_route(
            '',
            self.set_Produtos,
            description='Adicionar produto',
            name='',
            methods=['POST'],
            response_model=setProdutos,
            status_code=200
        )
        self.produtosRouter.add_api_route(
            '',
            self.delete_Produtos,
            description='Deletar produto',
            name='',
            methods=['DELETE'],
            response_model=setProdutos,
            status_code=200
        )
        self.produtosRouter.add_api_route(
            '',
            self.alterar_Produto,
            description='Alterar produto',
            name='',
            methods=['PATCH'],
            response_model=setProdutos,
            status_code=200
        )

    def get_Produtos(self):
        try:
            model_list_produtos = getProdutos.model_construct()
            model_list_produtos.produtos.clear()
            with DataBase() as banco:
                query_produtos = ("SELECT * FROM produto")
                resultado = banco.query(query_produtos)
                if resultado:
                    for id in resultado:
                        model_list_produtos.produtos.append(
                            model_list_produtos.Produto.model_construct().model_validate(id))
            return JSONResponse(json.loads(model_list_produtos.model_dump_json()), 200)

        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))

    def set_Produtos(self, produtoInfo: setProdutos = Body(...)):
        try:
            with DataBase() as banco:
                if not banco.queryone('SELECT id FROM produto WHERE cod = %s', [produtoInfo.id]):
                    query_str = SQL("INSERT INTO produto ({fields}) VALUES ({values}) RETURNING id").format(
                        fields=SQL(', ').join(map(Identifier, produtoInfo.model_dump(
                            exclude={'id'}))),
                        values=SQL(', ').join(map(Placeholder, produtoInfo.model_dump(
                            exclude={'id'})))
                    ).as_string(banco.connection)
                    result = banco.queryone(
                        query_str, produtoInfo.model_dump())
                    if result:
                        produtoInfo.id = result['id']
                        banco.commit()
                    return JSONResponse(json.loads(produtoInfo.model_dump_json()), 201)
                else:
                    raise HTTPException(
                        409, 'Já existe um produto com o mesmo código')
        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))

    def delete_Produtos(self, produto_info: setProdutos):
        try:
            with DataBase() as banco:
                banco.execute('DELETE FROM produto WHERE id = %s', [
                              produto_info.id])
                banco.commit()
                return JSONResponse({'detail': 'sucess'}, 200)
        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))

    def alterar_Produto(self, produto_info: setProdutos = Body(...)):
        try:
            with DataBase() as banco:
                if not banco.queryone('SELECT * FROM produto WHERE id = %s', [produto_info.id]):
                    raise HTTPException(404, "Produto não existe")
                else:
                    query_produto = SQL('UPDATE produto SET {data} WHERE id = %(id)s ').format(
                                        data=SQL(', ').join(Composed([Identifier(field), SQL(' = '), Placeholder(field)]) for field in produto_info.model_dump(
                                            exclude={'id'}))
                    ).as_string(banco.connection)
                    banco.execute(query_produto, produto_info.model_dump())
                    banco.commit()
                    return JSONResponse(json.loads(produto_info.model_dump_json()), 200)
        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(400, str(E))
