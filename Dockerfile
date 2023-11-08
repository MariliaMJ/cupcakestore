# Use a image base Python
FROM python:3.8

# Crie e defina o diretório de trabalho no contêiner
WORKDIR /cupcakeapp

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o código fonte para o contêiner
COPY . /cupcakeapp

# Defina as variáveis de ambiente
ENV DJANGO_SETTINGS_MODULE=cupcakestore.settings

# Exponha a porta em que o Django estará em execução
EXPOSE 8000

# Inicie o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
