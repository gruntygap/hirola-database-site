import config
import mysql.connector


def connect_to_db():
	connection = mysql.connector.connect(user=config.DATABASE_USER, password=config.DATABASE_PASSWORD,
										 host=config.DATABASE_ADDRESS, database=config.DATABASE_NAME,
										 port=config.DATABASE_PORT)
	return connection


def update_or_add_query(string):
	cnx = connect_to_db()
	cursor = cnx.cursor()
	try:
		cursor.execute(string)
	except mysql.connector.Error as err:
		return "Something went wrong: {}".format(err)
	cnx.commit()
	cursor.close()
	cnx.close()
	return "Query Completed Successfully"


def add_course(course_id, department, num_credits, title):
	return update_or_add_query(
		"INSERT into course values ('{}', '{}', {}, '{}');".format(course_id, department, num_credits, title))


def add_cluster(course_id, cluster_id):
	return update_or_add_query("INSERT into likely_course_conflicts values ('{}', {});".format(course_id, cluster_id))


def remove_cluster(course_id, cluster_id):
	return update_or_add_query(
		"DELETE from likely_course_conflicts where course_id = '{}' and cluster_id = {};".format(course_id, cluster_id))


def remove_section(course_id, section_id, semester, year):
	return update_or_add_query(
		"DELETE from section where course_id = '{}' and sec_id = {} and semester = '{}' and year = {};".format(course_id, section_id, semester, year))

def add_instructor(first, last, email, id, load):
	return update_or_add_query(
		"INSERT into instructor values ('{}', '{}', '{}', {}, {});".format(first, last, email, id, load))


def add_section(course_id, section, semester, year):
	return update_or_add_query(
		"INSERT into section values ('{}', {}, '{}', {});".format(course_id, section, semester, year))


def add_time_restriction(instructor_id, mod):
	return update_or_add_query("INSERT into instructor_time_restrictions values ({}, '{}');".format(instructor_id, mod))


def remove_time_restriction(instructor_id, mod):
	return update_or_add_query("DELETE from instructor_time_restrictions where id = {} and mod_slot = '{}';".format(instructor_id, mod))


def add_teaches(instructor_id, course_id, section, semester, year):
	return update_or_add_query(
		"INSERT into teaches values({}, '{}', {}, '{}', {}, NULL);".format(instructor_id, course_id, section, semester,
																		   year))


def remove_teaches(id, course_id, section, semester, year):
	return update_or_add_query(
		"DELETE from teaches where id = {} and course_id = '{}' and sec_id = {} and semester = '{}' and year = {};".format(id, course_id, section, semester, year))


def update_teaches_mod(instructor_id, course_id, section, semester, year, mod):
	if mod == "NULL":
		return update_or_add_query(
			"update teaches set mod_slot = {} where id = {} and course_id = '{}' and sec_id = {} and semester = '{}' and year = {};".format(
				mod, instructor_id, course_id, section, semester, year))
	else:
		return update_or_add_query(
			"update teaches set mod_slot = '{}' where id = {} and course_id = '{}' and sec_id = {} and semester = '{}' and year = {};".format(
				mod, instructor_id, course_id, section, semester, year))


def add_non_ins_load(instructor_id, task, teu, semester, year):
	return update_or_add_query(
		"INSERT into non_instructional_load values({}, '{}', {}, '{}', {});".format(instructor_id, task, teu, semester,
																					year))


# Lots of repeated code, consider compressing


def get_query(query):
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute(query)
	result_set = cursor.fetchall()
	cursor.close()
	cnx.close()
	return result_set


def get_course_table():
	return get_query("select * from course;")


def get_cluster_table():
	return get_query("select * from likely_course_conflicts order by cluster_id;")


def get_course_ids():
	return get_query("select course_id from course;")


def get_instructor_table(string):
	execute = "select * from instructor;"
	if string != 'all':
		execute = 'select first_name, last_name, id from instructor;'
	return get_query(execute)


def get_mods():
	return get_query("select mod_slot from timeslot;")


def get_instructor_time_restrictions_table():
	return get_query("select * from instructor_time_restrictions")


