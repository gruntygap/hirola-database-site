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
	course_ids = database.get_course_ids()
	return render_template('input_functions.html', course_ids=course_ids)


@app.route('/time-warps')
def time_warps():
	return render_template('time_warps.html')


@app.route("/receive-course", methods=['POST'])
def receive_course():
	receive = request.values
	return database.add_course(receive['courseID'], receive['department'], receive['credits'], receive['title'])


@app.route("/receive-instructor", methods=['POST'])
def receive_instructor():
	receive = request.values
	return database.add_instructor(receive['firstNameInput'], receive['lastNameInput'],
		receive['exampleInputEmail1'], receive['id'], receive['desiredLoadInput'])


@app.route("/receive-section", methods=['POST'])
def receive_section():
	receive = request.values
	return database.add_section(receive['courseID'], receive['section'],
		receive['semester'], receive['year'])


def make_query(query):
	pass


@app.route("/run_phase", methods=['POST'])
def execute_phase():
	database.run_phase(int(request.values["id"]))
	return "200 OK"

