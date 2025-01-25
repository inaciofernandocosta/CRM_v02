# CREWAI - Processador de Dados de Clientes

## Visão Geral
Este projeto foi desenvolvido para processar dados de clientes a partir de arquivos Excel, realizando análises e gerando relatórios detalhados. O sistema utiliza a biblioteca CREWAI para orquestrar o processamento dos dados e gerar insights sobre a base de clientes.

## Funcionalidades Atuais

### 1. Processamento de Dados
- Leitura de arquivos Excel contendo dados de clientes
- Identificação e contagem de clientes distintos
- Análise de status de atividade dos clientes
- Distribuição geográfica dos clientes por estado
- Geração de relatórios em formato Excel e texto

### 2. Análises Disponíveis
- Total de clientes distintos
- Total de registros no arquivo
- Quantidade de clientes ativos
- Distribuição de clientes por estado
- Validação de dados e colunas necessárias

### 3. Relatórios Gerados
- Relatório detalhado em formato texto com:
  - Totalizadores de clientes
  - Distribuição geográfica
  - Detalhes do processamento
  - Status da execução
- Arquivo Excel com métricas principais:
  - Clientes distintos
  - Total de registros
  - Clientes ativos

## Estrutura do Projeto

### Diretórios
- `src/`: Código fonte do projeto
  - `main.py`: Ponto de entrada da aplicação
  - `customer_crew.py`: Classes principais de processamento
  - `config.py`: Configurações e variáveis de ambiente
- `input/`: Arquivos Excel de entrada
- `output/`: Relatórios e arquivos gerados
- `venv311/`: Ambiente virtual Python

### Classes Principais

#### CustomerDataProcessor
Responsável pelo processamento direto dos dados:
- Leitura do arquivo Excel
- Validação de dados
- Cálculo de métricas
- Geração de relatórios em Excel

#### CustomerDataCrew
Gerencia o fluxo de processamento:
- Orquestração do processamento
- Formatação do relatório final
- Interface com o usuário

## Requisitos do Sistema

### Dependências
- Python 3.11+
- pandas
- openpyxl
- crewai
- logging

### Variáveis de Ambiente
- `OPENAI_API_KEY`: Chave da API OpenAI (necessária para funcionalidades futuras)

## Como Usar

1. Configure o ambiente:
```bash
python -m venv venv311
source venv311/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

2. Configure a variável de ambiente:
```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

3. Execute o processamento:
```bash
python src/main.py
```

## Formato do Arquivo de Entrada
O arquivo Excel deve conter as seguintes colunas:
- `Razao Social`: Nome/Razão Social do cliente
- `Ativo`: Status de atividade do cliente
- `UF`: Estado do cliente
- Outras colunas informativas (opcionais)

## Saídas Geradas

### 1. Relatório em Texto
Um relatório detalhado contendo:
- Totalizadores de clientes
- Distribuição por estado
- Detalhes do processamento
- Status da execução

### 2. Arquivo Excel
Arquivo `logs.xlsx` contendo:
- Métricas principais
- Contagens e totalizadores

## Próximos Passos
1. Implementação de análises avançadas usando IA
2. Geração de gráficos e visualizações
3. Interface web para visualização dos resultados
4. Expansão das métricas e análises disponíveis

## Suporte
Para mais informações ou suporte, entre em contato com a equipe de desenvolvimento.

---
*Última atualização: 19 de Janeiro de 2025*
