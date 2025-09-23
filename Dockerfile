FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema (MySQL + SQL Server)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    pkg-config \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    g++ \
    make \
    python3-dev \
    libffi-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Copiar o código da aplicação
COPY . /app

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta padrão
EXPOSE 8000

# Comando para iniciar com Gunicorn
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]

