from flask import *
import main

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('main.tpl')

@app.route('/load-data', methods = ['GET','POST'])
def start():
	if request.method == 'GET':
		return render_template('load-data.tpl')
	else:
		select = str(request.form.get('zte_type'))
		node_check = request.form.get('node_checkbox')
		main.start_filling(select,node_check)

		# try:
		# 	main.start_filling(select)
		# except:
		# 	return render_template('load-data.tpl', error = 'Something wrong')
		# else:
		# 	return render_template('load-data.tpl', error = 'Database created')
		

if __name__ == '__main__':
	app.run(debug = True)