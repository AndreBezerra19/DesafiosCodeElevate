from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Diretório onde os scripts estão dentro do container
DIARIO_DIR = "/app/diario_de_bordo"

# Argumentos padrão da DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 8),
    "retries": 1
}

# Criar DAG
with DAG(
    dag_id="pipe_transportes",
    default_args=default_args,
    schedule_interval="@daily",  # Diariamente
    catchup=False
) as dag:

    # Ingestão de dados
    insgest_data = BashOperator(
        task_id="executar_ingestao",
        bash_command=f"python {DIARIO_DIR}/ingest_data.py"
    )
    # Processamento de dados
    process_data = BashOperator(
        task_id="executar_etl",
        bash_command=f"python {DIARIO_DIR}/process_data.py"
    )
    # Ordem das tarefas
    insgest_data >> process_data