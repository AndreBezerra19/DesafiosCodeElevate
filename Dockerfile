FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV DIARIO_DIR=/app/diario_de_bordo
ENV SENSORES_DIR=/app/sensores

CMD ["airflow", "standalone"]