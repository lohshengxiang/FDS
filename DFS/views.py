from flask import Blueprint, redirect, render_template, jsonify, flash
from flask_login import current_user, login_required, login_user, logout_user
import psycopg2
from __init__ import login_manager
from forms import LoginForm, RegistrationForm, OrderForm


from datetime import datetime

#global
cart_list = []

view = Blueprint("view", __name__)

conn = psycopg2.connect("dbname=postgres user=postgres host = localhost password = welcome1")
cur = conn.cursor()

class User():
	username = None
	firstName = None
	user_type = None

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username


@login_manager.user_loader
def load_user(username):
	user = User()
	user.username = username 
	user.user_type = "User"
	return user

@view.route("/",  methods = ["GET","POST"])
def home():
	return render_template('welcome3.html')

@view.route("/japanese", methods = ["GET","POST"])
def japanese():
	form = OrderForm()
	query = "SELECT distinct rname from Food where category = 'Japanese'"
	cur.execute(query)
	rname_rows = cur.fetchall() # list of tuples
	rname_choices = []
	for row in rname_rows:
		rname_choices.append((row[0],row[0]))
	form.rname.choices = rname_choices 

	# get fnames
	# query = "SELECT distinct fname from Food where category = 'Japanese'" #issue here that wont submit form if food not jap
	query = "SELECT distinct fname from Food"
	cur.execute(query)
	fname_rows = cur.fetchall()
	fname_choices = []
	for row in fname_rows:
		fname_choices.append((row[0],row[0]))
	form.fname.choices = fname_choices

	#create order
	if form.validate_on_submit():
		if not current_user.is_authenticated:
			return redirect('/login')
		else:
			username = current_user.username
			rname = form.rname.data
			order_time = datetime.now().strftime("%H:%M:%S")
			payment_type = "CC"

			# get food price
			query = "SELECT price from Food where rname = %s and fname = %s"
			cur.execute(query,(form.rname.data,form.fname.data))
			total_cost = int(cur.fetchone()[0])

			order_date = datetime.now().strftime("%m/%d/%Y")
			dropoff = 1 #whats this?
			date = datetime.now().strftime("%m/%d/%Y")
			time = datetime.now().strftime("%H:%M:%S")

			cart_list.append((username,rname,order_time,payment_type,total_cost,order_date,dropoff,date,time)) #insert tuple
			# query = '''INSERT INTO orders(orderid, username, payment_method, order_time) \
			# VALUES (%s ,%s, %s, %s)'''
			# cur.execute(query,(orderid,username,payment_method,order_time,))
			# conn.commit()
			return redirect("/cart")
	return render_template('japanese.html', form = form)

@view.route("/cart", methods = ["GET","POST"])
def cart():
	return render_template('added_cart.html',cart_list = cart_list)


@view.route("/login", methods = ["GET","POST"])
def login():
	if current_user.is_authenticated:
		logout_user()
	form = LoginForm()
	if form.validate_on_submit():
		query = '''SELECT * from Users where uname = %s;'''
		cur.execute(query,(form.username.data,))
		user_exist = cur.fetchone() #checks the web_user db for user
		if user_exist: #is the user exists. i.e. he signed up before
			query = '''SELECT password FROM Users WHERE uname = %s'''
			cur.execute(query,(form.username.data,))
			password = cur.fetchone()[0]
			if password == form.password.data:
				user = User()
				user.username = form.username.data 
				login_user(user) #so we can access WebUser object with its attributes
				return redirect("/")
			else:
				form.password.errors.append("Wrong Password")
		else:
			form.username.errors.append("Invalid Username")
	return render_template("login3.html", form=form)



@view.route('/fname/<rname>')
def fname(rname):
	query = "SELECT fname from Food where rname = %s"
	cur.execute(query,(rname,))
	fname_rows = cur.fetchall()
	fname_choices = []

	for row in fname_rows:
		fname_choices.append((row[0],row[0]))
	
	fnameArray = []
	for row in fname_rows:
		fnameObj = {}
		fnameObj['id'] = row[0] #id is pizza
		fnameObj['fname'] = row[0] #fname also pizza
		fnameArray.append(fnameObj)
	return jsonify({'fname':fnameArray})

@view.route("/registration", methods = ["GET","POST"])
def registration():
	form = RegistrationForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		query = '''SELECT * FROM Users WHERE uname = %s'''
		cur.execute(query,(username,))
		exists_user = cur.fetchone()
		if exists_user:
			form.username.errors.append("{} is already in use.".format(username))
		else:
			query = "INSERT INTO Users VALUES (%s,%s)"
			cur.execute(query,(username,password))
			conn.commit()
			user = User()
			user.username = form.username.data
			login_user(user)
			return redirect("/registration_complete")
	return render_template('registration3.html', form = form)

@view.route("/registration_complete")
def registration_complete():
	return render_template('registration_complete.html')

@view.route("/orders")
@login_required
def orders():
	query = "SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' and table_name = 'Orders'"
	cur.execute(query)
	exists_table = cur.fetchone()
	if exists_table:
		query = "SELECT * from orders where username = %s"
		cur.execute(query,(current_user.username,))
		order_table = cur.fetchall()
		return render_template('orders.html', boolean = order_table)
	else:
		return render_template('orders.html', boolean = False)
		
@view.route("/logout", methods = ["GET"])
@login_required
def logout():
	logout_user()
	return render_template('logout.html')

@view.route("/restaurants", methods = ["GET","POST"])
def restaurants():
	return render_template('restaurants2.html')



@view.route("/exit",methods = ["GET"])
def exit():
	cur.close()
	conn.close()
	return "<h2>EXIT</h2>"

