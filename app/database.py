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


def start_phase(num):
	pass


def run_mass_query():
	cnx = connect_to_db()
	cursor = cnx.cursor()
	file = open("app/phases/test.txt", 'r')

	for line in file:
		try:
			cursor.execute("{}".format(line))
			cnx.commit()
		except:
			print("Cannot do that?")
	cursor.close()
	cnx.close()
	file.close()
	pass


def test_query():
	cnx = connect_to_db()
	cursor = cnx.cursor()

	cursor.execute("select * from student;")

	for (ID, name, dept_name, tot_cred) in cursor:
		print("{}, {}, {}, {}".format(
			ID, name, dept_name, tot_cred))
	cursor.close()
	cnx.close()