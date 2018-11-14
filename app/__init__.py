from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/add-instructor')
def add_instructor():
    return render_template('add-instructor.html')

@app.route('/add-course')
def add_course():
    return render_template('add-course.html')

@app.route('/add-section')
def add_section():
    return render_template('add-section-course.html')

@app.route('/assign-course-instructor')
def assign_course_instructor():
    return render_template('assign-course-instructor.html')

@app.route('/assign-course-mod')
def assign_course_mod():
    return render_template('assign-course-mod.html')

@app.route("/somewhere_else", methods=['POST'])
def receive_post():
	recieve = request.form
	for key, value in recieve.items():
		print(key)
		print(value)
	return render_template('show_data_sent.html', recieve=recieve)
