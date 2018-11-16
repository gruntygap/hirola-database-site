from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def landing_page():
	# pass in the classes within database for add-section-course
	# place that where steve is
    return render_template('dashboard.html', steve="steve is a good boi")


@app.route('/dashboard')
def dash():
	# pass in the classes within database for add-section-course
	# place that where steve is
    return landing_page()


@app.route('/functions')
def function_page():
    return render_template('input_functions.html')


@app.route('/time-warps')
def time_warps():
    return render_template('time_warps.html')


@app.route("/somewhere_else", methods=['POST'])
def receive_post():
	recieve = request.form
	for key, value in recieve.items():
		print(key)
		print(value)
	return render_template('show_data_sent.html', recieve=recieve)


def connect_to_db():
	pass


def make_query(query):
	pass

