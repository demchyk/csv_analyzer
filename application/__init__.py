from flask import Flask
from .agg import delete_temp_files

TEMP_FILES = ['DB/dashboard.temp','DB/export_to_csv.temp']

def init_app():
	delete_temp_files(TEMP_FILES)
	app = Flask(__name__)

	with app.app_context():

		from . import routes
		from .plotlydash.dashapp import init_dashboard
		app = init_dashboard(app)

		return app
		