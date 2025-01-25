import os
import pandas as pd
import numpy as np
from crewai import Agent, Task, Crew
import logging
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
import yaml
from openai import OpenAI
from agents.analysis_orchestrator import AnalysisOrchestrator

# Carrega variáveis de ambiente
load_dotenv()

# Configurações globais
OUTPUT_FILE = os.path.join(os.getenv('OUTPUT_DIR', 'output'), "relatorio_gerencial.xlsx")
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
MODEL_NAME = os.getenv('GPT_MODEL', 'gpt-4')  # Usa gpt-4 como fallback se não encontrar no .env

# Cliente OpenAI global
openai_client = OpenAI()

def load_agent_config(agent_name: str) -> Dict[str, Any]:
    """Carrega configuração do agente do arquivo YAML"""
    config_file = os.path.join(CONFIG_DIR, "agents.yaml")
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config.get(agent_name, {})

class DataAnalysisAgent(Agent):
    def __init__(self):
        # Carrega configuração do arquivo YAML
        config = load_agent_config("data_analysis_agent")
        model_config = config.get('model_config', {})
        
        # Inicializa o agente com a configuração
        super().__init__(
            name=config.get("name", "Data Analysis Agent"),
            role=config.get("role", "Analista de Dados Especialista"),
            goal=config.get("goal", "Analisar dados e gerar insights estratégicos"),
            backstory=config.get("backstory", ""),
            verbose=config.get("verbose", True),
            allow_delegation=config.get("allow_delegation", False),
            llm_model=MODEL_NAME  # Usa o modelo definido no .env
        )
    
    def analyze_customer_base(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa a base de clientes e gera insights estratégicos"""
        try:
            # Por enquanto, retorna None (insights desativados)
            return None
            
        except Exception as e:
            logging.error(f"Erro ao analisar base de clientes: {str(e)}")
            return None

    def analyze_revenue_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisa padrões de faturamento e gera insights estratégicos"""
        try:
            # Por enquanto, retorna None (insights desativados)
            return None
            
        except Exception as e:
            logging.error(f"Erro ao analisar padrões de faturamento: {str(e)}")
            return None

class CustomerDataCrew:
    def __init__(self):
        """Inicializa o CustomerDataCrew"""
        # Configura logging com nível DEBUG
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.data = None
        self.faturamento = None
        self.analysis_orchestrator = AnalysisOrchestrator()
        
    def _carregar_dados(self, arquivo_clientes: str, arquivo_faturamento: str):
        """Carrega dados dos arquivos Excel"""
        try:
            logging.info("Iniciando processamento do arquivo.")
            
            # Carrega base de clientes
            self.data = pd.read_excel(arquivo_clientes)
            logging.info(f"Base de clientes carregada: {len(self.data)} registros")
            logging.debug(f"Colunas na base de clientes: {self.data.columns.tolist()}")
            logging.debug(f"Primeiras linhas da base de clientes:")
            logging.debug(self.data.head())
            
            # Carrega dados de faturamento
            self.faturamento = pd.read_excel(arquivo_faturamento)
            logging.info(f"Dados de faturamento carregados: {len(self.faturamento)} registros")
            logging.debug(f"Colunas no faturamento: {self.faturamento.columns.tolist()}")
            logging.debug(f"Primeiras linhas do faturamento:")
            logging.debug(self.faturamento.head())
            
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {str(e)}")
            raise
            
    def processar_dados(self, arquivo_clientes):
        """Processa os dados dos clientes"""
        try:
            # Carrega dados
            self._carregar_dados(arquivo_clientes, os.path.join(os.path.dirname(arquivo_clientes), 'faturamento.xlsx'))
            
            # Gera relatório com métricas e KPIs
            metricas = self._calcular_metricas()
            self._gerar_relatorio_excel(metricas)
            
            # Gera insights usando o orquestrador
            insights = self.analysis_orchestrator.process_customer_data(self.data, self.faturamento)
            
            # Salva insights em uma nova aba do relatório
            with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl', mode='a') as writer:
                # Insights da base de clientes
                df_insights_clientes = pd.DataFrame([
                    {"Tipo": "Distribuição Geográfica", "Insight": insight}
                    for insight in insights['customer_analysis']['insights']
                ])
                df_insights_clientes.to_excel(writer, sheet_name='Insights - Clientes', index=False)
                
                # Insights de faturamento
                df_insights_faturamento = pd.DataFrame([
                    {"Tipo": "Faturamento", "Insight": insight}
                    for insight in insights['revenue_analysis']['insights']
                ])
                df_insights_faturamento.to_excel(writer, sheet_name='Insights - Faturamento', index=False)
                
                # Insights estratégicos
                df_insights_estrategicos = pd.DataFrame([
                    {"Tipo": "Oportunidades", "Insight": insight}
                    for insight in insights['strategic_insights']['oportunidades']
                ] + [
                    {"Tipo": "Riscos", "Insight": insight}
                    for insight in insights['strategic_insights']['riscos']
                ] + [
                    {"Tipo": "Recomendações", "Insight": insight}
                    for insight in insights['strategic_insights']['recomendacoes']
                ])
                df_insights_estrategicos.to_excel(writer, sheet_name='Insights - Estratégicos', index=False)
            
            return "Dados processados com sucesso\nRelatório Excel gerado com métricas e insights"
            
        except Exception as e:
            logging.error(f"Erro ao processar dados: {str(e)}")
            return f"Erro: {str(e)}"

    def _calcular_metricas(self):
        """Calcula métricas básicas"""
        try:
            # Lista para armazenar as métricas
            metricas_list = []
            
            # Função auxiliar para calcular métricas por origem
            def calcular_metricas_origem(df_clientes, df_faturamento, origem=None):
                total_clientes = len(df_clientes)
                
                # Agrupa faturamento por cliente
                fat_por_cliente = df_faturamento.groupby('Cliente').agg({
                    'valor_total': 'sum'
                }).reset_index()
                
                clientes_unicos = len(fat_por_cliente[fat_por_cliente['valor_total'] > 0])
                fat_total = fat_por_cliente['valor_total'].sum()
                
                return {
                    'Origem': 'Total' if origem is None else origem,
                    'Total Clientes': total_clientes,
                    'Clientes Ativos': clientes_unicos,
                    'Percentual Ativos': (clientes_unicos/total_clientes*100) if total_clientes > 0 else 0,
                    'Faturamento Total': fat_total,
                    'Ticket Médio': fat_total/clientes_unicos if clientes_unicos > 0 else 0
                }
            
            # Calcula métricas totais
            metricas_list.append(calcular_metricas_origem(self.data, self.faturamento))
            
            # Calcula métricas por origem
            for origem in ['AMBEV', 'E-COMMERCE']:
                # Filtra dados por origem
                clientes_origem = self.data[self.data['ORIGEM'] == origem]
                clientes_origem_list = clientes_origem['CLIENTE'].tolist()
                fat_origem = self.faturamento[self.faturamento['Cliente'].isin(clientes_origem_list)]
                
                # Calcula métricas desta origem
                metricas_list.append(calcular_metricas_origem(clientes_origem, fat_origem, origem))
            
            # Converte lista de métricas para DataFrame
            return pd.DataFrame(metricas_list)
            
        except Exception as e:
            logging.error(f"Erro ao calcular métricas: {str(e)}")
            raise

    def _gerar_kpis_automaticos(self):
        """Gera KPIs automáticos baseados nos dados disponíveis"""
        try:
            kpis = {}
            
            # KPIs por Estado
            estados = self.data.groupby('UF').agg({
                'CLIENTE': 'count',
                'Limite Global': 'mean'
            }).reset_index()
            estados.columns = ['UF', 'Total Clientes', 'Limite Médio']
            estados = estados.sort_values('Total Clientes', ascending=False)  # Ordena por total de clientes
            kpis['KPIs por Estado'] = estados
            
            # KPIs por Categoria de Produto
            categorias = self.faturamento.groupby('Categoria').agg({
                'Cliente': 'nunique',
                'valor_total': 'sum'
            }).reset_index()
            categorias.columns = ['Categoria', 'Clientes Únicos', 'Faturamento Total']
            categorias['Ticket Médio'] = categorias['Faturamento Total'] / categorias['Clientes Únicos']
            categorias = categorias.sort_values('Clientes Únicos', ascending=False)  # Ordena por clientes únicos
            kpis['KPIs por Categoria'] = categorias
            
            return kpis
            
        except Exception as e:
            logging.error(f"Erro ao gerar KPIs automáticos: {str(e)}")
            raise

    def _gerar_relatorio_excel(self, metricas):
        """Gera relatório Excel com dados e insights"""
        try:
            writer = pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl')
            
            # Debug das métricas recebidas
            logging.debug("Métricas recebidas:")
            logging.debug(metricas)
            logging.debug(f"Tipo das métricas: {type(metricas)}")
            
            # Salva aba de Métricas por Origem
            try:
                metricas_pivot = metricas.melt(
                    id_vars=['Origem'],
                    var_name='Métrica',
                    value_name='Valor'
                )
                logging.debug("Após melt:")
                logging.debug(metricas_pivot)
                
                metricas_pivot = metricas_pivot.pivot(
                    index='Métrica',
                    columns='Origem',
                    values='Valor'
                )
                logging.debug("Após pivot:")
                logging.debug(metricas_pivot)
                
                metricas_pivot = metricas_pivot.reset_index()
                logging.debug("Após reset_index:")
                logging.debug(metricas_pivot)
                
                metricas_pivot.to_excel(writer, sheet_name='Métricas por Origem', index=False)
                logging.debug("Métricas salvas com sucesso")
                
            except Exception as e:
                logging.error(f"Erro ao processar métricas: {str(e)}")
                raise
            
            # Gera e salva KPIs automáticos em novas abas
            try:
                kpis = self._gerar_kpis_automaticos()
                for nome_aba, df_kpi in kpis.items():
                    df_kpi.to_excel(writer, sheet_name=nome_aba, index=False)
                logging.debug("KPIs automáticos salvos com sucesso")
                
            except Exception as e:
                logging.error(f"Erro ao gerar KPIs automáticos: {str(e)}")
                # Continua mesmo se houver erro nos KPIs automáticos
            
            # Salva o arquivo
            writer.close()
            logging.info(f"Relatório salvo com sucesso em '{OUTPUT_FILE}'")
            
        except Exception as e:
            logging.error(f"Erro ao gerar relatório Excel: {str(e)}")
            raise