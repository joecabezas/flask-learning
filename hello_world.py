from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

@app.route('/post/<int:postNumber>')
def show_blog(postNumber):
   return 'Post Number: {}'.format(postNumber)

@app.route('/post/<any>')
def show_blog_any(any):
   return 'sorry only ints!'

if __name__ == '__main__':
    app.run(debug = True)