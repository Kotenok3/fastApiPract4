FROM python:3.10-slim

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY requirements.txt .

RUN python -m pip install --progress-bar off --upgrade pip
RUN python -m pip install --progress-bar off -r requirements.txt

COPY . .

RUN alembic upgrade head

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]