from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Annotated, Union
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from models.models_company import *
from models.dbcontext import *
from public.db import get_session
from starlette import status
from sqlalchemy import select, insert, text

C_R = APIRouter(tags = [Tags.companies], prefix = '/api/companies')

@C_R.get("/", response_model = Union[list[Main_Company], New_Respons], tags=[Tags.companies])
async def get_companies_db(DB: AsyncSession = Depends(get_session)):
    companies = await DB.execute(select(Company).order_by(Company.id.asc()))
    result = companies.scalars().all()
    if result == []:
        return JSONResponse(status_code=404, content={"message": "Компании не найдены"})
    return result

@C_R.get("/{id}", response_model = Union[Main_Company, New_Respons], tags=[Tags.companies])
async def get_company(id: int, DB: AsyncSession = Depends(get_session)):
    try:
        company = await DB.execute(select(Company).where(Company.id == id))
        return company.scalars().one()
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": "Компания не найдена"})

@C_R.post("/", response_model = Union[Main_Company, New_Respons], tags=[Tags.companies], status_code=status.HTTP_201_CREATED)
async def create_company(item: Annotated[Main_Company, Body(embed = True, description = "Новый пользователь")],
                DB: AsyncSession = Depends(get_session)):
    try:
        company = Company(name = item.name, country = item.country)
        if company is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        await DB.execute(insert(Company).values({"name": company.name, "country": company.country}))
        await DB.execute(text("commit;"))
        return company
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в добавлении объекта {company}")

@C_R.delete("/{id}", response_class=JSONResponse, tags=[Tags.companies])
async def delete_company(id: int, DB: AsyncSession = Depends(get_session)):
    company = await DB.execute(select(Company).where(Company.id == id))
    if company.first() == None:
        return JSONResponse(status_code=404, content={"message": "Компания не найдена"})
    try:
        await DB.execute(text(f'delete from companies where id={id};'))
        await DB.execute(text("commit;"))
    except HTTPException:
        JSONResponse(content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Компания удалёна {id}"})