def get_teaches_table():
	return get_query("select * from teaches;")


def get_section_table(custom=None):
	if custom is None:
		return get_query("select * from section;")
	else:
		return get_query(custom)


def get_non_instructional_load_table():
	return get_query("select * from non_instructional_load;")


def remove_non_instructional_load(id, task, semester, year):
	return update_or_add_query(
		"DELETE from non_instructional_load where id = {} and task = '{}' and semester = '{}' and year = {};".format(id, task, semester, year))


# Report Queries
def get_courses_and_instructors_report():
	return get_query("select * from teaches natural join course natural join instructor order by teaches.year, case teaches.semester when 'Interim' then 1 when 'Spring' then 2 when 'Summer' then 3 when 'Fall' then 4 end, instructor.last_name, instructor.first_name, course.department, teaches.sec_id;")


def get_unscheduled_courses():
	return get_query("select * from instructor natural join teaches natural join course where mod_slot is NULL;")


def get_course_times():
	return get_query("select * from course natural join teaches natural join timeslot order by teaches.year, case teaches.semester when 'Interim' then 1 when 'Spring' then 2 when 'Summer' then 3 when 'Fall' then 4 end, course.course_id, teaches.sec_id;")


def get_instructor_times():
	return get_query("select * from instructor natural join teaches natural join timeslot order by teaches.year, case teaches.semester when 'Interim' then 1 when 'Spring' then 2 when 'Summer' then 3 when 'Fall' then 4 end, instructor.last_name, instructor.first_name;")


def get_ins_restriction_violations():
	return get_query("select * from teaches natural join course natural join instructor natural join instructor_time_restrictions;")


def get_cluster_violations():
	return get_query("select * from (select * from teaches natural join course natural join likely_course_conflicts) A, (select * from teaches natural join course natural join likely_course_conflicts) B where A.course_id <> B.course_id and A.mod_slot = B.mod_slot and A.cluster_id = B.cluster_id and A.semester = B.semester and A.year = B.year order by A.mod_slot;")


def get_teu_violations():
	return get_query("select id, first_name, last_name, semester, year, SUM(teu) as teu, desired_load from (select first_name, last_name, id, SUM(IF(num_credits = 3 OR num_credits = 4, 3.4, num_credits)) as teu, semester, year, desired_load from teaches natural join instructor natural join course group by id, year, semester union (select first_name, last_name, id, teu, semester, year, desired_load from non_instructional_load natural join instructor) order by id, year, semester) as wow group by id, year, semester;")


def run_phase(num):
	path = ""
	response_stack = []
	if num is 1:
		path = "app/phases/phase_1.txt"
	elif num is 2:
		stack = run_phase(1)
		response_stack.append(stack[0])
		path = "app/phases/phase_2.txt"
	elif num is 3:
		stack = run_phase(2)
		response_stack.append(stack[0])
		response_stack.append(stack[1])
		path = "app/phases/phase_3.txt"
	elif num is 4:
		stack = run_phase(3)
		response_stack.append(stack[0])
		response_stack.append(stack[1])
		response_stack.append(stack[2])
		path = "app/phases/phase_4.txt"
	elif num is 5:
		stack = run_phase(4)
		response_stack.append(stack[0])
		response_stack.append(stack[1])
		response_stack.append(stack[2])
		response_stack.append(stack[3])
		path = "app/phases/phase_5.txt"
	cnx = connect_to_db()
	cursor = cnx.cursor()
	file = open(path, 'r')
	count = 1
	errored = False
	for line in file:
		try:
			cursor.execute("{}".format(line))
			cnx.commit()
		except mysql.connector.Error as err:
			error_string = "PHASE " + str(num) + ": LINE_" + str(count) + ": " + "Something went wrong: {}".format(err)
			print("PHASE " + str(num) + ": LINE_" + str(count) + ": " + "Something went wrong: {}".format(err))
			response_stack.append(error_string)
			errored = True
			break
		count = count + 1
	cursor.close()
	cnx.close()
	file.close()
	if errored is False:
		response_stack.append("Queries Completed Successfully")
	return response_stack
