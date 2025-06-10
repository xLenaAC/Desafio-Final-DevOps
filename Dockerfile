# Usar imagem oficial do Python
FROM python:3.11-slim

# Definir variáveis de ambiente para Flask (opcional, pode ser feito no run/compose)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=1313
# ENV FLASK_ENV=production # Descomente para uma imagem de produção

# Criar diretório de trabalho
WORKDIR /app

# Copiar primeiro o requirements.txt para aproveitar o cache do Docker
COPY requirements.txt requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto para o container
# Certifique-se de ter um .dockerignore para não copiar arquivos desnecessários (venv, .git, etc.)
COPY . .

# Expor a porta usada pelo Flask/Gunicorn
EXPOSE 1313

# Comando para rodar a aplicação
# Para desenvolvimento (usando o servidor Flask):
CMD ["flask", "run"]
# Para produção (usando Gunicorn, como no Procfile):
# CMD ["gunicorn", "--bind", "0.0.0.0:1313", "app:app"]
# Escolha um CMD. Para uma imagem de produção, o gunicorn é o ideal.
# Se este Dockerfile é para CI/CD que deploya em algo que usa Procfile (ex: Heroku),
# o CMD pode não ser tão crítico, mas é bom ter um default sensato.
# Para o pipeline que montamos antes (deploy em EC2), o CMD com gunicorn seria melhor.
