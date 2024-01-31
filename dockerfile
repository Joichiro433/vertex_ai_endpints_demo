FROM python:3.10-slim

RUN apt-get update -y \
    && apt-get install -y libgomp1 \
    && apt-get install -y gcc \
    && apt-get -y clean all

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    rm -rf ~/.cache

COPY ./app /app

WORKDIR /app

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
