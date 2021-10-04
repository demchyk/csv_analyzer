from bottle import *

app = Bottle()

# Static Routes
@app.get("/static/<filepath>")
def css(filepath):
    return static_file(filepath, root="static")


@app.route('/')
def main():
	return template('index')

@app.route('/load-data')
def main():
	return template('index')
	


run(app, host = 'localhost', port = 8080, reloader = True, debug = True)