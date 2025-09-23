FROM python:3.11-slim

WORKDIR /app

# Instalar dependências básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    pkg-config \
    curl \
    gnupg \
    dirmngr \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    g++ \
    make \
    python3-dev \
    libffi-dev \
 && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list \


 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
 && rm -rf /var/lib/apt/lists/*


# Copiar código
COPY . /app

# Instalar dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe porta
EXPOSE 8000

# Rodar Django + migrações + Gunicorn
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]

