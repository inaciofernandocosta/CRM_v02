# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-01-19

### Adicionado
- Análise RFV (Recência, Frequência, Valor) dos clientes
- Análise de Pareto (regra 80/20)
- Análise de mix de produtos por cliente
- Análise de participação por estado
- Métricas de concentração de faturamento
- Relatório gerencial aprimorado com novas seções:
  - Mix de Produtos por Cliente
  - Análise de Pareto e Concentração
  - Performance por Estado
  - Análise RFV
- Novas abas no Excel:
  - Análise RFV
  - Análise de Pareto
  - Top 20 Clientes
  - Análise por Família

### Modificado
- Renomeado arquivo de saída para 'relatorio_gerencial.xlsx'
- Melhorada a estrutura de análise de dados
- Aprimorada a apresentação das métricas
- Expandido o número de top clientes de 10 para 20
- Melhorada a integração entre as bases de dados

## [1.1.0] - 2025-01-19

### Adicionado
- Integração com dados de faturamento
- Análise de performance financeira
- Cálculo de métricas de faturamento (total, médio, mediano)
- Identificação dos top 10 clientes por faturamento
- Análise temporal do faturamento por semana
- Cálculo de crescimento semana a semana
- Análise por categoria de produtos/serviços
- Análise por tipo de negócio
- Novas abas no relatório Excel:
  - Métricas Principais
  - Distribuição por Estado
  - Top 10 Clientes
  - Faturamento Semanal
  - Análise por Categoria
  - Análise por Negócio
- Formatação de valores monetários no relatório

### Modificado
- Estrutura do projeto simplificada
- Remoção de arquivos desnecessários
- Atualização da documentação
- Ajuste nas colunas utilizadas para análise de faturamento

## [1.0.0] - 2025-01-19

### Adicionado
- Implementação inicial do processador de dados de clientes
- Classe `CustomerDataProcessor` para processamento de arquivos Excel
- Classe `CustomerDataCrew` para gerenciamento do fluxo de trabalho
- Funcionalidade de contagem de clientes distintos
- Análise de distribuição geográfica por estado
- Geração de relatório detalhado em texto
- Exportação de métricas para arquivo Excel
- Configuração de logging para rastreamento de execução
- Tratamento de erros e validações
- Documentação inicial do projeto (README.md)

### Modificado
- Ajuste na detecção do status de atividade dos clientes
- Melhoria na formatação do relatório de saída
- Otimização do processamento de dados

### Corrigido
- Correção na contagem de clientes ativos
- Ajuste no nome da coluna de clientes
- Melhoria nas mensagens de erro

## [0.2.0] - 2025-01-17

### Adicionado
- Implementação da classe `CustomerDataProcessor`
- Funcionalidade básica de processamento de Excel
- Sistema de logging

### Modificado
- Reestruturação do código para melhor organização
- Separação de responsabilidades em classes distintas

## [0.1.0] - 2025-01-16

### Adicionado
- Estrutura inicial do projeto
- Configuração básica do ambiente
- Primeiros testes de conceito
