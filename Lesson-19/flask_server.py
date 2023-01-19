import flask
from flask import Flask

app = Flask("sample_web_app")

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/valeria")
def valeria():
    return "That was Valeria"

if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=5555)
    app.run(debug=True,port=5001)