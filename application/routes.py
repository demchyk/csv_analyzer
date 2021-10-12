from flask import current_app as app
from flask import render_template,request
from . import engine

@app.route('/')
def index():
	return render_template('index.tpl')

@app.route('/load-data', methods = ['GET','POST'])
def load_data():
	if request.method == 'GET':
		return render_template('load-data.tpl')

	select = str(request.form.get('zte_type'))
	try:
		engine.start_filling(select)
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
	claster_check = str(request.form.get('cluster_check'))
	try:
		engine.start_agg(zte_type,time_interval,aggregation_time_type,aggregation_type,claster_check)
		return render_template('export_csv.tpl', error = 'Success')
	except:
		engine.start_agg(zte_type,time_interval,aggregation_time_type,aggregation_type,claster_check)