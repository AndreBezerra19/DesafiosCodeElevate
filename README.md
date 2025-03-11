# Desafios Code Elevate

## *Objetivo:*
  Nesse repositório, vamos desenvolver 2 projetos solicitados nos desafios da esteira **Code Elevate**.
  
  Os desafios serão separados em pastas para melhor visualização dos códigos. Os resultados serão centralizados em um banco de dados DuckDB para todos os projetos.
  
  Arquivos originais que serão consumidos, estarão na pasta raiz do projeto.

  - **Tecnologias utilizadas:**
  - *Python*
  - *Pyspark*
  - *Kafka*
  - *DuckDB*
  - *Docker*
  - *AirFlow*

### 1 - *Diário de bordo*

#### 📌 Objetivo do Projeto

Este projeto tem como objetivo criar um sistema de monitoramento de sensores IoT, utilizando Apache Kafka para transmissão de dados em tempo real e DuckDB para armazenamento e análise. O fluxo de dados segue os seguintes passos:

- **Producer**: gera dados simulados de sensores e os envia para um tópico no Kafka.
- **Kafka**: gerencia e distribui os dados.
- **Consumer**: recebe os dados do tópico Kafka e os armazena no banco de dados DuckDB.
- **Airflow** *(em desenvolvimento)* será responsável por orquestrar e monitorar o fluxo de dados.
- **Docker**: será utilizado para empacotar e facilitar a execução do projeto.

#### 🔧 Tecnologias Utilizadas

- Python
- Apache Kafka
- DuckDB
- Airflow (orquestração - em desenvolvimento)
- Docker (containerização)

#### 🛠 Configuração do Ambiente e execução
      1️⃣ Subir o Kafka com Docker
        O Kafka e o Zookeeper são executados via Docker Compose.
    
      2️⃣ Criar o Tópico Kafka
        Após iniciar o Kafka, crie um tópico chamado iot_sensors:
    
      3️⃣ Rodar o Producer
        O Producer gera dados de sensores simulados e os envia para o Kafka.
### 2 - *Monitoramento de sensores IoT*
