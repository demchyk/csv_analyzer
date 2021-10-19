from flask import current_app as app
from flask import render_template,request,redirect,url_for
from . import engine
from . plotlydash import dashboard
import time
import os

@app.route('/')
def index():
	return redirect(url_for('dashboard_init'))

@app.route('/load-data')
def load_data():
	return render_template('load-data.tpl',error = request.args.get('result'))

@app.route('/load-data-action', methods=['POST'])
def load_data_action():
	time1 = time.time()
	select = str(request.form.get('zte_type'))
	# engine.start_filling(select)
	try:
		engine.start_filling(select)
		print('Super algorithm has dealed with it in just ',time.time() - time1,' seconds')
		return redirect(url_for('load_data', result = 'Success'))
	except:
		return redirect(url_for('load_data', result = 'Missing some files / folders'))

@app.route('/export-to-csv')
def export_to_csv():
	return render_template('export_csv.tpl',error = request.args.get('result'))

@app.route('/export-to-csv-action', methods=['POST'])
def export_to_csv_action():
	if request.files['export_to_csv_input_file']:
		file = request.files['export_to_csv_input_file']
		file.save(os.path.join('DB', 'export_to_csv.temp'))
		time_interval = str(request.form.get('daterange'))
		aggregation_type = str(request.form.get('aggregation_cell_type'))
		aggregation_time_type = str(request.form.get('aggregation_time_type'))
		claster_check = str(request.form.get('cluster_check'))
		try:
			engine.start_agg_to_csv(time_interval,claster_check,aggregation_time_type,aggregation_type)
			return redirect(url_for('export_to_csv', result = 'Success'))
		except:
			engine.start_agg_to_csv(time_interval,claster_check,aggregation_time_type,aggregation_type)
	return redirect(url_for('export_to_csv', result = 'File was not uploaded'))


@app.route('/dashboard')
def dashboard_init():
	return render_template('dash.tpl')

@app.route('/dashboard-action', methods = ['POST'])
def upload():
	file = request.files['dashboard_input_file']
	print(file.filename)
	file.save(os.path.join('DB', 'dashboard.temp'))
	return(redirect('/dashapp'))
# @app.route('/dashboard', methods = ['GET','POST'])
# def dashboard_init():
# 	if request.method == 'GET':
# 		return render_template('dashboard.tpl')
# 	zte_type = str(request.form.get('zte_type'))
# 	time_interval = str(request.form.get('daterange'))
# 	claster_check = str(request.form.get('cluster_check'))
# 	try:
# 		engine.start_agg_to_dashboard_pickle(zte_type,time_interval,claster_check)		
# 		dashboard.init_dashboard(app)
# 		return redirect('/dashapp')
# 	except:
# 		engine.start_agg_to_dashboard_pickle(zte_type,time_interval,claster_check)
# 		dashboard.init_dashboard(app)




# @app.route('/' , methods=['GET', 'POST'])
# def landing_page():
# 	dashboard_id = request.args.get('dashboard_id')
# 	session['dashboard_id'] = dashboard_id

# 	return redirect("/dash/")