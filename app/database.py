import config
import mysql.connector


def connect_to_db():
	connection = mysql.connector.connect(user=config.DATABASE_USER,
								  password=config.DATABASE_PASSWORD,
								  host=config.DATABASE_ADDRESS,
								  database=config.DATABASE_NAME)
	return connection


def run_query():
	pass


def add_course(course_id, department, num_credits, title):
	cnx = connect_to_db()
	cursor = cnx.cursor()
	try:
		cursor.execute("INSERT into course values ('{}', '{}', {}, '{}');".format(course_id, department, num_credits, title))
	except mysql.connector.Error as err:
		return "Something went wrong: {}".format(err)
	cnx.commit()
	cursor.close()
	cnx.close()
	return "Query Completed Successfully"


def add_instructor(first, last, email, id, load):
	cnx = connect_to_db()
	cursor = cnx.cursor()
	try:
		cursor.execute("INSERT into instructor values ('{}', '{}', '{}', {}, {});".format(first, last, email, id, load))
	except mysql.connector.Error as err:
		return "Something went wrong: {}".format(err)
	cnx.commit()
	cursor.close()
	cnx.close()
	return "Query Completed Successfully"


def add_section(course_id, section, semester, year):
	cnx = connect_to_db()
	cursor = cnx.cursor()
	try:
		cursor.execute("INSERT into section values ('{}', {}, '{}', {});".format(course_id, section, semester, year))
	except mysql.connector.Error as err:
		return "Something went wrong: {}".format(err)
	cnx.commit()
	cursor.close()
	cnx.close()
	return "Query Completed Successfully"


def add_teaches(instructor_id, course_id, section, semester, year, mod):
	cnx = connect_to_db()
	cursor = cnx.cursor()
	try:
		cursor.execute("INSERT into teaches values({}, '{}', {}, '{}', {}, '{}');".format(instructor_id, course_id, section, semester, year, mod))
	except mysql.connector.Error as err:
		return "Something went wrong: {}".format(err)
	cnx.commit()
	cursor.close()
	cnx.close()
	return "Query Completed Successfully"


# Lots of repeated code, consider compressing


def get_course_table():
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute("select * from course;")
	result_set = cursor.fetchall()
	cursor.close()
	cnx.close()
	return result_set


def get_course_ids():
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute("select course_id from course;")
	result_set = cursor.fetchall()
	cursor.close()
	cnx.close()
	return result_set


def get_instructor_table(string):
	execute = "select * from instructor;"
	if string != 'all':
		execute = 'select first_name, last_name, id from instructor;'
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute(execute)
	result_set = cursor.fetchall()
	cursor.close()
	cnx.close()
	return result_set


def get_mods():
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute("select mod_slot from timeslot;")
	result_set = cursor.fetchall()
	cursor.close()
	cnx.close()
	return result_set


def get_teaches_table():
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute("select * from teaches;")
	result_set = cursor.fetchall()
	cursor.close()
	cnx.close()
	return result_set


def run_phase(num):
	path = ""
	if num is 1:
		path = "app/phases/phase_1.txt"
	elif num is 2:
		run_phase(1)
		path = "app/phases/phase_2.txt"
	elif num is 3:
		run_phase(2)
		path = "app/phases/phase_3.txt"
	elif num is 4:
		run_phase(3)
		path = "app/phases/phase_4.txt"
	elif num is 5:
		run_phase(4)
		path = "app/phases/phase_5.txt"
	cnx = connect_to_db()
	cursor = cnx.cursor()
	file = open(path, 'r')

	for line in file:
		try:
			cursor.execute("{}".format(line))
			cnx.commit()
		except mysql.connector.Error as err:
			error_string = "Something went wrong: {}".format(err)
			print(error_string)
			return error_string
	cursor.close()
	cnx.close()
	file.close()
	return "Queries Completed Successfully"


def test_query():
	cnx = connect_to_db()
	cursor = cnx.cursor()

	cursor.execute("select * from student;")

	for (ID, name, dept_name, tot_cred) in cursor:
		print("{}, {}, {}, {}".format(
			ID, name, dept_name, tot_cred))
	cursor.close()
	cnx.close()
