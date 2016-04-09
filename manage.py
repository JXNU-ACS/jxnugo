#-*- coding: UTF-8 -*-
from app import create_app
from flask.ext.script import Manager,Shell,Server
from app.models import Role,User

app=create_app()
manager=Manager(app)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("runserver",Server(host='0.0.0.0',port='5000'))



if __name__=='__main__':
    manager.run()