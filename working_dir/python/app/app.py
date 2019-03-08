from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello, World!'

@application.route('/test')
def test():
    return 'Everything works as expected.'