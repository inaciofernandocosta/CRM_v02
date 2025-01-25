from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import yaml
import os
import sys
import pandas as pd
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime

# Adicionar o diretório src ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from customer_crew import run_crew

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Agent(BaseModel):
    name: str
    role: str
    goal: str
    status: str = "active"
    insights: List[str] = []
    progress: int = 0

# Armazenar resultados do crew
crew_results = {
    "status": "idle",  # idle, running, completed
    "start_time": None,
    "end_time": None,
    "results": None
}

@app.get("/agents", response_model=List[Agent])
async def get_agents():
    yaml_path = os.path.join(os.path.dirname(__file__), "..", "..", "src", "config", "agents.yaml")
    
    with open(yaml_path, 'r') as file:
        agents_data = yaml.safe_load(file)
    
    agents = []
    for agent_name, agent_info in agents_data.items():
        insights = []
        if "analysis" in agent_name.lower():
            insights = [
                "Identificou padrões importantes nos dados",
                "Gerou relatório de tendências",
                "Recomendações estratégicas baseadas em dados"
            ]
        elif "process" in agent_name.lower():
            insights = [
                "Processamento eficiente de arquivos",
                "Otimização do fluxo de trabalho",
                "Redução do tempo de processamento"
            ]
        
        # Definir progresso com base no status do crew
        progress = 100 if crew_results["status"] == "completed" else (
            50 if crew_results["status"] == "running" else 0
        )
        
        agent = Agent(
            name=agent_name,
            role=agent_info.get('role', ''),
            goal=agent_info.get('goal', ''),
            status="completed" if crew_results["status"] == "completed" else "active",
            insights=insights,
            progress=progress
        )
        agents.append(agent)
    
    return agents

@app.get("/crew/status")
async def get_crew_status():
    return crew_results

async def run_crew_task():
    global crew_results
    try:
        crew_results["status"] = "running"
        crew_results["start_time"] = datetime.now().isoformat()
        
        # Executar o crew e capturar resultados
        results = run_crew()
        
        crew_results["results"] = results
        crew_results["status"] = "completed"
        crew_results["end_time"] = datetime.now().isoformat()
    except Exception as e:
        crew_results["status"] = "error"
        crew_results["results"] = str(e)

@app.post("/start-crew")
async def start_crew(background_tasks: BackgroundTasks):
    global crew_results
    if crew_results["status"] == "running":
        return {"message": "Crew is already running"}
    
    # Resetar resultados
    crew_results = {
        "status": "idle",
        "start_time": None,
        "end_time": None,
        "results": None
    }
    
    # Iniciar crew em background
    background_tasks.add_task(run_crew_task)
    return {"message": "Crew started successfully"}

@app.get("/export/{format}")
async def export_results(format: str):
    if not crew_results["results"]:
        return {"error": "No results available to export"}
    
    data = crew_results["results"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format == "json":
        return {
            "data": data,
            "filename": f"crew_results_{timestamp}.json"
        }
    elif format == "csv":
        # Converter resultados para DataFrame e depois para CSV
        df = pd.DataFrame(data)
        csv_content = df.to_csv(index=False)
        return {
            "data": csv_content,
            "filename": f"crew_results_{timestamp}.csv"
        }
    elif format == "excel":
        # Converter resultados para DataFrame e depois para Excel
        df = pd.DataFrame(data)
        excel_path = f"/tmp/crew_results_{timestamp}.xlsx"
        df.to_excel(excel_path, index=False)
        return {
            "file_path": excel_path,
            "filename": f"crew_results_{timestamp}.xlsx"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
