import os
dbname= 'pushpy'
DB_URI= 'sqlite:///'+ dbname + '.db'

CSRF_ENABLED = True
SECRET_KEY = ''
basedir = os.path.abspath(os.path.dirname(__file__))
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' }]

## Allowed users to send notifications ( using gmail accounts )
adminusers=[{'nickname':'nick1','email':'user@gmail.com'},
            ]