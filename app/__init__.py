from flask import Flask, render_template, request
import config
import mysql.connector

app = Flask(__name__)


@app.route('/')
def landing_page():
	# pass in the classes within database for add-section-course
	# place that where steve is
	return render_template('dashboard.html', steve="steve is a good boi")


@app.route('/functions')
def function_page():
	return render_template('input_functions.html')


@app.route('/time-warps')
def time_warps():
	return render_template('time_warps.html')


@app.route("/somewhere_else", methods=['POST'])
def receive_post():
	connect_to_db()
	receive = request.form
	for key, value in receive.items():
		print(key)
		print(value)
	return render_template('show_data_sent.html', recieve=receive)


def connect_to_db():
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


def make_query(query):
	pass
