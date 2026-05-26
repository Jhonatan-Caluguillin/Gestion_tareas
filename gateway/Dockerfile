FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
# Forzamos la instalación de fastapi, uvicorn y httpx directamente aquí
RUN pip install --no-cache-dir fastapi uvicorn httpx

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]