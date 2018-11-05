from flask import Flask, render_template, url_for, request
import osmnx as ox, networkx as nx

from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'


class ReusableForm(Form):
	present_lat = TextField('present_lat:', validators=[validators.required()])
	present_long = TextField('present_long:', validators=[validators.required()])
	dest_lat = TextField('dest_lat:', validators=[validators.required()])
	dest_long = TextField('dest_long:', validators=[validators.required()])

def get_time():
	time = strftime("%Y-%m-%dT%H:%M")
	return time

def write_to_disk(name, surname, email):
	data = open('file.log', 'a')
	timestamp = get_time()
	data.write('DateStamp={}, Name={}, Surname={}, Email={} \n'.format(timestamp, present_lat, present_long, dest_lat))
	data.close()

@app.route('/index', methods=['GET', 'POST'])

def hello():
	form = ReusableForm(request.form)

	#print(form.errors)
	if request.method == 'POST':
		present_lat=request.form['present-lat']
		present_long=request.form['present-long']
		dest_lat=request.form['dest-lat']
		dest_long=request.form['dest-long']

		print(present_lat)

	if form.validate():
		write_to_disk(present_lat, present_long, dest_lat)
		flash('Hello: {} {}'.format(present_lat, present_long))

	else:
		print('hi')

	return render_template('index.html', form=form)

# @app.route("/test-page")
# def test_page():
# 	value = 1
# 	return render_template("test.html", value=value)

if __name__ == "__main__":
	app.run(debug=True)