from flask import current_app as app
from flask import render_template,request,redirect
from . import engine
import time

@app.route('/')
def index():
	return render_template('index.tpl')

@app.route('/load-data', methods = ['GET','POST'])
def load_data():
	if request.method == 'GET':
		return render_template('load-data.tpl')
	time1 = time.time()
	select = str(request.form.get('zte_type'))
	engine.start_filling(select)
	# try:
	# 	engine.start_filling(select)
	# 	return render_template('load-data.tpl', error = 'Success')
	# except:
	# 	return render_template('load-data.tpl', error = 'Missing some files / folders')
	print('Super algorithm has dealed with it in just ',time.time() - time1,' seconds')

@app.route('/export-to-csv', methods = ['GET','POST'])
def export_to_csv():
	if request.method == 'GET':
		return render_template('export_csv.tpl')
	zte_type = str(request.form.get('zte_type'))
	time_interval = str(request.form.get('daterange'))
	aggregation_type = str(request.form.get('aggregation_cell_type'))
	aggregation_time_type = str(request.form.get('aggregation_time_type'))
	claster_check = str(request.form.get('cluster_check'))
	try:
		engine.start_agg_to_csv(zte_type,time_interval,claster_check,aggregation_time_type,aggregation_type)
		return render_template('export_csv.tpl', error = 'Success')
	except:
		engine.start_agg_to_csv(zte_type,time_interval,claster_check,aggregation_time_type,aggregation_type)

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard_init():
	if request.method == 'GET':
		return render_template('dashboard.tpl')
	zte_type = str(request.form.get('zte_type'))
	time_interval = str(request.form.get('daterange'))
	claster_check = str(request.form.get('cluster_check'))
	try:
		engine.start_agg_to_dashboard_pickle(zte_type,time_interval,claster_check)
		return render_template('dashboard.tpl')
	except:
		engine.start_agg_to_dashboard_pickle(zte_type,time_interval,claster_check)

# @app.route('/' , methods=['GET', 'POST'])
# def landing_page():
# 	dashboard_id = request.args.get('dashboard_id')
# 	session['dashboard_id'] = dashboard_id

# 	return redirect("/dash/")