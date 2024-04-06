from app import app, mysql
from flask import render_template, url_for, flash, get_flashed_messages, redirect, request,session,json
from datetime import datetime
import os

import models
import forms
import DietSystem
import toHTML


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

""" BMI CALCULATOR """
@app.route('/bmi_cal',methods=['GET','POST'])
def bmi_cal():
	if request.method == "POST":
		name=request.form['name']
		gender=request.form['gender']
		h=int(request.form['Height'])
		w=int(request.form['Weight'])
		age=request.form['Age']
		t=w/h*h
		result="         Hello "+name+" your BMI is "+str(t)+" Thanks for using BMI Calculator Serviece"
		return render_template('bmi_cal.html',result=result)
	return render_template('bmi_cal.html')
""" MY BMI CALCULATOR """
@app.route('/myBMI')
def myBMI():
	if "user" in session:
		cur= mysql.connection.cursor()
		query="select fname,height,Weight,age from user where email='"+session["user"]+"'"
		cur.execute(query)
		user=cur.fetchone()
		name=user[0]
		h=int(user[1])
		w=int(user[2])
		age=user[3]
		print(name ,h ,w ,age)
		t=w/h*h
		result="         Hello "+name+" your BMI is "+str(t)+" Thanks for using BMI Calculator Serviece"
		cur.close()

		return render_template('mybmi.html',result=result)
	return render_template('bmi_cal.html')

""" END OF BMI CALCULATORS """
""" REGISTRATION FORM """

@app.route('/sign_up')
def sign_up():
	return render_template('sign-up.html')

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == "POST":
		Fname=request.form['fname']
		Lname=request.form['lname']
		email=request.form['email']
		password=request.form['password']
		address=request.form['address']
		h=int(request.form['height'])
		w=int(request.form['weight'])
		age=int(request.form['age'])
		gender=request.form['gender']
		food=request.form['food']
		act=request.form['act']

		cur= mysql.connection.cursor()
		cur.execute("insert into user (fname,lname,email, pass,address,age,height,Weight,gender,foodtype,act) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(Fname,Lname,email,password,address,age,h,w,gender,food,act))
		mysql.connection.commit()
		cur.close()
		return render_template('index.html')

"""" Login Form """
@app.route('/log-in',methods=['GET','POST'])
def log_in():
	if request.method == "POST":
		email=request.form['email']
		password=request.form['password']
		cur= mysql.connection.cursor()
		query="SELECT * FROM user WHERE email= '" + email + "' AND pass = '" + password + "'"
		cur.execute(query)
		rc=cur.rowcount
		if cur.rowcount == 1:
			mysql.connection.commit()
			res=cur.fetchone()
			session["id"]=res[0]
			print(res[0])
			cur.close()
			session['user']=email
			return redirect(url_for('Home'))
		else:
			return render_template('Log-in.html',msg="Wrong user name or password")
	return render_template('Log-in.html',msg="")
@app.route('/Home')
def Home():
	if 'user' in session:
		return render_template('home.html')
	else:
		return render_template('Log-in.html',msg="Login to home page")

#diet plan
@app.route('/createDiet')
def createDiet():
	if "user" in session:
		cur= mysql.connection.cursor()
		query="select fname,age,height,Weight,gender,act from user where email='"+session["user"]+"'"
		cur.execute(query)
		user=cur.fetchone()
		diet=DietSystem.generator(user)
		toHTML.createHTML(diet)
		f=toHTML.copy_rename(session['user'])
		#diet store in json
		cur.close()
		dietDB={}
		if os.path.exists('dietDB.json'):
			with open('dietDB.json') as diets:
				dietDB = json.load(diets)
		if session["user"] in dietDB.keys():
			flash('Diet was Already created you can see using the show food list.')
			return redirect(url_for('Home'))
		dietDB[session['user']]= {"file":f}
		with open('dietDB.json','w') as diets:
			json.dump(dietDB, diets)
		#json end
		return render_template('showDiet.html')
@app.route('/changeDiet')
def changeDiet():
	if "user" in session:
		cur= mysql.connection.cursor()
		query="select fname,age,height,Weight,gender,act from user where email='"+session["user"]+"'"
		cur.execute(query)
		user=cur.fetchone()
		diet=DietSystem.generator(user)
		toHTML.createHTML(diet)
		cur.close()
		return render_template('showDiet.html')
# Showing Diet Plan
@app.route('/myDiet')
def myDiet():
	if "user" in session:
		user=session['user']
		if os.path.exists('dietDB.json'):
			with open('dietDB.json') as diets:
				dietDB = json.load(diets)
				return render_template(dietDB[user]["file"])
#pass
""" Edit Profile"""
@app.route('/editProfile')
def editProfile():
	if "user" in session:
		cur= mysql.connection.cursor()
		query="select * from user where id='"+str(session["id"])+"'"
		cur.execute(query)
		user=cur.fetchone()
		print(user)
		cur.close()
		return render_template('editProfile.html',user=user)
#upate in db
@app.route('/update',methods=['GET','POST'])
def update():
	if request.method == "POST" :
		if "user" in session:
			id=session['id']
			Fname=request.form['fname']
			Lname=request.form['lname']
			email=request.form['email']
			password=request.form['password']
			address=request.form['address']
			h=int(request.form['height'])
			w=int(request.form['weight'])
			age=int(request.form['age'])
			cur= mysql.connection.cursor()
			cur.execute("update user set fname=%s,lname=%s,email=%s, pass=%s,address=%s,age=%s,height=%s,Weight=%s where id=%s",(Fname,Lname,email,password,address,age,h,w,id))
			mysql.connection.commit()
			cur.close()
			return redirect(url_for("home"))
"""end edit profile"""
@app.route('/Logout')
def Logout():
	if "user" in session:
		user=session.pop('user',None)
		id=session.pop('id',None)
		return render_template('index.html')
