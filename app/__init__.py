from flask import Flask, render_template, request
import app.database as database

app = Flask(__name__)


@app.route('/')
def landing_page():
	courses = database.get_course_table()
	instructors = database.get_instructor_table()
	return render_template('dashboard.html', courses=courses, instructors=instructors)


@app.route('/functions')
def function_page():
	return render_template('input_functions.html')


@app.route('/time-warps')
def time_warps():
	return render_template('time_warps.html')


@app.route("/somewhere_else", methods=['POST'])
def receive_post():
	receive = request.form
	for key, value in receive.items():
		print(key)
		print(value)
	database.test_query()
	return render_template('show_data_sent.html', recieve=receive)


def make_query(query):
	pass


@app.route("/run_phase", methods=['POST'])
def execute_phase():
	database.run_phase(int(request.values["id"]))
	return "200 OK"

