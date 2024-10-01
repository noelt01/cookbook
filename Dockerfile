FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app/
COPY .env /.env

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]