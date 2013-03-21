import os
dbhost= '127.0.0.1'
dbuser= 'root'
dbpass= 'mysql'
dbname= 'pushpy'
DB_URI= 'mysql://'+ dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname
#DBU_URI='sqlite:////absolute/path/to/database.txt'
CSRF_ENABLED = True
SECRET_KEY = ''
basedir = os.path.abspath(os.path.dirname(__file__))
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' }]
