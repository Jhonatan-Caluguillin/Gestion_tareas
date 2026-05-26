FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn

# Copiamos los archivos manteniendo sus nombres reales
COPY database.py .
COPY main.py .

EXPOSE 8001

# Ejecutamos apuntando a main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]