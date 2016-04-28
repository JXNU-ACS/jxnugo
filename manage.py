#!usr/bin/env/ python
#-*- coding: UTF-8 -*-
from app import create_app,db
import os
from flask.ext.script import Manager,Shell
from app.models import Role,User,Post
from flask.ext.migrate import Migrate,MigrateCommand
basedir=os.path.abspath(os.path.dirname(__file__))

app=create_app('default')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@139.129.52.83:3306/jxnugo'
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://root:laidaolong@localhost:3306/jxnugo'
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()