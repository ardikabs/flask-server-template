import os
from server import make_server
from server.app import db
from server.main.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = make_server("default")
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def recreatedb():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    manager.run()