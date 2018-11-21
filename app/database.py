import config
import mysql.connector


def connect_to_db():
	pass


def run_query():
	pass


def start_phase(num):
	pass


def test_query():
	cnx = mysql.connector.connect(user=config.DATABASE_USER,
								  password=config.DATABASE_PASSWORD,
								  host=config.DATABASE_ADDRESS,
								  database=config.DATABASE_NAME)
	cursor = cnx.cursor()

	cursor.execute("select * from student;")

	for (ID, name, dept_name, tot_cred) in cursor:
		print("{}, {}, {}, {}".format(
			ID, name, dept_name, tot_cred))
	cursor.close()
	cnx.close()