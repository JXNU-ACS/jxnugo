from flask.ext.script import Manager,Shell
from app import create_app, db
from app.models import Role, User, Post, Follow, bbsPost
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, bbsPost=bbsPost, Follow=Follow)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
