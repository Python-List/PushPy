import os
from flask import Flask,redirect,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_openid import OpenID
from config import basedir
from datetime import timedelta
import config
from config import adminusers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= config.DB_URI
app.config['SECRET_KEY']=config.SECRET_KEY
app.config['CSRF_ENABLED']=config.CSRF_ENABLED
app.config['OPENID_PROVIDERS']=config.OPENID_PROVIDERS
db = SQLAlchemy(app)

#Creamos el Login Manager
lm = LoginManager()
lm.setup_app(app)
lm.refresh_view = 'login'
app.config['REMEMBER_COOKIE_DURATION']=timedelta(minutes=2)
lm.needs_refresh_message = (
    u"Para proteger el acceso por favor inicia sesion de nuevo"
    )
lm.session_protection = "strong"

#Creamos el Openid
oid = OpenID(app, os.path.join(basedir, 'tmp'))


#Definimos el decorador que devuelve el usuario en caso de que exista
@lm.user_loader
def load_user(id):
    return model.adminUser.query.get(int(id))
@lm.needs_refresh_handler
def refresh():
    # do stuff
    return redirect(url_for('login'))

import model
from app import views
