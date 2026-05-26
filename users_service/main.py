from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select
from database import Base, engine, get_db

app = FastAPI(title="Users Service con DB")

# Definición de la tabla de Usuarios
class UserTable(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[str] = mapped_column(default="user")

# Evento para crear las tablas automáticamente al encender el servicio
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Esto crea la tabla si no existe en la DB
        await conn.run_sync(Base.metadata.create_all)

# 1. READ (Listar todos)
@app.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable))
    users = result.scalars().all()
    return {"service": "Users Service", "users": users}

# 2. CREATE (Crear usuario)
@app.post("/create-user")
async def create_user(username: str, role: str = "user", db: AsyncSession = Depends(get_db)):
    new_user = UserTable(username=username, role=role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "Usuario creado con éxito", "user": new_user}

# 3. READ (Buscar por ID específico)
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).filter(UserTable.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# 4. UPDATE (Actualizar datos de usuario)
@app.put("/update-user/{user_id}")
async def update_user(user_id: int, username: str, role: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).filter(UserTable.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_user.username = username
    db_user.role = role
    await db.commit()
    await db.refresh(db_user)
    return {"message": "Usuario actualizado con éxito", "user": db_user}

# 5. DELETE (Eliminar usuario)
@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).filter(UserTable.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    await db.delete(db_user)
    await db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado correctamente"}
