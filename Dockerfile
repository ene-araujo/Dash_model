# Usa Python 3.11.9 slim como base (compatível com seu projeto)
FROM python:3.11.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements.txt para otimizar cache do Docker
COPY requirements.txt .

# Instala as dependências sem cache
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o container
COPY . .

# Comando de inicialização usando Gunicorn
# Importante: 'main:server' -> 'server' é o objeto Flask exposto no app.py
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 main:server
