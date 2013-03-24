#!flask/bin/python
from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g
import datetime
from app import app,db,model,oid
from forms import LoginForm,SendPush
from flask_login import login_user, logout_user, current_user, login_required, fresh_login_required
from push import pushclass
import json
from config import adminusers
import threading

#Inicializamos la base de datos y creamos los usuarios
db.create_all()
dbadmins=model.adminUser.query.all()
for admin in dbadmins:
    db.session.delete(admin)
    db.session.commit()
for user in adminusers:
    print 'anyadiendo usuario'
    newAdmin= model.adminUser(nickname=user['nickname'],email=user['email'])
    db.session.add(newAdmin)
    db.session.commit()


def store_user(jsondata):
    try:
        udid=jsondata['udid']
        language=jsondata['language']
        push=jsondata['push']
        last=jsondata['last']
        token=None
        if jsondata.has_key('token'):
            if(jsondata['token'] is not None):
                token=jsondata['token']

        #Check if the user exists
        print 'Comprobamos si existe usuario con udid '+udid
        checkuser = model.User.query.filter_by(udid=udid).first()
        if checkuser is not None:
            print '>The user exists, update the data'
            checkuser.udid=udid
            checkuser.language=language
            checkuser.push=push
            checkuser.last=datetime.date.today()
            checkuser.token=token
            db.session.commit()
        else:
            print '>The user doesnt exists, create one'
            newuser  = model.User(udid=udid,language=language,push=push,last=last,token=token)
            db.session.add(newuser)
            db.session.commit()
    except:
        print '>Error: Impossible to store the user'

@app.before_request
def before_request():
    g.user = current_user

@app.route('/pushpy/push',methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        if g.user.is_authenticated():
            return redirect(url_for('sendpush'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = False
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template("login.html",
    content={'title':'Push notifications'},
    form=form,
    providers = app.config['OPENID_PROVIDERS']
    )
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Impossible to login without email')
        redirect(url_for('login'))
    print '>The user '+resp.email+' is trying to access'
    user = model.adminUser.query.filter_by(email = resp.email).first()
    if user is not None:
        login_user(user, remember=False)
        return redirect(url_for('sendpush'))
    print ">The user is not allowed"
    flash('User not allowed')
    return redirect(url_for('login'))


@app.route('/pushpy/push/send',methods = ['GET', 'POST'])
@fresh_login_required
def sendpush():
    pushform=SendPush()
    if pushform.validate_on_submit():
        #Se envian las notificaciones
        print '>Sending notificacions'
        devmode=pushform.devmode
        users=model.User.query.filter_by(language=pushform.language.data,push=True).all()
        pushclass.send_push_message(users,devmode,json.dumps({"aps": {"alert" : pushform.msj.data, "badge": 0, "sound": "default"}}))
        return redirect(url_for('sendpush'))
    return render_template("sendpush.html",
    content={"title":"Send notifications"},
    form=pushform)

@app.route('/pushpy/push/users',methods = ['GET', 'POST'])
@fresh_login_required
def usersview():
    return render_template("base.html",
                           content={"title":"Users administration"})


@app.route('/pushpy/user',methods=['POST'])
def user():
    if request.headers['Content-Type'] == 'application/json':
        print ">User " + request.json['username'] + ' request data update'
        store_user(request.json)
        return 'Data updated'
    else:
        return "Format not supported"
