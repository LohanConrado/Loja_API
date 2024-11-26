from typing import Union
from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel, Field
from uvicorn import run
import os

if __name__ == '__main__':
    
    import api
    
    run('api:app',
        port=8001)

