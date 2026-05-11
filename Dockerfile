FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

# Expõe uma porta para o Render não reclamar
EXPOSE 8080

# Mantém o processo rodando com um servidor simples (opcional)
CMD python -c "import time; exec(open('bot.py').read())" &
CMD while true; do sleep 1; done
