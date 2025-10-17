# ===== Dockerfile =====
FROM python:3.11.9-slim

# Configura ambiente
ENV PORT=10000
WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Expõe a porta
EXPOSE 10000

# Executa o app com Gunicorn (modo produção)
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 main:app.server
