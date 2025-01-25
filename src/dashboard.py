import streamlit as st
import yaml
import time
from datetime import datetime
import pandas as pd
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Agentes AI",
    page_icon="🤖",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .agent-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-inactive {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def load_agents_config():
    """Carrega a configuração dos agentes do arquivo YAML"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'agents.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Erro ao carregar configuração dos agentes: {str(e)}")
        return {}

def display_agent_card(agent_name, agent_config, col):
    """Exibe o card de um agente"""
    with col:
        st.markdown(f"""
        <div class="agent-card">
            <h3>{agent_config.get('name', agent_name)}</h3>
            <p><strong>Função:</strong> {agent_config.get('role', 'N/A')}</p>
            <p><strong>Objetivo:</strong> {agent_config.get('goal', 'N/A')}</p>
            <p class="status-active">Status: Ativo</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.title("🤖 Dashboard de Agentes AI")
    
    # Carrega configuração dos agentes
    agents_config = load_agents_config()
    
    if not agents_config:
        st.warning("Nenhuma configuração de agente encontrada.")
        return
    
    # Cria layout em grid para os agentes
    cols = st.columns(2)
    
    # Exibe cards dos agentes
    for i, (agent_name, agent_config) in enumerate(agents_config.items()):
        display_agent_card(agent_name, agent_config, cols[i % 2])
    
    # Área de logs e atividades
    st.subheader("📋 Log de Atividades")
    
    # Criação de alguns logs de exemplo
    activities = []
    current_time = datetime.now().strftime("%H:%M:%S")
    activities.append({
        "Horário": current_time,
        "Agente": "Cientista de Dados AI",
        "Ação": "Analisando dados de clientes..."
    })
    
    # Exibe a tabela de logs
    log_df = pd.DataFrame(activities)
    st.dataframe(log_df, hide_index=True)

if __name__ == "__main__":
    main()
