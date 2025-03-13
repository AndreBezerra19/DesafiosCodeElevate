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

#### 📌 Objetivo

O projeto Diário de Bordo tem como objetivo processar e armazenar informações sobre registros operacionais de transportes, garantindo a integridade e qualidade dos dados para análise. O fluxo de dados segue os seguintes passos:

**Ingestão de Dados**: leitura de arquivos CSV e armazenamento no DuckDB.
**Processamento de Dados**: aplicação de transformações usando PySpark.

#### 🔧 Tecnologias Utilizadas

- Python
- PySpark
- DuckDB
- Docker (containerização)

#### Configuração do Ambiente e Execução
       Subir o ambiente com Docker
       DuckDB e dependências, são executados via Docker Compose.
   
       Rodar o processo de Ingestão de Dados
       O script **ingest_data.py** lê os dados do CSV e armazena no DuckDB.
   
       Executar o Processamento de Dados
       O script **process_data.py** realiza transformações nos dados usando PySpark.
   
       Validar os Dados no DuckDB
       Verifica a estrutura e integridade dos dados no banco.
       
### 2 - *Monitoramento de sensores IoT*

#### 📌 Objetivo

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

####  Configuração do Ambiente e execução
        Subir o Kafka com Docker
        O Kafka e o Zookeeper são executados via Docker Compose.
    
        Criar o Tópico Kafka
        Após iniciar o Kafka, crie um tópico chamado iot_sensors:
    
        Rodar o Producer
        O Producer gera dados de sensores simulados e os envia para o Kafka.


# **Guia de Execução**

Todos os componentes do projeto são executados dentro de containers Docker.

---

## **Configuração do Ambiente**

### **Instale o Docker e o Docker Compose**
Se ainda não tiver instalado, siga as instruções originais:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### **Clone este repositório**
```bash
git clone https://github.com/seu-repositorio.git
cd DesafiosCodeElevate
```

---

## **Como Executar os Containers**

### **Construir e iniciar os containers**
```bash
docker-compose up --build -d
```
Isso iniciará os containers:
- `app`: Container principal onde os scripts Python serão executados.
- `kafka`: Servidor Kafka.
- `zookeeper`: Necessário para o Kafka funcionar.

### **Verificar se os containers estão rodando**
```bash
docker ps
```
Se tudo estiver correto, os containers serão listados.

---

## **Executar os Scripts do Projeto Transportes**

### **Acessar o aplicativo `app`**
```bash
docker exec -it desafioscodeelevate-app-1 bash
```

### **Rodar a ingestão de dados**
```bash
python /app/diario_de_bordo/ingest_data.py
```

### **Processar os dados**
```bash
python /app/diario_de_bordo/process_data.py
```

---

## **Executar o Projeto Sensores IoT**

### **Iniciar o Producer**
```bash
python /app/sensores_iot/producer.py
```

### **Iniciar o Consumer**
```bash
python /app/sensores_iot/consumer.py
```

---

## **Verificar os Dados no DuckDB**

### **Entrar no Python via container**
```bash
python
```

### **Listar as tabelas**
```python
import duckdb
con = duckdb.connect("/app/db_desafios.duckdb")
print(con.execute("SELECT table_name FROM information_schema.tables").fetchall())
```

### **Consultar os dados**
```python
print(con.execute("SELECT * FROM sensor_monitor.b_sensores_iot LIMIT 10").fetchall())
con.close()
```

Para sair do Python, digite `exit()`.

---

## **Parar os Containers**
Se precisar interromper todos os containers:
```bash
docker-compose down
```

---



