# users_service/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# URL de conexión (Usa variables de entorno, clave para cuando usemos Docker y AWS)
# Por ahora toma un valor por defecto local si no existe la variable
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@localhost:5432/users_db"
)

# Creamos el motor asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Creamos la fábrica de sesiones para las peticiones
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Clase base para nuestros modelos (tablas)
class Base(DeclarativeBase):
    pass

# Dependencia para inyectar la sesión en los endpoints de FastAPI
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()