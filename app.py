from flask import Flask, render_template, Response, request, url_for, redirect
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
import base64
import numpy as np
import pandas as pd
import sqlite3, os
import datetime, re
from werkzeug import secure_filename
import cv2
import sys
import pytesseract
import demo


UPLOAD_FOLDER = 'static/userUploads'
ALLOWED_EXTENSIONS = {'jpg'}

def expense_calc(spent, limit):
	vals = [spent, limit-spent]
	labs = ['Spent', 'Available']
	colors = ("red", "green")
	figureObject, axesObject = plt.subplots()
	wedges, texts = axesObject.pie(vals, labels = labs, colors = colors, wedgeprops = dict(width = 0.3), startangle = 90)
	plt.savefig('static/Images/limits_plot.png')

	figfile = BytesIO()
	plt.savefig(figfile, format='png')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue()).decode()
	return figdata_png;

def daily_calc(df):
	fig, ax = plt.subplots()
	ax.plot('x', 'y' , data = df, linestyle = '-', marker = 'o')
	plt.savefig('static/Images/daily_plot.png')

	figfile = BytesIO()
	plt.savefig(figfile, format='png')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue()).decode()
	return figdata_png;

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/dashboard')
def Dashboard():
	x = datetime.datetime.now()
	month = "__-" + x.strftime("%m") + "-" + x.strftime("%Y")
	conn = sqlite3.connect('static/database.db')
	expense_limit = 10
	expense_made = 1
	res = conn.execute("select lim from users where email = 'abc@abc.com' ")
	for row in res:
		expense_limit = int(row[0], 10)
	res = conn.execute("select sum(value) from expenses where email = ? and added like ? ", ('abc@abc.com', month) )
	for row in res:
		expense_made = row[0]
	if expense_made is None:
		expense_made = 0
	expense_graph = expense_calc(expense_made, expense_limit)

	
	dates = []
	expenses = []
	
	res = conn.execute("select  added, sum(value) from expenses where email = ? and added like ? group by added" , ('abc@abc.com', month))
	for row in res:
		expenses.append(row[1])
		d = row[0]
		dates.append(d[0:2])
	data = {'x' : dates, 'y' : expenses}
	df = pd.DataFrame(data)
	daily_graph = daily_calc(df)
	return render_template('dashboard.html', limit = expense_limit, done = expense_made, expense = expense_graph, daily = daily_graph)

@app.route('/limitUpdate', methods = ['POST'])
def changeLimit():
	new_limit = 0
	if request.method == 'POST':
		result = request.form['newLimit'];
		new_limit = int(result, 10)
		conn = sqlite3.connect('static/database.db')
		conn.execute("Update users set lim = ? where name = ?" , (result, 'abc'))
		conn.commit()
	return render_template('updated_limit.html');

@app.route('/addExpense')
def addExpense():
	return render_template('add_expense.html')

@app.route('/evaluate', methods = ['POST' , 'GET'])
def evaluate():
	if request.method == 'POST':
		f = request.files['file']
		filename = 'receipt.jpg'
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		text = demo.imageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		text = text.lower()
		scanned_text = text
		res = text.rfind('total')
		text = text[res+6:]
		text = text.split()
		# con = sqlite3.connect('static/database.db')
		# x = datetime.datetime.now()
		# con.execute("INSERT INTO scans VALUES (?, ?, ?)", (x, scanned_text, text[0]))
		# con.commit()
	return render_template('scanned.html', total = text[0])

@app.route('/evalFinal', methods = ['POST'])
def finalEval():
	if request.method == 'POST' :
		total = request.form['total']
		con = sqlite3.connect('static/database.db')
		x = datetime.datetime.now()
		d = x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y")
		con.execute("INSERT INTO expenses VALUES (?, ?, ?)", ('abc@abc.com', d, total))
		con.commit()
		return redirect(url_for('Dashboard'))

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

if __name__=='__main__':
	app.run(debug=True)