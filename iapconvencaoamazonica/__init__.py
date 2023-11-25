from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
import os
import sqlalchemy


app = Flask(__name__)
ckeditor = CKEditor(app)

if os.getenv('DATABASE_URL'):
    URL_DB = os.getenv('DATABASE_URL')
    nova_URL = URL_DB.replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_DATABASE_URI'] = nova_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iap_amazonica.db'

app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['SECRET_KEY'] = '60cc737479829f9462369024bee383ce'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from iapconvencaoamazonica import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de dados criado")
else:
    print("Base de dados já existente")

from iapconvencaoamazonica import routes
