import os
import pandas as pd
from crewai import Task, Agent, Crew
from crewai.project import task

class CrewBase:
    def __init__(self):
        self.tasks = []
        self.agents = []

    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process='sequential')

class CustomerDataCrew(CrewBase):
    @task
    def process_customer_data_task(self) -> Task:
        def process_file(context):
            file_path = context.get("inputs", {}).get("file_path")
            if not file_path:
                return "Erro: Caminho do arquivo não foi fornecido."
            try:
                df = pd.read_excel(file_path)
            except FileNotFoundError:
                return f"Erro: Arquivo '{file_path}' não encontrado."

            if 'cliente' not in df.columns:
                return "Erro: Coluna 'cliente' não encontrada no arquivo."

            distinct_customers = df['cliente'].nunique()
            output_file = "/Users/fernandocosta/Documents/2025/Crew/V4/output/logs.xlsx"
            output_df = pd.DataFrame({'Clientes Distintos': [distinct_customers]})
            output_df.to_excel(output_file, index=False)

            return f"Processamento concluído. Clientes distintos: {distinct_customers}. Resultado salvo em '{output_file}'."

        return Task(description="Tarefa para processar clientes", execute=process_file)