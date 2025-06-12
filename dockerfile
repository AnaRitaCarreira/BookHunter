# Imagem base Python slim para menor tamanho
FROM python:3.10-slim

# Atualiza pacotes e instala dependências para Chrome + Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
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
    --no-install-recommends

# Instala Google Chrome Stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y google-chrome-stable

# Baixa e instala chromedriver (verifique a versão compatível com seu Chrome)
ENV CHROME_DRIVER_VERSION 114.0.5735.90
RUN wget -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
 && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ \
 && rm /tmp/chromedriver_linux64.zip \
 && chmod +x /usr/local/bin/chromedriver

# Define diretório de trabalho
WORKDIR /app

# Copia requirements.txt e instala dependências Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Define variável para o Chrome binário
ENV CHROME_BIN=/usr/bin/google-chrome-stable

# Comando padrão para rodar seu script
CMD ["python", "main.py"]
