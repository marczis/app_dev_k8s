from flask import Flask
import socket
application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello, World!'

@application.route('/test')
def test():
    return 'Everything works as expected.'

@application.route('/info')
def info():
    return socket.gethostname()