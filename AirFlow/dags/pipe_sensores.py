from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Diretório onde os scripts de sensores estão dentro do container
SENSORES_DIR = "/app/sensores_iot"

# Argumentos padrão da DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 8),
    "retries": 1
}

# Criando a DAG
with DAG(
    dag_id="pipe_sensores",
    default_args=default_args,
    schedule_interval="@hourly",  # Executa a cada hora
    catchup=False
) as dag:

    # Tarefa 1: Iniciar Producer (gera os eventos)
    tarefa_producer = BashOperator(
        task_id="executar_producer",
        bash_command=f"python {SENSORES_DIR}/producer.py"
    )

    # Tarefa 2: Iniciar Consumer (processa os eventos)
    tarefa_consumer = BashOperator(
        task_id="executar_consumer",
        bash_command=f"python {SENSORES_DIR}/consumer.py"
    )

    # Definição da ordem das tarefas
    tarefa_producer >> tarefa_consumer