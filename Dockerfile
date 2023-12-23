FROM python:3.10

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-dev

COPY ./app /code/app

ENV PYTHONPATH=/code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
