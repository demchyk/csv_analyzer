from bottle import *
from dbwork import *

app = Bottle()
def hello():
	return 'Hello!'


@app.route('/')
def main():
	return creator_basa()

debug(True)
run(app, host = 'localhost', port = 8080, reloader = True)