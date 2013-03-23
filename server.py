# Pushpy: Created by ppeibumur

import app

if __name__ == '__main__':
    #Initialize DB and Add users
    app.db.create_all()
    dbadmins=app.model.adminUser.query.all()
    for admin in dbadmins:
        app.db.session.delete(admin)
        app.db.session.commit()
    for user in app.adminusers:
        newAdmin= app.model.adminUser(nickname=user['nickname'],email=user['email'])
        app.db.session.add(newAdmin)
        app.db.session.commit()

    #Initialize flask
    app.app.run(port=5000,host='0.0.0.0',debug=False)

