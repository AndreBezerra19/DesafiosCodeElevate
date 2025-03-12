FROM apache/airflow:2.7.3-python3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV AIRFLOW_HOME=/opt/airflow
ENV DIARIO_DIR=/app/diario_de_bordo
ENV SENSORES_DIR=/app/sensores

RUN airflow db init

CMD ["airflow", "webserver"]