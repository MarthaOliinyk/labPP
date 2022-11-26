from flask import Flask
# from waitress import serve
from os import getenv
# from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth


app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

import src.resourses
import src.models.role
import  src.models.users_roles

@app.before_first_request
def create_tables():
    db.create_all()
    src.models.Role(name='user').save_to_db()
    src.models.Role(name='admin').save_to_db()
# serve(app)
