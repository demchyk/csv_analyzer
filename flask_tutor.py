from flask import *
import main

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('main.tpl')

@app.route('/load-data', methods = ['GET','POST'])
def load_data():
	if request.method == 'GET':
		return render_template('load-data.tpl')

	select = str(request.form.get('zte_type'))
	try:
		main.start_filling(select)
	except:
		return render_template('load-data.tpl', error = 'Something wrong')
	else:
		return render_template('load-data.tpl', error = 'Database created')

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
	if request.method == 'GET':
		return render_template('dashboard.tpl')
	select = str(request.form.get('zte_type'))
	# node_check = request.form.get('node_checkbox')
	main.start_agg(select)
		

if __name__ == '__main__':
	app.run(debug = True)