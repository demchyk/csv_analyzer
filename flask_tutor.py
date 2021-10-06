from flask import *
import main
import time
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
		time1 = time.time()
		main.start_filling(select)
	except:
		return render_template('load-data.tpl', error = 'Something wrong')
	else:
		
		return f'{time.time() - time1}'


@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
	if request.method == 'GET':
		return render_template('dashboard.tpl')
	zte_type = str(request.form.get('zte_type'))
	time_interval = str(request.form.get('daterange'))
	agregation_type = str(request.form.get('agregation_type'))

	# node_check = request.form.get('node_checkbox')
	# main.start_agg(select)
	return(f"<script>alert('{zte_type}, {time_interval}, {agregation_type}')</script>")
		

if __name__ == '__main__':
	app.run(debug = True, threaded = True)