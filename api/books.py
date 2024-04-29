from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.Tags import Tags
from models.db_models import Book
from models.simple_models import SimpleBook
from db import get_session
from starlette import status

bookRouter = APIRouter(prefix='/api/book', tags=[Tags.books])


@bookRouter.get("/")
async def get_books(db: AsyncSession = Depends(get_session)):
    books = await db.execute(select(Book))
    return books.scalars().all()


@bookRouter.get("/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_session)):
    try:
        book = await db.execute(select(Book).where(Book.id == book_id))
        return book.scalars().one()
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": "Книга не найдена"})


@bookRouter.post("/", response_model=SimpleBook, status_code=status.HTTP_201_CREATED)
async def create_book(item: SimpleBook, db: AsyncSession = Depends(get_session)):
    new_book = Book(title=item.title, release_year=item.release_year, author_id=item.author_id)
    try:
        if new_book is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в добавлении объекта {new_book}")


@bookRouter.delete("/{id}")
async def delete_book(id: int, db: AsyncSession = Depends(get_session)):
    book = await db.execute(select(Book).filter(Book.id == id))
    book = book.scalars().first()

    if book is None:
        return JSONResponse(status_code=404, content={"message": "Автор не найден"})

    try:
        await db.delete(book)
        await db.commit()
    except Exception as e:
        return JSONResponse(content={"message": f"Ошибка: {str(e)}"})

    return JSONResponse(content={"message": f"Автор удалён: {id}"})
