FROM python:3.10-slim

# Instala dependências necessárias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libxext6 \
    libxfixes3 \
    libglib2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Cria pasta de cache do Chrome
ENV STORAGE_DIR=/opt/render/project/.render
RUN mkdir -p $STORAGE_DIR/chrome

# Baixa e extrai Google Chrome (sem instalar via dpkg)
RUN cd $STORAGE_DIR/chrome && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -x google-chrome-stable_current_amd64.deb . && \
    rm google-chrome-stable_current_amd64.deb

# Adiciona Chrome extraído ao PATH
ENV PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"
ENV CHROME_BIN="/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"

# Define diretório de trabalho
WORKDIR /app

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia seu código
COPY . .

# Comando padrão
CMD ["python", "main.py"]
