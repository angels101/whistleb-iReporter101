from app import create_app, db
from flask_script import Manager,Server
from app.models import User,Case,Role,Status,Admin
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import FlaskForm

# Creating app instance
app = create_app('production')
# app = create_app('test')

manager= Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app, db=db, User=User, Role=Role, Status=Status, Case=Case, Admin=Admin)

if __name__ == '__main__':
    manager.run()  