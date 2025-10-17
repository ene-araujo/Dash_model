# ===============================
# Imagem base
# ===============================
FROM python:3.11.9-slim

# ===============================
# Variáveis de ambiente
# ===============================
ENV PORT=10000 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DASH_DEBUG_MODE=False

WORKDIR /app

# ===============================
# Instala dependências
# ===============================
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# ===============================
# Copia o código
# ===============================
COPY . .

# ===============================
# Comando de execução
# ===============================
# Usa main.py (que define layout e importa server)
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 120 main:server

