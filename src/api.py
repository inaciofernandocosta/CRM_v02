from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import traceback
from customer_crew import CustomerDataCrew
import os
from typing import Optional
import threading
import time

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado global do crew
crew_state = {
    "status": "idle",
    "start_time": None,
    "crew": None,
    "thread": None,
    "error": None,
    "stats": {
        "active_agents": 0,
        "completed_tasks": 0,
        "success_rate": 0,
        "average_time": "0m"
    }
}

def run_crew():
    try:
        logger.info("Iniciando execução do crew...")
        input_file = os.path.join(os.path.dirname(__file__), "..", "input", "Base_de_clientes_V4.xlsx")
        logger.info(f"Arquivo de entrada: {input_file}")
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
        
        crew_state["crew"] = CustomerDataCrew()
        logger.info("CustomerDataCrew inicializado")
        
        crew_state["stats"]["active_agents"] = len(crew_state["crew"].agents)
        logger.info(f"Número de agentes ativos: {crew_state['stats']['active_agents']}")
        
        result = crew_state["crew"].processar_dados(input_file)
        logger.info(f"Processamento concluído com resultado: {result}")
        
        crew_state["stats"]["completed_tasks"] += 1
        crew_state["stats"]["success_rate"] = 100
        crew_state["status"] = "idle"
        
    except Exception as e:
        error_msg = f"Erro na execução do crew: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        crew_state["status"] = "error"
        crew_state["error"] = str(e)

@app.get("/crew/status")
async def get_crew_status():
    logger.info(f"Status atual do crew: {crew_state['status']}")
    return {
        "status": crew_state["status"],
        "startTime": crew_state["start_time"],
        "error": crew_state["error"]
    }

@app.get("/crew/stats")
async def get_crew_stats():
    logger.info(f"Estatísticas do crew: {crew_state['stats']}")
    return crew_state["stats"]

@app.post("/crew/start")
async def start_crew():
    logger.info("Requisição para iniciar o crew recebida")
    
    if crew_state["status"] == "running":
        logger.warning("Tentativa de iniciar crew que já está rodando")
        raise HTTPException(status_code=400, detail="Crew is already running")
    
    try:
        crew_state["status"] = "running"
        crew_state["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        crew_state["error"] = None
        
        logger.info("Iniciando thread do crew")
        thread = threading.Thread(target=run_crew)
        thread.start()
        crew_state["thread"] = thread
        
        logger.info("Crew iniciado com sucesso")
        return {"status": "started"}
        
    except Exception as e:
        error_msg = f"Erro ao iniciar crew: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        crew_state["status"] = "error"
        crew_state["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crew/stop")
async def stop_crew():
    logger.info("Requisição para parar o crew recebida")
    
    if crew_state["status"] != "running":
        logger.warning("Tentativa de parar crew que não está rodando")
        raise HTTPException(status_code=400, detail="Crew is not running")
    
    try:
        if crew_state["crew"]:
            logger.info("Parando o crew")
            # Implementar lógica de parada do crew
            crew_state["status"] = "idle"
            crew_state["error"] = None
            logger.info("Crew parado com sucesso")
        return {"status": "stopped"}
    except Exception as e:
        error_msg = f"Erro ao parar crew: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        crew_state["status"] = "error"
        crew_state["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))
