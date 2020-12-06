import connexion
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# variables to export:
basedir = ""
flask_app = None
db = None
ma = None
dbname = 'blogposts.db'


def initialize_backend():
    global basedir
    global flask_app
    global db
    global ma
    global dbname

    basedir = os.path.abspath('.')

    swagger_app = connexion.App(__name__, specification_dir=basedir)
    flask_app = swagger_app.app

    flask_app.config['SQLALCHEMY_ECHO'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
        os.path.join(basedir, dbname)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(flask_app)

    ma = Marshmallow(flask_app)


initialize_backend()
