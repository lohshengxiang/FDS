from flask import Blueprint, redirect, render_template, jsonify, flash
from flask_login import current_user, login_required, login_user, logout_user
import psycopg2
from __init__ import login_manager
from forms import LoginForm, RegistrationForm, OrderForm, RestaurantForm, PaymentForm, AddressForm

from datetime import datetime

#global
cart_list = []
new_address = []

view = Blueprint("view", __name__)

conn = psycopg2.connect("dbname=fds2 user=postgres host = localhost password = password")
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

class FoodItem():
	foodName = None
	price = None
	category = None
	availability = None


@login_manager.user_loader
def load_user(username):
	user = User()
	user.username = username 
	query = "SELECT * from FDS_Manager where uname = %s"
	try:
		cur.execute(query,(username,))
	except:
		conn.rollback()
	exist = cur.fetchone()
	if exist:
		user.user_type = "Manager"
	else:
		query = "SELECT * from Customer where uname = %s"
		try:
			cur.execute(query,(username,))
		except:
			conn.rollback()
		exist = cur.fetchone()
		if exist:
			user.user_type = "User"
		else:
			query = "SELECT * from Restaurant where uname = %s"
			try:
				cur.execute(query,(username,))
			except:
				conn.rollback()
			exist = cur.fetchone()
			if exist:
				user.user_type = "Restaurant"
			else:
				user.user_type = "Delivery_staff"
	return user

@view.route("/",  methods = ["GET","POST"])
def home():
	test = False
	if current_user.is_authenticated:
		test = current_user.user_type
		userType = current_user.user_type
		if (userType == 'Restaurant'):
			return redirect ('/homeRestaurant')
	return render_template('welcome3.html', test = test)

# START OF RESTAURANT VIEW ROUTES
@view.route("/homeRestaurant", methods = ["GET","POST"])
def homePage():
	return render_template('homeRestaurant.html')

@view.route("/menuRestaurant", methods = ["GET","POST"])
def menuPage():
	username = current_user.username
	#create empty list to store all food items of restaurant
	foodItem_list = []
	nameQuery = "SELECT distinct fname from Food where runame = %s"
	cur.execute(nameQuery,(username,)) 
	nameList = cur.fetchall()

	priceQuery = "SELECT price from Food where runame = %s"
	cur.execute(priceQuery,(username,)) 
	priceList = cur.fetchall()

	categoryQuery = "SELECT category from Food where runame = %s"
	cur.execute(categoryQuery,(username,)) 
	categoryList = cur.fetchall()

	availabilityQuery = "SELECT availability from Food where runame = %s"
	cur.execute(availabilityQuery,(username,)) 
	availabilityList = cur.fetchall()

	for x in range(len(nameList)):
		item = FoodItem()
		item.foodName = nameList[x]
		item.price = priceList[x]
		item.category = categoryList[x]
		item.availability = availabilityList[x]
		foodItem_list.append(item)

	return render_template('menuRestaurant.html', foodItem_list = foodItem_list)

# END OF RESTAURANT VIEW ROUTES

@view.route("/category/<category>", methods = ["GET","POST"])
def category(category):
	form = RestaurantForm()
	query = "SELECT distinct runame from Food where category = %s"
	cur.execute(query,(category,))
	rname_rows = cur.fetchall()
	rname_choices = []
	for row in rname_rows:
		rname_choices.append((row[0],row[0]))
	form.rname.choices = rname_choices
	if form.validate_on_submit():
		return redirect('/restaurant/' + form.rname.data)
	return render_template('category.html', form = form, category = category)


