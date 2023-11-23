from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)

app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['SECRET_KEY'] = '60cc737479829f9462369024bee383ce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iap_amazonica.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from iapconvencaoamazonica import routes
