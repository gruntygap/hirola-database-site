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


def get_course_table():
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute("select * from course")
	result_set = cursor.fetchall()
	cursor.close()
	cnx.close()
	return result_set


def get_instructor_table():
	cnx = connect_to_db()
	cursor = cnx.cursor()
	cursor.execute("select * from instructor")
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
		except:
			print("Cannot do that?")
	cursor.close()
	cnx.close()
	file.close()


def test_query():
	cnx = connect_to_db()
	cursor = cnx.cursor()

	cursor.execute("select * from student;")

	for (ID, name, dept_name, tot_cred) in cursor:
		print("{}, {}, {}, {}".format(
			ID, name, dept_name, tot_cred))
	cursor.close()
	cnx.close()
