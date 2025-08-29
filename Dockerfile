FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema necessárias para mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta padrão
EXPOSE 8000

# Comando para iniciar com Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000","--workers 3" , "--timeout 120"]
