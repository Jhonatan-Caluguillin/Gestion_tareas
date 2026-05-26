# tasks_service/database.py
import os
import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


# 1. Variables de conexión separadas para poder maniobrar
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "postgres_db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = "tasks_db"

# URL final para SQLAlchemy
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Función para asegurar que la base de datos existe antes de que SQLAlchemy haga su magia
def build_database_sync():
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    # Nos conectamos a la base de datos por defecto 'postgres' usando una conexión síncrona simple
    try:
        conn = psycopg2.connect(
            dbname='postgres', 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificamos si existe tasks_db
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}';")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"¡La base de datos {DB_NAME} no existe! Creándola ahora mismo...", flush=True)
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Esperando a que Postgres despierte... {e}", flush=True)

# Ejecutamos el chequeo nativo antes de inicializar el motor
import time
# Le damos 3 segundos al contenedor de postgres para que acepte conexiones de red antes del chequeo
time.sleep(3) 
build_database_sync()

# Ahora sí, creamos el motor asíncrono con total seguridad de que la DB existe
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()