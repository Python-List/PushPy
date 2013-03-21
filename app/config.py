import os
dbhost= 'localhost'
dbuser= 'root'
dbpass= ''
dbname= ''
DB_URI= 'mysql://'+ dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname
CSRF_ENABLED = True
SECRET_KEY = '0B137449663DACC4C92289E8867CBEE7A2915B4975B013CA3DC187F14AF0B800'
basedir = os.path.abspath(os.path.dirname(__file__))
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' }]
