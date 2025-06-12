FROM zenika/alpine-chrome:with-node

# Instala o Python e pip (alpine usa apk)
RUN apk add --no-cache python3 py3-pip

WORKDIR /app

# Copia requirements e instala libs Python
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia seu código
COPY . .

# Define variável ambiente para o binário do chrome (já vem nessa imagem)
ENV CHROME_BIN=/usr/bin/chromium-browser

# Comando padrão
CMD ["python3", "main.py"]
