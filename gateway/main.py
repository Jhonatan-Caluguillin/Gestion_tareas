# gateway/main.py
from fastapi import FastAPI
import httpx

app = FastAPI(title="API Gateway")

# USAMOS LOS NOMBRES DE LOS SERVICIOS DE DOCKER COMPOSE
# En lugar de localhost, Docker asocia estos nombres con las IPs internas de los contenedores
USERS_SERVICE_URL = "http://users_service:8001"
TASKS_SERVICE_URL = "http://tasks_service:8002"

@app.get("/")
def read_root():
    return {"message": "Bienvenido al API Gateway"}

@app.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        # Redirige la petición internamente al contenedor de usuarios
        response = await client.get(f"{USERS_SERVICE_URL}/")
        return response.json()

@app.get("/tasks")
async def get_tasks():
    async with httpx.AsyncClient() as client:
        # Redirige la petición internamente al contenedor de tareas
        response = await client.get(f"{TASKS_SERVICE_URL}/")
        return response.json()