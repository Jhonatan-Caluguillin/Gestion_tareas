from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select
from database import Base, engine, get_db

app = FastAPI(title="Tasks Service con DB")

# Definición de la tabla de Tareas
class TaskTable(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="pending")  # pending, in_progress, completed
    user_id: Mapped[int] = mapped_column(nullable=False)  # Relación conceptual con el id de usuario

# Evento para crear las tablas automáticamente al encender el servicio
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 1. READ (Listar todas las tareas)
@app.get("/")
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskTable))
    tasks = result.scalars().all()
    return {"service": "Tasks Service", "tasks": tasks}

# 2. CREATE (Crear una tarea)
@app.post("/create-task")
async def create_task(title: str, description: str, user_id: int, db: AsyncSession = Depends(get_db)):
    new_task = TaskTable(title=title, description=description, user_id=user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return {"message": "Tarea creada con éxito", "task": new_task}

# 3. READ (Buscar tarea por ID específico)
@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskTable).filter(TaskTable.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

# 4. UPDATE (Actualizar estado o información de la tarea)
@app.put("/update-task/{task_id}")
async def update_task(task_id: int, title: str, description: str, status: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskTable).filter(TaskTable.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db_task.title = title
    db_task.description = description
    db_task.status = status
    await db.commit()
    await db.refresh(db_task)
    return {"message": "Tarea actualizada con éxito", "task": db_task}

# 5. DELETE (Eliminar tarea)
@app.delete("/delete-task/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskTable).filter(TaskTable.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    await db.delete(db_task)
    await db.commit()
    return {"message": f"Tarea con ID {task_id} eliminada correctamente"}

    