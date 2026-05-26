from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="API Gateway")

# Direcciones internas de Docker Compose
USERS_SERVICE_URL = "http://users_service:8001"
TASKS_SERVICE_URL = "http://tasks_service:8002"

@app.get("/")
def read_root():
    return {"message": "Bienvenido al API Gateway"}

# ==========================================
#          RUTAS DE USUARIOS (USERS)
# ==========================================

# 1. Listar usuarios (Read)
@app.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USERS_SERVICE_URL}/")
        return response.json()

# 2. Crear usuario (Create)
@app.post("/users/create")
async def create_user(username: str, role: str = "user"):
    async with httpx.AsyncClient() as client:
        # Pasamos los parámetros como query params hacia el microservicio
        response = await client.post(f"{USERS_SERVICE_URL}/create-user", params={"username": username, "role": role})
        return response.json()

# 3. Obtener un usuario por ID (Read)
@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USERS_SERVICE_URL}/users/{user_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en el sistema")
        return response.json()

# 4. Actualizar usuario (Update)
@app.put("/users/update/{user_id}")
async def update_user(user_id: int, username: str, role: str):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{USERS_SERVICE_URL}/update-user/{user_id}", params={"username": username, "role": role})
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return response.json()

# 5. Eliminar usuario (Delete)
@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USERS_SERVICE_URL}/delete-user/{user_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return response.json()


# ==========================================
#          RUTAS DE TAREAS (TASKS)
# ==========================================

# 1. Listar todas las tareas (Read)
@app.get("/tasks")
async def get_tasks():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TASKS_SERVICE_URL}/")
        return response.json()

# 2. Crear tarea (Create)
@app.post("/tasks/create")
async def create_task(title: str, description: str, user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TASKS_SERVICE_URL}/create-task", 
            params={"title": title, "description": description, "user_id": user_id}
        )
        return response.json()

# 3. Obtener una tarea por ID (Read)
@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TASKS_SERVICE_URL}/tasks/{task_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return response.json()

# 4. Actualizar tarea (Update)
@app.put("/tasks/update/{task_id}")
async def update_task(task_id: int, title: str, description: str, status: str):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{TASKS_SERVICE_URL}/update-task/{task_id}", 
            params={"title": title, "description": description, "status": status}
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return response.json()

# 5. Eliminar tarea (Delete)
@app.delete("/tasks/delete/{task_id}")
async def delete_task(task_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{TASKS_SERVICE_URL}/delete-task/{task_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return response.json()