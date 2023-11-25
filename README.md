# cupcakestore
Cupcake Ecommerce Project 

# Para rodar localmente
Tenha o python e git instalado e configurado adequadamente em sua máquina.

1. Clone o repositório:
```bash
$ git clone https://github.com/MariliaMJ/cupcakestore
```
2. Crie seu virtual environment:
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```
3. Instale os requirements:
```bash
$ pip install -r requirements.txt
```
4. Rode as migrações:
```bash
$ python manage.py makemigrations
$ python manage.py migrate
``````
5. Crie um superuser:
```bash
$ python manage.py createsuperuser
```
6. Rode o projeto:
```bash
$ python manage.py runserver
``````