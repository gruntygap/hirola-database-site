from flask import Flask, render_template, request, redirect
import app.database as database
import json

app = Flask(__name__)


@app.route('/')
def landing_page():
	courses = database.get_course_table()
	clusters = database.get_cluster_table()
	instructors = database.get_instructor_table('all')
	teaches = database.get_teaches_table()
	sections = database.get_section_table()
	non_ins_load = database.get_non_instructional_load_table()
	return render_template('dashboard.html', courses=courses, instructors=instructors, teaches=teaches, sections=sections, clusters=clusters, non_ins_load=non_ins_load)


@app.route('/functions')
def function_page():
	course_ids = database.get_course_ids()
	mods = database.get_mods()
	instructors = database.get_instructor_table('part')
	clusters = database.get_cluster_table()
	teaches = database.get_teaches_table()
	return render_template('input_functions.html', course_ids=course_ids, mods=mods, instructors=instructors, clusters=clusters, teaches=teaches)

@app.route('/time-warps')
def time_warps():
	return render_template('time_warps.html')


@app.route("/receive-course", methods=['POST'])
def receive_course():
	receive = request.values
	return database.add_course(receive['courseID'], receive['department'], receive['credits'], receive['title'])


@app.route("/receive-cluster", methods=['POST'])
def receive_cluster():
	receive = request.values
	return database.add_cluster(receive['courseID'], receive['clusterID'])


@app.route("/remove-cluster/<course_id>/<cluster_id>", methods=['GET'])
def remove_cluster(course_id, cluster_id):
	remove = database.remove_cluster(course_id, cluster_id)
	return redirect('/functions')


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


@app.route("/receive-non-ins-load", methods=['POST'])
def recieve_non_ins_load():
	receive = request.values
	return database.add_non_ins_load(receive['instructorID'], receive['task'], receive['teu'], receive['semester'], receive['year'])


@app.route("/run_phase", methods=['POST'])
def execute_phase():
	response = database.run_phase(int(request.values["id"]))
	response = json.dumps(response)
	return response

