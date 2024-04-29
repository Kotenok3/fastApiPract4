# нужные библиотеки
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from public.users import U_R
from public.companies import C_R
from datetime import datetime
from public.db import create_tables, index_builder
from contextlib import asynccontextmanager

# заполнение таблиц начальными данными
index_builder()

# занесение информации о включении и выключении в log.txt
@asynccontextmanager
async def lifespan(app: FastAPI):
    open("log.txt", mode="a").write(f'{datetime.now()}: Begin\n')
    yield
    open("log.txt", mode="a").write(f'{datetime.now()}: End\n')

# Экземпляр FastAPI
app = FastAPI(lifespan=lifespan)

# включаем роутеры
app.include_router(U_R)
app.include_router(C_R)

@app.get('/')
def index():
    return FileResponse("files/index.html")