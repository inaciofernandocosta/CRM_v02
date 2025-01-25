import logging
import pandas as pd
from typing import Dict, Any, List
import os

class AnalysisOrchestrator:
    """
    Orquestrador que coordena os diferentes agentes de análise.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_customer_base(self, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analisa a base de clientes em detalhes.
        """
        insights = {
            'distribuicao_geografica': {},
            'qualidade_dados': {},
            'segmentacao': {},
            'insights': []
        }
        
        # Análise geográfica
        dist_estados = customer_data['UF'].value_counts()
        top_estados = dist_estados.head()
        insights['distribuicao_geografica'] = {
            'total_estados': len(dist_estados),
            'estados_principais': top_estados.to_dict(),
            'concentracao': f"{(top_estados.sum() / len(customer_data) * 100):.1f}% dos clientes em {len(top_estados)} estados"
        }
        
        # Qualidade dos dados
        campos_importantes = ['CLIENTE', 'CNPJ/CPF', 'E-MAIL', 'LOGRADOURO', 'CEP']
        completude = {campo: (customer_data[campo].notna().sum() / len(customer_data) * 100) 
                     for campo in campos_importantes}
        insights['qualidade_dados'] = {
            'completude': completude,
            'campos_criticos': [campo for campo, valor in completude.items() if valor < 90]
        }
        
        # Segmentação por origem
        seg_origem = customer_data['ORIGEM'].value_counts()
        insights['segmentacao'] = {
            'distribuicao_origem': seg_origem.to_dict(),
            'proporcao': f"AMBEV: {(seg_origem.get('AMBEV', 0)/len(customer_data)*100):.1f}%, E-commerce: {(seg_origem.get('E-COMMERCE', 0)/len(customer_data)*100):.1f}%"
        }
        
        # Insights gerais
        insights['insights'].extend([
            f"Concentração geográfica em {len(top_estados)} estados principais",
            f"Campos com dados incompletos: {', '.join(insights['qualidade_dados']['campos_criticos'])}",
            f"Distribuição entre canais: {insights['segmentacao']['proporcao']}"
        ])
        
        return insights
    
    def analyze_revenue_patterns(self, revenue_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analisa padrões de faturamento.
        """
        insights = {
            'metricas_gerais': {},
            'tendencias': {},
            'categorias': {},
            'insights': []
        }
        
        # Métricas gerais
        fat_total = revenue_data['valor_total'].sum()
        clientes_unicos = revenue_data['Cliente'].nunique()
        insights['metricas_gerais'] = {
            'faturamento_total': fat_total,
            'clientes_unicos': clientes_unicos,
            'ticket_medio': fat_total / clientes_unicos if clientes_unicos > 0 else 0
        }
        
        # Análise por categoria
        fat_categoria = revenue_data.groupby('Categoria').agg({
            'Cliente': 'nunique',
            'valor_total': 'sum'
        }).reset_index()
        fat_categoria['ticket_medio'] = fat_categoria['valor_total'] / fat_categoria['Cliente']
        
        top_categorias = fat_categoria.nlargest(5, 'valor_total')
        insights['categorias'] = {
            'total_categorias': len(fat_categoria),
            'top_categorias': top_categorias.to_dict('records'),
            'concentracao': f"{(top_categorias['valor_total'].sum() / fat_total * 100):.1f}% do faturamento em 5 categorias"
        }
        
        # Análise temporal
        colunas_semanas = [col for col in revenue_data.columns if col.startswith('fat_semana_')]
        fat_semanal = pd.DataFrame({
            'semana': range(len(colunas_semanas)),
            'faturamento': [revenue_data[col].sum() for col in colunas_semanas]
        })
        
        tendencia = 'crescente' if fat_semanal['faturamento'].iloc[-1] > fat_semanal['faturamento'].iloc[0] else 'decrescente'
        variacao = ((fat_semanal['faturamento'].iloc[-1] / fat_semanal['faturamento'].iloc[0] - 1) * 100)
        
        insights['tendencias'] = {
            'tendencia_geral': tendencia,
            'variacao_percentual': f"{variacao:.1f}%",
            'faturamento_semanal': fat_semanal.to_dict('records')
        }
        
        # Insights gerais
        insights['insights'].extend([
            f"Faturamento total de R$ {fat_total:,.2f} com {clientes_unicos} clientes únicos",
            f"Ticket médio geral de R$ {insights['metricas_gerais']['ticket_medio']:,.2f}",
            f"Tendência {tendencia} com variação de {variacao:.1f}% no período",
            f"Concentração de faturamento: {insights['categorias']['concentracao']}"
        ])
        
        return insights
    
    def generate_strategic_insights(self, customer_insights: Dict[str, Any], revenue_insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera insights estratégicos combinando análises de clientes e faturamento.
        """
        strategic_insights = {
            'oportunidades': [],
            'riscos': [],
            'recomendacoes': []
        }
        
        # Análise de oportunidades
        if customer_insights['qualidade_dados']['campos_criticos']:
            strategic_insights['oportunidades'].append(
                "Melhorar qualidade dos dados para possibilitar ações mais direcionadas"
            )
        
        if float(revenue_insights['tendencias']['variacao_percentual'].rstrip('%')) > 0:
            strategic_insights['oportunidades'].append(
                f"Aproveitar tendência de crescimento ({revenue_insights['tendencias']['variacao_percentual']})"
            )
        
        # Análise de riscos
        concentracao_geo = float(customer_insights['distribuicao_geografica']['concentracao'].split('%')[0])
        if concentracao_geo > 70:
            strategic_insights['riscos'].append(
                f"Alta concentração geográfica ({concentracao_geo:.1f}% dos clientes)"
            )
        
        # Recomendações estratégicas
        strategic_insights['recomendacoes'].extend([
            "Desenvolver plano de expansão geográfica para reduzir concentração",
            "Implementar programa de enriquecimento de dados dos clientes",
            f"Focar em categorias top 5 que representam {revenue_insights['categorias']['concentracao']}"
        ])
        
        return strategic_insights
    
    def process_customer_data(self, customer_data: pd.DataFrame, revenue_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Processa os dados dos clientes e gera relatório completo.
        """
        try:
            # 1. Análise da base de clientes
            self.logger.info("Iniciando análise da base de clientes...")
            customer_insights = self.analyze_customer_base(customer_data)
            self.logger.info("Análise da base de clientes concluída")
            
            # 2. Análise de faturamento
            self.logger.info("Iniciando análise de faturamento...")
            revenue_insights = self.analyze_revenue_patterns(revenue_data)
            self.logger.info("Análise de faturamento concluída")
            
            # 3. Geração de insights estratégicos
            self.logger.info("Gerando insights estratégicos...")
            strategic_insights = self.generate_strategic_insights(customer_insights, revenue_insights)
            self.logger.info("Insights estratégicos gerados")
            
            # 4. Consolida resultados
            report = {
                'customer_analysis': customer_insights,
                'revenue_analysis': revenue_insights,
                'strategic_insights': strategic_insights
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Erro ao processar dados: {str(e)}")
            raise
