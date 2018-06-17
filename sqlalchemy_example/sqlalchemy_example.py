import json

from flask import Flask
from flask import redirect
from flask import url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
db = SQLAlchemy(app)

class Tasks(db.Model):
    name = db.Column('name', db.String(), primary_key = True)
    done = db.Column(db.Boolean())

    def __init__(self, name, done=False):
        self.name = name
        self.done = done


@app.route('/list')
def list():
    tasks = Tasks.query.all()
    return json.dumps([{'name':task.name, 'done':task.done} for task in tasks])

@app.route('/read/<string:name>')
def read(name):
    tasks = Tasks.query.filter_by(name=name)
    return json.dumps(tasks)

@app.route('/create/<string:name>')
def create(name):
    task = Tasks(name=name)
    db.session.add(task)
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)