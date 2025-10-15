# Dockerfile
FROM python:3.11.9-slim

# Variáveis de ambiente
ENV PORT 10000
WORKDIR /app

# Copia e instala o requirements.txt primeiro para otimizar cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto
COPY . .

# Comando de inicialização do servidor Gunicorn
# Usa 'app:server' porque o objeto 'server' está definido no app.py
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 app:server
