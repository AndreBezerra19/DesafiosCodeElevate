FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py consumer.py /app/
COPY dags /opt/airflow/dags/
COPY dados /opt/airflow/dados/

CMD ["tail", "-f", "/dev/null"]