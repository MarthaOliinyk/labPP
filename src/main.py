from flask import Flask
from waitress import serve

app = Flask('__name__')


@app.route('/api/v1/hello-world-15')
def hello_world():
    return "Hello World 15"


if __name__ == '__main__':
    app.run(debug=True)

serve(app)
