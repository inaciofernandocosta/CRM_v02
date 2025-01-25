import uvicorn
from api import app

if __name__ == "__main__":
    # Configuração do Uvicorn para desenvolvimento
    uvicorn.run(
        app,
        host="127.0.0.1",  # Localhost
        port=8000,
        reload=True,  # Auto-reload em desenvolvimento
        log_level="debug"
    )
