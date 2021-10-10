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
		return render_template('load-data.tpl', error = 'Success')
	except:
		return render_template('load-data.tpl', error = 'Missing some files / folders')



@app.route('/export-to-csv', methods = ['GET','POST'])
def dashboard():
	if request.method == 'GET':
		return render_template('export_csv.tpl')
	zte_type = str(request.form.get('zte_type'))
	time_interval = str(request.form.get('daterange'))
	aggregation_type = str(request.form.get('aggregation_cell_type'))
	aggregation_time_type = str(request.form.get('aggregation_time_type'))
	try:
		main.start_agg(zte_type,time_interval,aggregation_time_type,aggregation_type)
		return render_template('export_csv.tpl', error = 'Success')
	except:
		main.start_agg(zte_type,time_interval,aggregation_time_type,aggregation_type)

		
if __name__ == '__main__':
	app.run(debug = True, threaded = True)