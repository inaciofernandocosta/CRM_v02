import os
import logging
import warnings
import pandas as pd

# Suprimir avisos específicos do openpyxl
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def tratar_faturamento():
    """
    Trata o arquivo de faturamento para manter apenas clientes que existem na base.
    """
    try:
        # Define caminhos dos arquivos
        input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
        fat_file = os.path.join(input_dir, 'BD dash.xlsx')
        base_file = os.path.join(input_dir, 'Base_de_clientes_V4.xlsx')
        output_file = os.path.join(input_dir, 'faturamento.xlsx')

        # Carrega os arquivos
        logger.info("Carregando arquivos...")
        faturamento = pd.read_excel(fat_file)
        base_clientes = pd.read_excel(base_file)

        # Remove a última linha (Total)
        logger.info("Removendo linha de total...")
        faturamento = faturamento[faturamento['Cliente'] != 'Total']

        # Filtra apenas clientes que existem na base
        logger.info("Filtrando clientes...")
        clientes_base = set(base_clientes['CLIENTE'])
        faturamento_filtrado = faturamento[faturamento['Cliente'].isin(clientes_base)]

        # Salva o arquivo tratado
        logger.info("Salvando arquivo tratado...")
        faturamento_filtrado.to_excel(output_file, index=False)
        
        # Log das métricas
        total_original = len(faturamento)
        total_filtrado = len(faturamento_filtrado)
        logger.info(f"Registros originais: {total_original}")
        logger.info(f"Registros após filtro: {total_filtrado}")
        logger.info(f"Registros removidos: {total_original - total_filtrado}")
        
        logger.info(f"Arquivo salvo com sucesso em: {output_file}")
        return True

    except Exception as e:
        logger.error(f"Erro ao tratar arquivo: {str(e)}")
        return False

if __name__ == '__main__':
    tratar_faturamento()
