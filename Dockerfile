# -------- Dockerfile --------
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar restante do código, inclusive a pasta static
COPY . .

# Render passará PORT; se rodar localmente usa 8080
ENV PORT=8080
EXPOSE ${PORT}

# servidor WSGI em primeiro plano
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
