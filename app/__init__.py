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
	ins_time_restrict = database.get_instructor_time_restrictions_table()
	return render_template('dashboard.html', **locals())


@app.route('/functions')
def function_page():
	# unneeded as each component loads on it's own
	course_ids = database.get_course_ids()
	mods = database.get_mods()
	instructors = database.get_instructor_table('part')
	clusters = database.get_cluster_table()
	sections = database.get_section_table()
	non_ins_load = database.get_non_instructional_load_table()
	teaches = database.get_teaches_table()
	return render_template('input_functions.html', **locals())


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
	database.remove_cluster(course_id, cluster_id)
	course_ids = database.get_course_ids()
	clusters = database.get_cluster_table()
	return render_template('add-cluster.html', **locals())


@app.route("/add-cluster", methods=['GET'])
def add_cluster():
	course_ids = database.get_course_ids()
	clusters = database.get_cluster_table()
	return render_template('add-cluster.html', **locals())


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


@app.route("/remove-section/<course_id>/<section_id>/<semester>/<year>", methods=['GET'])
def remove_section(course_id, section_id, semester, year):
	database.remove_section(course_id, section_id, semester, year)
	course_ids = database.get_course_ids()
	sections = database.get_section_table()
	return render_template('add-section-course.html', **locals())


@app.route("/receive-restriction", methods=['POST'])
def receive_restriction():
	receive = request.values
	return database.add_time_restriction(receive['instructorToPair'], receive['modToPair'])


@app.route("/receive-teaches", methods=['POST'])
def recieve_teaches():
	receive = request.values
	section = json.loads(receive['section'])
	return database.add_teaches(receive['instructorToPair'], section['course_id'], section['section'], section['semester'], section['year'])


@app.route("/remove-teaches", methods=['POST'])
def remove_teaches():
	receive = request.values
	taught = json.loads(receive['taught'])
	database.remove_teaches(taught['id'], taught['course_id'], taught['section'], taught['semester'], taught['year'])
	return get_assign_course_instructor()


@app.route("/receive-teaches-mod", methods=['POST'])
def recieve_teaches_mod():
	receive = request.values
	teaches = json.loads(receive['teach'])
	return database.update_teaches_mod(teaches['id'], teaches['course_id'], teaches['section'], teaches['semester'], teaches['year'], receive['modToPair'])


@app.route("/receive-non-ins-load", methods=['POST'])
def recieve_non_ins_load():
	receive = request.values
	return database.add_non_ins_load(receive['instructorID'], receive['task'], receive['teu'], receive['semester'], receive['year'])


@app.route("/remove-time-restrict/<instructor_id>/<mod>", methods=['GET'])
def remove_time_restrictions(instructor_id, mod):
	database.remove_time_restriction(instructor_id, mod)
	return get_time_restrictions()


@app.route("/run_phase", methods=['POST'])
def execute_phase():
	response = database.run_phase(int(request.values["id"]))
	response = json.dumps(response)
	return response


@app.route("/get_mod_selection", methods=['GET'])
def get_assign_mod():
	teaches = database.get_teaches_table()
	return render_template("assign-mod-select.html", **locals())


@app.route("/get-cluster-page", methods=['GET'])
def get_cluster_page():
	course_ids = database.get_course_ids()
	clusters = database.get_cluster_table()
	return render_template("add-cluster.html", **locals())


@app.route("/get-section-page", methods=['GET'])
def get_section_page():
	course_ids = database.get_course_ids()
	sections = database.get_section_table()
	return render_template("add-section-course.html", **locals())


@app.route("/get-time-restrictions", methods=['GET'])
def get_time_restrictions():
	mods = database.get_mods()
	instructors = database.get_instructor_table('part')
	ins_time_restrict = database.get_instructor_time_restrictions_table()
	return render_template("add-instructor-time-restriction.html", **locals())


@app.route("/get-assign-course-instructor", methods=['GET'])
def get_assign_course_instructor():
	sections = database.get_section_table("select * from section natural left join teaches where id is NULL;")
	instructors = database.get_instructor_table('part')
	teaches = database.get_teaches_table()
	return render_template("assign-course-instructor.html", **locals())


@app.route("/get-assign-mod", methods=['GET'])
def get_mod_component():
	mods = database.get_mods()
	teaches = database.get_teaches_table()
	return render_template("assign-mod.html", **locals())


@app.route("/get-non-instructional", methods=['GET'])
def get_non_instructional():
	instructors = database.get_instructor_table('part')
	return render_template("add-non-instructional-load.html", **locals())