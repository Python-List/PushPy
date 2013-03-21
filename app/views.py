#!flask/bin/python
from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g
import datetime
from app import app,db,model,oid
from forms import LoginForm,SendPush
from flask_login import login_user, logout_user, current_user, login_required, fresh_login_required
from push import pushclass
import json
import threading

#Inicializamos la base de datos
db.create_all()

def store_user(jsondata):
    #try:
        username=jsondata['username']
        udid=jsondata['udid']
        language=jsondata['language']
        push=jsondata['push']
        last=jsondata['last']
        token=None
        if jsondata.has_key('token'):
            if(jsondata['token'] is not None):
                token=jsondata['token']

        #Comprobamos si el usuario existe
        print 'Comprobamos si existe usuario con udid '+udid
        checkuser = model.User.query.filter_by(username=username).first()
        if checkuser is not None:
            print '>El usuario ya existe, lo actualizamos'
            checkuser.username=username
            checkuser.udid=udid
            checkuser.language=language
            checkuser.push=push
            checkuser.last=datetime.date.today()
            checkuser.token=token
            db.session.commit()
        else:
            print '>El usuario no existe, creamos usuario'
            newuser  = model.User(username=username,udid=udid,language=language,push=push,last=last,token=token)
            db.session.add(newuser)
            db.session.commit()
    #except:
        #print '>ERROR: ha sido imposible almacenar al usuario'

@app.before_request
def before_request():
    g.user = current_user

@app.route('/yonkiPOPS/push',methods = ['GET', 'POST'])
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
    content={'title':'Notificaciones push'},
    form=form,
    providers = app.config['OPENID_PROVIDERS']
    )
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Imposible loggear sin email')
        redirect(url_for('login'))
    print 'El usuario '+resp.email+' esta intentando acceder'
    user = model.yonkiUser.query.filter_by(email = resp.email).first()
    if user is not None:
        login_user(user, remember=False)
        return redirect(url_for('sendpush'))
    print "El usuario no esta registrado"
    flash('Usuario no registrado')
    return redirect(url_for('login'))


@app.route('/yonkiPOPS/push/send',methods = ['GET', 'POST'])
@fresh_login_required
def sendpush():
    pushform=SendPush()
    if pushform.validate_on_submit():
        #Se envian las notificaciones
        print 'Enviando notificacion'
        print 'Cuerpo: '+pushform.msj.data
        print 'MovieID: '+pushform.movieID.data
        print 'VideoID: '+pushform.videoID.data

        users=model.User.query.filter_by(language=pushform.language.data,push=True,username='pepibumur').all()
        pushclass.send_push_message(users,json.dumps({"aps": {"alert" : pushform.msj.data, "movieID":pushform.movieID.data,"videoID":pushform.videoID.data, "badge": 0, "sound": "sound.caff"}}))
        #t=threading.Thread(target=pushclass.send_push_message, args=(users,json.dumps({"aps": {"alert" : pushform.msj.data, "badge": 0, "sound": "sound.caff"}})))
        #t.start()
        return redirect(url_for('sendpush'))
    return render_template("sendpush.html",
    content={"title":"Envio de notificaciones"},
    form=pushform)

@app.route('/yonkiPOPS/user',methods=['POST'])
def user():
    if request.headers['Content-Type'] == 'application/json':
        print "> El usuario " + request.json['username'] + ' desea actualizar sus datos'
        store_user(request.json)
        return 'Datos actualizados'
    else:
        return "Formato no soportado"
