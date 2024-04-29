from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.Tags import Tags
from models.db_models import Author
from models.simple_models import SimpleAuthor, SimpleAuthorPath
from db import get_session
from starlette import status

authorRouter = APIRouter(prefix='/api/author', tags=[Tags.authors])


@authorRouter.get("/")
async def get_authors(db: AsyncSession = Depends(get_session)):
    try:
        authors = await db.execute(select(Author).options(selectinload(Author.books)))

        if not authors:
            raise HTTPException(status_code=404, detail="Авторы не найдены")

        return authors.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")


@authorRouter.get("/{id}")
async def get_author(id: int, db: AsyncSession = Depends(get_session)):
    try:
        author = await db.execute(select(Author).filter(id == Author.id).options(selectinload(Author.books)))

        if not author:
            raise HTTPException(status_code=404, detail="Авторы не найдены")

        return author.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")


@authorRouter.post("/", response_model=SimpleAuthor, status_code=status.HTTP_201_CREATED)
async def create_author(item: SimpleAuthor, db: AsyncSession = Depends(get_session)):
    new_author = Author(name=item.name, birth_year=item.birth_year)
    try:
        if new_author is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        db.add(new_author)
        await db.commit()
        await db.refresh(new_author)
        return new_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в добавлении объекта {new_author}")


@authorRouter.delete("/{id}")
async def delete_author(id: int, db: AsyncSession = Depends(get_session)):
    author = await db.execute(select(Author).filter(Author.id == id))
    author = author.scalars().first()

    if author is None:
        return JSONResponse(status_code=404, content={"message": "Автор не найден"})

    try:
        await db.delete(author)
        await db.commit()
    except Exception as e:
        return JSONResponse(content={"message": f"Ошибка: {str(e)}"})

    return JSONResponse(content={"message": f"Автор удалён: {id}"})


@authorRouter.put("/")
async def edit_author(item: SimpleAuthor, db: AsyncSession = Depends(get_session)):
    author_await = await db.execute(select(Author).filter(item.id == Author.id))
    author = author_await.scalar()

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    author.name = item.name
    author.birth_year = item.birth_year
    db.add(author)

    await db.commit()

    await db.refresh(author)
    return author


@authorRouter.patch("/")
async def path_edit_user(item: SimpleAuthorPath, db: AsyncSession = Depends(get_session)):
    author_await = await db.execute(select(Author).where(Author.id == item.id))
    author = author_await.scalars().first()
    count_change = 0

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    if item.name is not None:
        author.name = item.name
        count_change += 1

    if item.birth_year is not None:
        author.birth_year = item.birth_year
        count_change += 1

    if count_change > 1:
        db.add(author)

        await db.commit()

        await db.refresh(author)
    return author
