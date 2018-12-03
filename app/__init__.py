from flask import Flask, render_template, request
import app.database as database

app = Flask(__name__)


@app.route('/')
def landing_page():
	courses = database.get_course_table()
	instructors = database.get_instructor_table('all')
	teaches = database.get_teaches_table()
	sections = database.get_section_table()
	return render_template('dashboard.html', courses=courses, instructors=instructors, teaches=teaches, sections=sections)


@app.route('/functions')
def function_page():
	course_ids = database.get_course_ids()
	mods = database.get_mods()
	instructors = database.get_instructor_table('part')
	return render_template('input_functions.html', course_ids=course_ids, mods=mods, instructors=instructors)


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


@app.route("/receive-teaches", methods=['POST'])
def recieve_teaches():
	receive = request.values
	return database.add_teaches(receive['instructorToPair'], receive['courseID'], receive['section'], receive['semester'], receive['year'])


@app.route("/receive-teaches-mod", methods=['POST'])
def recieve_teaches_mod():
	receive = request.values
	return database.update_teaches_mod(receive['instructorToPair'], receive['courseID'], receive['section'], receive['semester'], receive['year'], receive['modToPair'])


@app.route("/run_phase", methods=['POST'])
def execute_phase():
	return database.run_phase(int(request.values["id"]))

