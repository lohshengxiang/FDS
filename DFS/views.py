from flask import Blueprint, redirect, render_template, jsonify, flash, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import psycopg2
from __init__ import login_manager
from forms import LoginForm, RegistrationForm, OrderForm, RestaurantForm, PaymentForm, AddressForm, ChangePasswordForm

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

class Restaurant():
	restaurantName = None
	restaurantaddress = None

class DeliveryStaff():
	dName = None
	dRating = None

class FDSPromotion(): 
	promoId = None
	promoCode = None
	startDate = None 
	endDate = None
	name = None

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
		query = "SELECT distinct mname from FDS_Manager where uname = %s"
		cur.execute(query,(username,))
		user.firstName = cur.fetchone()[0]
	else:
		query = "SELECT * from Customer where uname = %s"
		try:
			cur.execute(query,(username,))
		except:
			conn.rollback()
		exist = cur.fetchone()
		if exist:
			user.user_type = "User"
			query = "SELECT distinct cname from Customer where uname = %s"
			cur.execute(query,(username,))
			user.firstName = cur.fetchone()[0]
		else:
			query = "SELECT * from Restaurant where uname = %s"
			try:
				cur.execute(query,(username,))
			except:
				conn.rollback()
			exist = cur.fetchone()
			if exist:
				user.user_type = "Restaurant"
				query = "SELECT distinct rname from Restaurant where uname = %s"
				cur.execute(query,(username,))
				user.firstName = cur.fetchone()[0]
			else:
				user.user_type = "Delivery_staff"
				query = "SELECT distinct dname from Delivery_Staff where uname = %s"
				cur.execute(query,(username,))
				user.firstName = cur.fetchone()[0]
	return user

@view.route("/",  methods = ["GET","POST"])
def home():
	test = False
	if current_user.is_authenticated:
		test = current_user.user_type
		userType = current_user.user_type
		if (userType == 'Restaurant'):
			return redirect ('/homeRestaurant')
		elif userType == 'Manager': 
			return redirect('/homeManager')
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

# START OF MANAGER VIEW ROUTES
@view.route("/homeManager", methods = ["GET", "POST"])
def managerHome(): 
	return render_template('homeManager.html')

@view.route("/adminManager", methods = ["GET", 'POST'])
def managerAdmin(): 
	return render_template('adminManager.html')

@view.route("/adminManager/manageRestaurants", methods = ["GET", "POST"])
def manageRestuarants():
	restaurant_list = []
	restaurantQuery = "SELECT * from Restaurant"
	cur.execute(restaurantQuery)
	restaurants = cur.fetchall()
	rname_rows = []
	address_rows = []
	for row in restaurants:
		rname_rows.append(row[1])
		address_rows.append(row[2])

	for x in range(len(rname_rows)):
		restaurant = Restaurant()
		restaurant.restaurantName = rname_rows[x]
		restaurant.restaurantAddress = address_rows[x]
		restaurant_list.append(restaurant)

	return render_template('manageRestaurants.html', restaurant_list = restaurant_list)

@view.route("/adminManager/manageDeliveryStaff", methods = ["GET", "POST"])
def manageDeliveryStaff():
	dstaff_list = []
	dstaffQuery = "SELECT * from Delivery_Staff"
	cur.execute(dstaffQuery)
	dstaff = cur.fetchall()
	dname_rows = []
	rating_rows = []
	for row in dstaff:
		dname_rows.append(row[1])
		rating_rows.append(row[2])

	for x in range(len(dname_rows)):
		dstaff = DeliveryStaff()
		dstaff.dName = dname_rows[x]
		dstaff.dRating = rating_rows[x]
		dstaff_list.append(dstaff)

	return render_template('manageDeliveryStaff.html', dstaff_list = dstaff_list)

@view.route("/adminManager/managePromo", methods = ["GET", "POST"]) 
def managePromo():
	promo_list = []

	promoQuery = "SELECT * from FDS_Promo order by PromoId"
	cur.execute(promoQuery)
	promo = cur.fetchall()
	ids_rows = []
	codes_rows = []
	sDates_rows = []
	eDates_rows = []
	names_rows = []
	for row in promo: 
		ids_rows.append(row[0])
		codes_rows.append(row[1])
		sDates_rows.append(row[2])
		eDates_rows.append(row[3])
		names_rows.append(row[4])

	for x in range(len(sDates_rows)):
		promo = FDSPromotion()
		promo.promoId = ids_rows[x]
		promo.promoCode = codes_rows[x]
		promo.startDate = sDates_rows[x]
		promo.endDate = eDates_rows[x]
		promo.name = names_rows[x]
		promo_list.append(promo)

	return render_template('managePromo.html', promo_list = promo_list)

# END OF MANAGER VIEW ROUTES

