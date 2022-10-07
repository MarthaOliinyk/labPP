from flask import Flask
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.models.user import User
from src.models.tag import Tag
from src.models.note import Note


@app.route('/api/v1/hello-world-15')
def hello_world():
    return "Hello World 15"


if __name__ == '__main__':
    app.run(debug=True)

serve(app)
