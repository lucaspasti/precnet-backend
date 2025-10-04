# Imagem base leve do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala libs do sistema necessárias para pdfplumber e Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \   
    libxslt-dev \
    libjpeg-dev \
    libz-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Cria diretório para uploads
RUN mkdir -p uploads

ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONUNBUFFERED=1

# Expõe a porta Flask
EXPOSE 5000

# Comando padrão
CMD ["flask", "run"]
