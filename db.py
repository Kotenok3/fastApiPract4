from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models.db_models import Base, Author, Book
from config import settings

engine = create_async_engine(settings.POSTGRES_DATABASE_URL, echo=True)


async def get_session():
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def db_init():
    await create_tables()

    async with engine.begin() as conn:
        author1 = Author(name='Клюев Александр', birth_year=2002)
        author2 = Author(name='Л.Толстой', birth_year=1828)
        author3 = Author(name='Ф.Достоевский', birth_year=1821)

        await conn.execute(
            insert(Author).values([
                {"name": author1.name, "birth_year": author1.birth_year},
                {"name": author2.name, "birth_year": author2.birth_year},
                {"name": author3.name, "birth_year": author3.birth_year}
            ])
        )

        books = [
            {"title": 'FastApiPrct2', "release_year": 2023, "author_id": 1},
            {"title": 'FastApiPrct3', "release_year": 2024, "author_id": 1},
            {"title": 'Война и мир', "release_year": 1869, "author_id": 2},
            {"title": 'Преступление и наказание', "release_year": 1866, "author_id": 3},
            {"title": 'Мастер и Маргарита', "release_year": 1967, "author_id": 3}
        ]

        await conn.execute(
            insert(Book).values(books)
        )

        await conn.execute(text('commit'))
