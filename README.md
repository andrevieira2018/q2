# q2
 
Desafio Quero Educação - Cloud Intern
 
## Antes de começar
 
Você tem 5 dias após o recebimento do desafio para completá-lo. Use um repositório privado no Gitlab.
 
## Questão
 
Na pasta q2 temos uma aplicação web escrita em Python que contém um formulário. Quando o form é enviado, a aplicação salva as infos em um banco Postgres.
 
### Observações
 
- Aplicação exposta na porta 80 ou 443
- Existem alguns bugs na aplicação e para corrigi-los você não precisa de nenhum conhecimento específico em Python
- Se fizer alguma mudança para te ajudar no debug, sugerimos mantê-las para entender sua linha de raciocínio
- Se tiver algum conhecimento em Python e quiser melhorar o código, fique à vontade
 
### Solução
 
- Use Kubernetes de preferência ou Docker Compose para orquestração local
- Escreva uma documentação como se fosse para novatos
 
## Submissão
 
- Mantenha o enunciado das questões no seu README.md
- Não coloque todas as alterações em um único commit, porque queremos ver sua linha de raciocínio e organização
- Dê acesso com permissão de repórter para o grupo `quero-cloud` no seu repositório privado do Gitlab
- Avise o recrutador da Quero
 
##### INICIANDO APP FLASK - SQL - PYTHON - NGINX
Preparando o ambiente, será necessário a instalação dos pacotes docker e docker-compose de acordo com sua distribuição linux, recomendo a instalação do sistema CoreOS que é próprio para ambiente de containers.
 
Após o ambiente pré-configurado é hora de realizar a criação de fato do ambiente DEVE primeiramente necessário realizar a criação de alguns arquivos e diretórios como:
 
[andre@andre-pc compose-flask]$ ls -R
.:
app.py  database.py         Dockerfile  forms.py   __pycache__  requirements.txt
conf.d  docker-compose.yml  env_file    models.py  README.md    templates
 
./conf.d:
flask app.conf
 
./_ pycache _:
database.python-38.pyc  forms.python-38.pyc  models.python-38.pyc
 
./templates:
signup.html  success.html
 
--------------------------------------------------------------------------------------------------------------------------
 
-`app.py` -> Referente a sua aplicacao o codigo.
 
import datetime
import os
 
from flask import Flask, render_template, redirect, url_for
from forms import SignupForm
 
from models import Signups
from database import db_session
 
app = Flask(__name__)
app.secret_key = os.environ['APP SECRET_KEY']
 
@app.route("/", methods=('GET', 'POST'))
def signup():
    form = Signup Form()
    if form.validate _on_submit():
        sign up = Sign Ups(nome=form.nome.data, mensagem=form.mensagem.data, date signed up=datetime.datetime.now())
        db session.add(signup)
        db session.commit()
        return render_template('success.html')
        return render_template('signup.html', form=form)
        
@app.route('/')
def success():
    return render_template('success.html')
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
 
 
 
-`database.py` -> informacoes do banco de dados.
 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scope session, session maker
from sqlalchemy.ext.declarative import declarative_base
 
user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'
engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
 