@view.route("/restaurant/<rname>",methods = ["GET","POST"])
def choose_food(rname):
	form = OrderForm()
	form2 = PaymentForm()
	form3 = AddressForm()

	query = "SELECT distinct fname from Food where runame = %s"
	try:
		cur.execute(query,(rname,))
	except:
		conn.rollback()	
	fname_rows = cur.fetchall() # list of tuples
	fname_choices = []
	for row in fname_rows:
		fname_choices.append((row[0],row[0]))
	form.fname.choices = fname_choices

	query = "SELECT max(order_limit) from Food where runame = %s" 
	try:
		cur.execute(query,(rname,))
	except:
		conn.rollback()
	limit = int(cur.fetchone()[0])
	quantity_choices = []
	for i in range(1,limit+1):
		quantity_choices.append((str(i),i)) #id has to be string
	form.quantity.choices = quantity_choices

	global cart_list
	global new_address
	if cart_list != []:

		addresses = []
		if new_address != []:
			for i in new_address:
				addresses.append(i)

		query = "SELECT distinct address from orders where cuname = %s limit 5" #change this to order by
		cur.execute(query,(current_user.username,))
		address_rows = cur.fetchall()

		if address_rows:
			for i in address_rows:
				addresses.append(i[0])

		address_choices = []
		for i in addresses:
			address_choices.append((str(i),i))
		form2.address.choices = address_choices

	if form.validate_on_submit(): 
		if not current_user.is_authenticated:
			return redirect('/login')
		else:
			username = current_user.username
			order_time = datetime.now().strftime("%H:%M:%S")
			fname = form.fname.data

			# get food price
			query = "SELECT price from Food where runame = %s and fname = %s"
			cur.execute(query,(rname,form.fname.data))
			total_cost = int(cur.fetchone()[0]) 
			total_cost *= int(form.quantity.data) #subject to promotion

			order_date = datetime.now().strftime("%m/%d/%Y")
			dropoff = 1 #whats this?
			

			
			item_dict = {'username': username,
						'rname' : rname,
						'fname' : fname,
						'quantity' : form.quantity.data,
						'order_time' : order_time,
						'total_cost' : total_cost}

			cart_list.append(item_dict)
			return redirect("/restaurant/" + rname)

	if form2.validate_on_submit() and cart_list != []:
		cuname = current_user.username
		rname = rname
		payment_type = form2.payment_method.data
		total_cost = 0 # need to recalculate this by having quantity

		for i in cart_list:
			total_cost += i["total_cost"]

		address = form2.address.data
		order_date = datetime.now().strftime("%m/%d/%Y")
		order_time = datetime.now().strftime("%H:%M:%S")
		#used to have rname in query
		query = '''INSERT INTO orders(cuname, payment_type,total_cost,address,order_date,order_time) 
					VALUES (%s,%s,%s,%s,%s,%s)'''
		cur.execute(query,(cuname,payment_type,total_cost,address,order_date,order_time))
		conn.commit()
		return redirect('/pay')
			
	return render_template('orders2.html', form = form, form2 = form2, 
		form3 = form3, rest = rname, current_order = cart_list, current_order_len = len(cart_list), 
		new_address = new_address)

@view.route("/<rname>/add_address", methods = ["GET","POST"])
def add_address(rname):
	global new_address
	form = AddressForm()
	if form.validate_on_submit(): 
		new_address.append(form.address.data)
		return redirect("/restaurant/" + rname)

	return render_template("add_address.html", form = form)


@view.route("/pay", methods = ["GET","POST"])
def pay():
	global cart_list
	cart_list = []
	global new_address
	new_address = []
	return render_template('pay.html')


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
			try:
			    cur.execute(query,(form.username.data,))
			except Exception:
			    conn.rollback()
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



@view.route('/quantity/<fname>/<rname>')
def quantity(fname,rname):
	query = "SELECT order_limit from Food where rname = %s and fname = %s"
	cur.execute(query,(rname,fname))
	limit = int(cur.fetchone()[0])

	quantityArray = []
	for i in range(1,limit+1):
		quantityObj = {}
		quantityObj['id'] = i
		quantityObj['quantity'] = i
		quantityArray.append(quantityObj)
	return jsonify({'quantity':quantityArray})



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
			query = "INSERT INTO Customer VALUES (%s,%s,0)"
			cur.execute(query,(username,username))
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
	# query = "SELECT * from orders where cuname = %s"
	# cur.execute(query,(current_user.username,))
	# order_table = cur.fetchall() #order_table is a list of tuples

	query = "SELECT * from get_orders(%s)"
	try: 
		cur.execute(query,(current_user.username,))
	except:
		conn.rollback()
	order_table = cur.fetchall() ##order_table is a list of tuples
	if order_table:  
		return render_template('orders.html', status = order_table)
	else:
		return render_template('orders.html', status = 'You have no orders')
		
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