@view.route("/category/<category>", methods = ["GET","POST"])
def category(category):
	form = RestaurantForm()
	query = "SELECT distinct rname from Restaurant,Food where runame = uname and category = %s"
	# query = "SELECT distinct runame from Food where category = %s"
	try:
		cur.execute(query,(category,))
	except:
		conn.rollback()
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
	global cart_list
	global new_address

	query = "SELECT distinct uname from Restaurant where rname = %s"
	try:
		cur.execute(query,(rname,))
	except:
		conn.rollback()	

	runame = cur.fetchone()[0]

	query = "SELECT distinct fname from Food where runame = %s"
	try:
		cur.execute(query,(runame,))
	except:
		conn.rollback()	
	fname_rows = cur.fetchall() # list of tuples

	current_foods = []
	if cart_list != []:
		for i in cart_list:
			current_foods.append(i['fname'])


	#we dont want repeated foods if not primary key error in Contains
	fname_choices = []
	for row in fname_rows:
		if row[0] not in current_foods:
			fname_choices.append((row[0],row[0]))
	form.fname.choices = fname_choices

	query = "SELECT max(order_limit) from Food where runame = %s" 
	try:
		cur.execute(query,(runame,))
	except:
		conn.rollback()
	limit = int(cur.fetchone()[0])
	quantity_choices = []
	for i in range(1,limit+1):
		quantity_choices.append((str(i),i)) #id has to be string
	form.quantity.choices = quantity_choices

	
	
	if cart_list != []:
		if cart_list[0]["rname"] != rname:
			cart_list = []

	addresses = []
	if new_address != []:
		for i in new_address:
			addresses.append(i)

	query = "SELECT distinct deliveryAddress from orders where cuname = %s limit 5" #change this to order by
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
			cur.execute(query,(runame,form.fname.data))
			food_cost = int(cur.fetchone()[0]) 
			food_cost *= int(form.quantity.data) #subject to promotion

			order_date = datetime.now().strftime("%m/%d/%Y")
			
			item_dict = {'username': username,
						'rname' : rname,
						'fname' : fname,
						'quantity' : form.quantity.data,
						# 'order_time' : order_time,
						'food_cost' : food_cost}

			cart_list.append(item_dict)
			# return redirect(request.referrer)
			return redirect("/restaurant/" + rname)

	if form2.validate_on_submit() and cart_list != []:
		cuname = current_user.username
		payment_type = form2.payment_method.data
		total_cost = 0 

		for i in cart_list:
			total_cost += i["food_cost"]

		address = form2.address.data
		order_date = datetime.now().strftime("%m/%d/%Y")
		order_time = datetime.now().strftime("%H:%M:%S")
		#used to have rname in query
		query = "SELECT max(orderid) from Orders"
		cur.execute(query)
		maxid = int(cur.fetchone()[0])
		if maxid:
			newid = maxid + 1
		else:
			newid = 0
		query = '''INSERT INTO orders(orderId,cuname, payment_type, deliveryAddress,order_date,order_time,deliveryFee,foodCost) 
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
		cur.execute(query,(newid,cuname,payment_type,address,order_date,order_time,5,total_cost))
		conn.commit()

		for i in cart_list:
			query = '''INSERT INTO Contain(orderId,runame,fname,quantity) values (%s,%s,%s,%s)'''
			cur.execute(query,(newid,runame,i['fname'],i['quantity']))
			conn.commit()
		
		return redirect('/pay')

	total_cost = 0
	for i in cart_list:
		total_cost += i["food_cost"]
			
	return render_template('orders2.html', form = form, form2 = form2, 
		form3 = form3, rname = rname, current_order = cart_list, current_order_len = len(cart_list), 
		new_address = new_address, runame = runame, total_cost = total_cost, cart_list = cart_list)

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
	query = "SELECT order_limit from Food where runame = %s and fname = %s"
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
	query = '''WITH new_contains as(
	select * from Contain c1 join Restaurant r1 on c1.runame = r1.uname
	)
	select * from Orders join (select distinct orderid, rname from new_contains) c2 using (orderid) where cuname = %s order by orderid DESC'''

	# query = "SELECT * from get_orders(%s)"
	try: 
		cur.execute(query,(current_user.username,))
	except:
		conn.rollback()
	order_table = cur.fetchall() ##order_table is a list of tuples
	order_list = []
	for i in order_table:
		one_order_dict = {}
	
		#(orderId, cuname, payment_type, deliveryAddress, is_delivered, order_date, order_time, deliveryFee, foodCost, promoCode, rname) 
		one_order_dict["orderid"] = i[0]
		one_order_dict["payment_type"] = i[2]
		one_order_dict["address"] = i[3]
		one_order_dict["is_delivered"] = i[4]
		one_order_dict["order_date"] = i[5]
		one_order_dict["order_time"] = i[6]
		one_order_dict["deliveryFee"] = i[7]
		one_order_dict["foodCost"] = i[8]
		one_order_dict["promoCode"] = i[9]
		one_order_dict["rname"] = i[10]
		order_list.append(one_order_dict)
	if order_list:  
		return render_template('orders.html', status = order_list)
	else:
		return render_template('orders.html', status = 'You have no orders')
		

@view.route("/profile", methods = ["GET","POST"])
@login_required
def profile():
	#get points
	query = "SELECT distinct points from customer where uname = %s"
	cur.execute(query,(current_user.username,))
	points = int(cur.fetchone()[0])
	return render_template("profile.html", points = points)

@view.route("/profile/<nav>", methods = ["GET","POST"])
@login_required
def profile_nav(nav):
	form = ChangePasswordForm()
	if nav == "password":
		if form.validate_on_submit():
			oldPassword = form.oldPassword.data
			newPassword = form.newPassword.data

			#check old password exist
			query = "SELECT * from Users where uname = %s and password = %s"
			cur.execute(query,(current_user.username,oldPassword))
			exist = cur.fetchone()
			if not exist:
				form.oldPassword.errors.append("Wrong Password")
			else:
				query = "UPDATE Users SET password = %s where uname = %s"
				cur.execute(query,(newPassword,current_user.username))
				conn.commit()
				flash('Password changed!')
				return redirect(url_for('view.profile_nav', nav = "password"))
		return render_template("profile_password.html",form = form)
	else:
		template = "profile_" + nav + ".html"
		return render_template(template)

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