db_ session = scoped session(session maker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative base()
Base.query = db_session.query_property()
 
def init db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create all(bind=engine)
 
 
-`Dockerfile`  -> Configurações do Ambiente Docker
 
FROM python:3
MAINTAINER Ameya Lokare <lokare.ameya@gmail.com>
 
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/flaskapp/src
#Criação do volume: VOLUME ["/opt/services/flaskapp/src"]
# Cópia e criação dos diretórios necessários para funcionamento da aplicação.
COPY requirements.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src
RUN pip install -r requirements.txt
COPY . /opt/services/flaskapp/src
EXPOSE 5090
CMD ["python", "app.py"]
 
 
-`forms.py`   -> Formulario da aplicacao.
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
 
class SignupForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    mensagem = StringField('mensagem', validators=[DataRequir
 
 
-`requirements.txt` -> Pacotes necessários para subir aplicação
Flask
psycopg2
SQLAlchemy
Flask-WTF
 
 
-`docker-compose.yml ` -> Configuração de imagem do container, informações de portas, volume, variáveis do ambiente.
version: '3'
services:
  db:
    image: "postgres:9.6.5"
    volumes:
      - "dbdata:/var/lib/postgresql/data"
    env_file:
      - env_file
    networks:
      - db_nw
  flaskapp:
    build: .
    env_file:
      - env_file
    volumes:
      - .:/opt/services/flaskapp/src
    networks:
      - db_nw
      - web_nw
    depends_on:
      - db
  nginx:
    image: "nginx:1.13.5"
    ports:
      - "80:80"
    volumes:
      - ./conf.d:/etc/nginx/conf.d
    networks:
      - web_nw
    depends_on:
      - flaskapp
networks:
  db_nw:
    driver: bridge
  web_nw:
    driver: bridge
volumes:
  dbdata:
 
-`env_file` -> Variáveis do ambiente como usuário do banco de dados e senhas.
POSTGRES_USER=postgres
POSTGRES_PASSWORD=USE_YOUR_PASSWORD
POSTGRES_DB=flaskapp_db
APP_SECRET_KEY=USE_YOUR_SECRET_KEY
 
 
-`models.py ` -> descricao dado que sera gerenciado pela aplicacao como atributos das classes como nome, endereço, id e entre outras configurações.
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime
 
class Signups(Base):
    """
    Example Signups table
    """
    __tablename__ = 'signups'
    id = Column(Integer, primary_key=True)
    nome = Column(String(256))
    mensagem = Column(String(256), unique=True)
    date_signed_up = Column(DateTime())
 
 
#Diretório: Necessário criar os seguinte diretórios: templates e conf.d
-`templates`
       |_ singup.html
          <!DOCTYPE html>
<html lang="en">
    <body>
        <h1> Seja bem-vindo nos envie sua mensagem !!! </h1>
        <form method="POST" action="/">
            {{ form.csrf_token }}
            {{ form.nome.label }} {{ form.nome(size=20) }}
            {{ form.mensagem.label }} {{ form.mensagem(size=40) }}
            <input type="submit" value="Enviar">
        </form>
    </body>
</html>
|_success.html
<!DOCTYPE html>
<html lang="en">
    <body>
        <h1> Enviado com sucesso !!!!</h1>
        <input type="button" value="Voltar" onClick="history.go(-1)">
        </form>
    </body>
</html>
 
        
-`conf.d`
     |_flaskapp.conf
server {
    listen 80;
    server_name localhost;
 
    location / {
        proxy_set_header   Host                 $host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
        proxy_set_header Host $http_host;
 
        proxy_pass http://flaskapp:5090;
    }
}
 
Após criação de todos os arquivos e diretórios, realizar o procedimento de criação das máquinas com os seguintes comandos no terminal linux.
# Observação este processo pode levar alguns minutos dependendo da sua 
 
Realizando o build ->conexão e máquina, aqui vai realizar o download de todas dependências e pacotes necessários para funcionamento da aplicação.
[andre@andre-pc compose-flask]$ docker-compose
db uses an image, skipping
nginx uses an image, skipping
Building flaskapp
Step 1/9 : FROM python:3
 ---> efdecc2e377a
Step 2/9 : ENV PYTHONUNBUFFERED 1
 ---> Running in 641e9aed6ad0
Removing intermediate container 641e9aed6ad0
 ---> a43a38644ad6
Step 3/9 : RUN mkdir -p /opt/services/flaskapp/src
 ---> Running in ebcfc1050a4a
Removing intermediate container ebcfc1050a4a
 ---> f9f14fdcb220
Step 4/9 : COPY requirements.txt /opt/services/flaskapp/src/
 ---> cbc677505f93
Step 5/9 : WORKDIR /opt/services/flaskapp/src
 ---> Running in bda645f36d13
Removing intermediate container bda645f36d13
 ---> 8ee944de5adb
Step 6/9 : RUN pip install -r requirements.txt
 ---> Running in 88a5264ad159
Collecting Flask
  Downloading Flask-1.1.1-py2.py3-none-any.whl (94 kB)
Collecting psycopg2
  Downloading psycopg2-2.8.4.tar.gz (377 kB)
Collecting SQLAlchemy
  Downloading SQLAlchemy-1.3.13.tar.gz (6.0 MB)
Collecting Flask-WTF
  Downloading Flask_WTF-0.14.3-py2.py3-none-any.whl (13 kB)
Collecting Werkzeug>=0.15
  Downloading Werkzeug-1.0.0-py2.py3-none-any.whl (298 kB)
Collecting Jinja2>=2.10.1
  Downloading Jinja2-2.11.1-py2.py3-none-any.whl (126 kB)
Collecting click>=5.1
  Downloading Click-7.0-py2.py3-none-any.whl (81 kB)
Collecting itsdangerous>=0.24
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting WTForms
  Downloading WTForms-2.2.1-py2.py3-none-any.whl (166 kB)
Collecting MarkupSafe>=0.23
  Downloading MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl (32 kB)
Building wheels for collected packages: psycopg2, SQLAlchemy
  Building wheel for psycopg2 (setup.py): started
  Building wheel for psycopg2 (setup.py): finished with status 'done'
  Created wheel for psycopg2: filename=psycopg2-2.8.4-cp38-cp38-linux_x86_64.whl size=498822 sha256=c4eae62a0def4181d8c47ab91ab0c43ab937ce2a3101ee8d657e74775ce8be73
  Stored in directory: /root/.cache/pip/wheels/ac/07/3e/87adc95a2be1ee727bc54f487ce874bd6765ec9f206effb0df
  Building wheel for SQLAlchemy (setup.py): started
  Building wheel for SQLAlchemy (setup.py): finished with status 'done'
  Created wheel for SQLAlchemy: filename=SQLAlchemy-1.3.13-cp38-cp38-linux_x86_64.whl size=1225498 sha256=30b1efa9aacd3d9ef5d1532fb8f4a81fb38b13ef7669279343c2fa6053e191af
  Stored in directory: /root/.cache/pip/wheels/1b/5b/fe/df3abf130f4f66b437ea92eb98814d9d9fa80d70a6ee080b96
Successfully built psycopg2 SQLAlchemy
Installing collected packages: Werkzeug, MarkupSafe, Jinja2, click, itsdangerous, Flask, psycopg2, SQLAlchemy, WTForms, Flask-WTF
Successfully installed Flask-1.1.1 Flask-WTF-0.14.3 Jinja2-2.11.1 MarkupSafe-1.1.1 SQLAlchemy-1.3.13 WTForms-2.2.1 Werkzeug-1.0.0 click-7.0 itsdangerous-1.1.0 psycopg2-2.8.4
Removing intermediate container 88a5264ad159
 ---> df9773002738
Step 7/9 : COPY . /opt/services/flaskapp/src
 ---> 63fca6f6dd09
Step 8/9 : EXPOSE 5090
 ---> Running in 6ed0204bb2ea
Removing intermediate container 6ed0204bb2ea
 ---> e8a269400b5a
Step 9/9 : CMD ["python", "app.py"]
 ---> Running in 5ee92b2e6c40
Removing intermediate container 5ee92b2e6c40
 ---> 832e0ab204e9
Successfully built 832e0ab204e9
Successfully tagged compose-flask_flaskapp:latest
# Após o build feito vamos subir o DB primeiro para que ele popule faca criação do banco e tabelas.
[andre@andre-pc compose-flask]$ docker-compose up -d db && docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"
# Por final rodar docker-compose up para debugar se caso ocorra algum erro podermos ver.
[andre@andre-pc compose-flask]$ docker-compose up
Creating network "compose-flask_db_nw" with driver "bridge"
Creating network "compose-flask_web_nw" with driver "bridge"
Creating compose-flask_db_1 ... done
Creating compose-flask_flaskapp_1 ... done
Creating compose-flask_nginx_1    ... done
Attaching to compose-flask_db_1, compose-flask_flaskapp_1, compose-flask_nginx_1
db_1        | LOG:  database system was shut down at 2020-02-14 20:23:29 UTC
flaskapp_1  |  * Serving Flask app "app" (lazy loading)
flaskapp_1  |  * Environment: production
db_1        | LOG:  MultiXact member wraparound protections are now enabled
flaskapp_1  |    WARNING: This is a development server. Do not use it in a production deployment.
flaskapp_1  |    Use a production WSGI server instead.
flaskapp_1  |  * Debug mode: on
flaskapp_1  |  * Running on http://0.0.0.0:5090/ (Press CTRL+C to quit)
db_1        | LOG:  database system is ready to accept connections
flaskapp_1  |  * Restarting with stat
db_1        | LOG:  autovacuum launcher started
flaskapp_1  |  * Debugger is active!
flaskapp_1  |  * Debugger PIN: 342-377-714
 
# Se tudo estiver ok, apresentará estas informações.
 
 
 


