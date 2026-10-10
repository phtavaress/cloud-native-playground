FROM python:3.13-slim

WORKDIR /app

COPY ./requirements.txt /app

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --uid 10001 --no-create-home appuser

USER 10001

COPY . /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]