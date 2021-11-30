from application import init_app
import warnings
warnings.filterwarnings("ignore")


app = init_app()

if __name__ == '__main__':
	app.run(debug=True)