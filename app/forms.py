from flask.ext.wtf import Form, TextField, BooleanField, SelectField
from flask.ext.wtf import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SendPush(Form):
    msj = TextField('msj', validators = [Required()])
    movieID = TextField('movieID')
    videoID = TextField('videoID')


    language = SelectField(u'language',coerce=unicode, choices=[('es', 'Espanyol'), ('en', 'Ingles')],validators = None)

    def validate(self):
        if self.msj.data!="" and len(self.msj.data)>=20 and len(self.msj.data)<=107:
            return True
        else:
            return False