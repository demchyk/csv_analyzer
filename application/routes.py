from flask import current_app as app
from flask import render_template,request,redirect,url_for
from . import engine
from . plotlydash import dashboard
import time
import os

# Redirectig from root to start page (dashboard)
@app.route('/')
def index():
	return redirect(url_for('dashboard_init'))
# ----------------------------------------------------------------------------------

# Render template with taking error as parametr from link (?error=smth)
@app.route('/load-data')
def load_data():
	return render_template('load-data.tpl',error = request.args.get('result'))
# ----------------------------------------------------------------------------------

# Handle form POST method to start uploading data to pickle. Result is returned as url parameter (?result=Success)
@app.route('/load-data-action', methods=['POST'])
def load_data_action():
	time1 = time.time()
	zte_type = str(request.form.get('zte_type'))
	# engine.start_filling(zte_type)
	try:
		engine.start_filling(zte_type) # method to fill pickle from zip(csv)
		print('Super algorithm has dealed with it in just ',time.time() - time1,' seconds')
		return redirect(url_for('load_data', result = 'Success'))
	except:
		return redirect(url_for('load_data', result = 'Missing some files / folders'))

# ----------------------------------------------------------------------------------
# Render template with taking error as parametr from link (?error=smth)
@app.route('/export-to-csv')
def export_to_csv():
	return render_template('export_csv.tpl',error = request.args.get('result'))
# ----------------------------------------------------------------------------------

# Getting multiple form's parametrs. Getting pickle file from local and putting it to server as temp file
@app.route('/export-to-csv-action', methods=['POST'])
def export_to_csv_action():
	if request.files['export_to_csv_input_file']:
		file = request.files['export_to_csv_input_file']
		file.save(os.path.join('DB', 'export_to_csv.temp')) # saving local file to server's folder
		time_interval = str(request.form.get('daterange'))
		aggregation_type = str(request.form.get('aggregation_cell_type'))
		aggregation_time_type = str(request.form.get('aggregation_time_type'))
		claster_check = str(request.form.get('cluster_check'))
		try:
			engine.start_agg_to_csv(time_interval,claster_check,aggregation_time_type,aggregation_type)
			return redirect(url_for('export_to_csv', result = 'Success'))
		except:
			engine.start_agg_to_csv(time_interval,claster_check,aggregation_time_type,aggregation_type) # to see exact error from flask
	return redirect(url_for('export_to_csv', result = 'File was not uploaded')) # try to upload file again
# ----------------------------------------------------------------------------------

# Render template for uploading pickle to dashboard
@app.route('/dashboard')
def dashboard_init():
	return render_template('dash.tpl')
# ----------------------------------------------------------------------------------

# Handling POST method. Saving file from local to server
@app.route('/dashboard-action', methods = ['POST'])
def upload():
	file = request.files['dashboard_input_file']
	file.save(os.path.join('DB', 'dashboard.temp')) # saving local file to server's folder
	return(redirect('/dashapp'))
# ----------------------------------------------------------------------------------