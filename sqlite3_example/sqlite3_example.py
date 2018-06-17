import json
import sqlite3
import sys

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)

@app.route('/create_database')
def create_database():
    conn = _get_connection()
    print("Opened database successfully");

    conn.execute('CREATE TABLE IF NOT EXISTS tasks (name TEXT, done INTEGER)')
    print("Table created successfully");
    conn.close()

    return "Done"

@app.route('/create/<string:name>')
def create(name):
    result = {'success':False}
    try:
        if _add_new_task(name):
            result['success'] = True
            return json.dumps(result)
    except:
        result['message'] = "error in db"
        return json.dumps(result)
    result['message'] = "not even connected"
    return json.dumps(result)

@app.route('/list')
def list():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall();
    return json.dumps([{'name':item[0], 'done':item[1]} for item in rows], indent=4)

@app.route('/read/<string:name>')
def read(name):
    if not name:
        return
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE name=?", (name,))

    row = cursor.fetchone();
    return json.dumps({'name':row[0], 'done':row[1]})

@app.route('/update/<string:name>/<int:value>')
def update(name, value):
    if not name:
        return
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done=? WHERE name=?", (value, name))
    conn.commit()
    conn.close()
    return redirect(url_for('read', name=name))

@app.route('/delete/<string:name>')
def delete(name):
    if not name:
        return
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE name=?", (name,))
    conn.commit()
    conn.close()
    return "ok"

def _add_new_task(name):
    if not name:
        return False

    conn = _get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (name,done) VALUES (?,?)",
            (name,0)
        )

        conn.commit()
        conn.close()
        return True
    return False

def _get_connection():
    return sqlite3.connect("database.db")

if __name__ == '__main__':
    app.run(debug=True)