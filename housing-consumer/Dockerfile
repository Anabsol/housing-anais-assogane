FROM python:3.9

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "consumer.py"]
