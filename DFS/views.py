from flask import Blueprint, redirect, render_template, jsonify, flash, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import psycopg2
from __init__ import login_manager
from forms import LoginForm, RegistrationForm, OrderForm, RestaurantForm, \
PaymentForm, AddressForm, ChangePasswordForm, ReviewForm , AddCreditCardForm, \
ConfirmForm, AddAddressForm, CreditCardForm, CreatePromoForm
import base64
from datetime import datetime
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)


#global
cart_list = []
new_address = []
payment_type = ""
fixed_delivery_fee = 5
card_used = ""
points_used = 0

view = Blueprint("view", __name__)

conn = psycopg2.connect("dbname=fds2 user=postgres host = localhost password = welcome1")
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
		elif userType == 'Delivery_staff':
			return redirect('/homeDeliveryStaff')
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

@view.route("/adminManager/managePromo/createPromo", methods = ["GET", "POST"]) # not working idk why cant update DB and redirect :(
def createPromo():
	username = current_user.username
	form = CreatePromoForm()
	if form.validate_on_submit() :
		promoid = form.promoId.data
		code = form.promoCode.data
		startdate = form.start_date.data
		enddate = form.end_date.data
		promoname = form.promoName.data
		query = "INSERT INTO FDS_Promo VALUES (%s,%s,%s,%s,%s %s)"
		cur.execute(query, (promoid, code, startdate, enddate, promoname, username))
		conn.commit() 
		flash('New promotion added!')
		return redirect("/adminManager/managePromo")
	return render_template('createPromo.html', form = form)

# END OF MANAGER VIEW ROUTES

# START OF DELIVERY STAFF VIEW ROUTES

@view.route("/homeDeliveryStaff", methods = ["GET", "POST"])
def deliveryStaffHome(): 
	return render_template('homeDeliveryStaff.html')

@view.route("/deliveriesDeliveryStaff", methods = ["GET", 'POST'])
def deliveryStaffDeliveries(): 
	username = current_user.username

	#current deliveries
	currentQuery = '''WITH temp AS(
					SELECT DISTINCT orderId, runame FROM Contain
					)
					SELECT DISTINCT * FROM Orders O 
					JOIN Delivers D ON O.orderId = D.orderId 
					JOIN temp C ON C.orderId = D.orderId 
					JOIN Restaurant R ON R.uname = C.runame
					WHERE O.is_delivered = false AND D.duname = %s'''
	cur.execute(currentQuery,(username,))

	current_table = cur.fetchall()
	current_list = []
	for i in current_table:
		current_dict = {}
	
		#(orderId, rname, restaurantAddress, cuname, order_date, order_time, deliveryAddress, payment_type, total_payment, 
		# depart_restaurant, arrive_restaurant, depart_customer, arrive_customer) 
		current_dict["orderId"] = i[0]
		current_dict["rname"] = i[20]
		current_dict["restaurantAddress"] = i[21]
		current_dict["cuname"] = i[1]
		current_dict["order_date"] = i[5]
		current_dict["order_time"] = i[6]
		current_dict["deliveryAddress"] = i[3]
		current_dict["payment_type"] = i[2]
		current_dict["total_payment"] = i[7]+i[8]
		current_dict["depart_restaurant"] = i[13]
		current_dict["arrive_restaurant"] = i[14]
		current_dict["depart_customer"] = i[15]
		current_dict["arrive_customer"] = i[16]
		current_list.append(current_dict)

	#completed deliveries
	completedQuery = '''WITH temp AS(
					SELECT DISTINCT orderId, runame FROM Contain
					)
					SELECT DISTINCT * FROM Orders O 
					JOIN Delivers D ON O.orderId = D.orderId 
					JOIN temp C ON C.orderId = D.orderId 
					JOIN Restaurant R ON R.uname = C.runame
					WHERE O.is_delivered = true AND D.duname = %s'''
	cur.execute(completedQuery,(username,))

	completed_table = cur.fetchall()
	completed_list = []
	for i in completed_table:
		completed_dict = {}
	
		#(orderId, rname, restaurantAddress, cuname, order_date, order_time, deliveryAddress, payment_type, total_payment, 
		# depart_restaurant, arrive_restaurant, depart_customer, arrive_customer) 
		completed_dict["orderId"] = i[0]
		completed_dict["rname"] = i[20]
		completed_dict["restaurantAddress"] = i[21]
		completed_dict["cuname"] = i[1]
		completed_dict["order_date"] = i[5]
		completed_dict["order_time"] = i[6]
		completed_dict["deliveryAddress"] = i[3]
		completed_dict["payment_type"] = i[2]
		completed_dict["total_payment"] = i[7]+i[8]
		completed_dict["depart_restaurant"] = i[13]
		completed_dict["arrive_restaurant"] = i[14]
		completed_dict["depart_customer"] = i[15]
		completed_dict["arrive_customer"] = i[16]
		completed_dict["rating"] = i[12]
		current_list.append(current_dict)	
		
	return render_template('deliveriesDeliveryStaff.html', current_list = current_list)

@view.route("/scheduleDeliveryStaff", methods = ["GET", 'POST'])
def deliveryStaffSchedule(): 
	

	return render_template('scheduleDeliveryStaff.html')

@view.route("/ratingsDeliveryStaff", methods = ["GET", 'POST'])
def deliveryStaffRatings(): 
	username = current_user.username

	ratingQuery = "SELECT orderId, rating from Delivers where duname = %s"
	cur.execute(ratingQuery, (username,))
	ratings = cur.fetchall()
	ratings_list = []
	for row in ratings:
		ratings_dict = {}
		ratings_dict["orderId"] = row[0]
		ratings_dict["rating"] = row[1]
		ratings_list.append(ratings_dict)

	avg_ratingQuery = "SELECT avg_rating from Delivery_Staff where uname = %s"
	cur.execute(avg_ratingQuery, (username,))
	avg_rating = cur.fetchone()[0]

	return render_template('ratingsDeliveryStaff.html', ratings_list = ratings_list, avg_rating = avg_rating)

# END OF DELIVERY STAFF VIEW ROUTES

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
		return redirect('/order/' + form.rname.data)
	return render_template('category.html', form = form, category = category)

@view.route("/order/<rname>",methods = ["GET","POST"])
def order_food(rname):
	form = OrderForm()

	global cart_list
	global new_address
	global fixed_delivery_fee
	delivery_fee = fixed_delivery_fee
	new_address = []

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
			return redirect("/order/" + rname)

	total_cost = 0
	for i in cart_list:
		total_cost += i["food_cost"]
			
	return render_template('order_food.html', form = form, rname = rname,  current_order_len = len(cart_list), 
	 runame = runame, total_cost = total_cost, cart_list = cart_list, delivery_fee = delivery_fee)

@view.route("/order/<rname>/address", methods = ["GET","POST"])
def order_address(rname):
	global new_address
	global cart_list
	global fixed_delivery_fee
	delivery_fee = fixed_delivery_fee
	form = AddressForm()
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
	form.address.choices = address_choices

	total_cost = 0
	for i in cart_list:
		total_cost += i["food_cost"]

	if form.validate_on_submit():
		address = form.address.data
		new_address = [address]
		return redirect("/order/"+rname+"/payment")
	return render_template("order_address.html", form = form, new_address = new_address, 
		rname = rname, cart_list = cart_list, total_cost = total_cost, delivery_fee = delivery_fee)


@view.route("/order/<rname>/add_address", methods = ["GET","POST"])
def add_address(rname):
	global new_address
	form = AddAddressForm()
	if form.validate_on_submit(): 
		new_address.append(form.address.data)
		return redirect("/order/" + rname + "/address")

	return render_template("add_address.html", form = form)

@view.route("/order/<rname>/payment", methods = ["GET","POST"])
def order_payment(rname):
	global cart_list
	global new_address
	global payment_type
	global fixed_delivery_fee
	global points_used

	delivery_fee = fixed_delivery_fee
	form = PaymentForm()

	query = '''SELECT points from Customer where uname = %s'''
	cur.execute(query,(current_user.username,))
	points = cur.fetchone()[0]

	if form.validate_on_submit(): 
		payment_type = form.payment_method.data
		fee_boolean = form.points.data

		if fee_boolean:
			if points >= delivery_fee:
				after_points = points - delivery_fee
				delivery_fee = 0 
			else:
				delivery_fee -= points
				after_points = 0
			points_used = points - after_points
			


		if payment_type == "Credit Card":
			return redirect("/order/" + rname + "/payment/cc")
		else:
			return redirect("/order/" + rname + "/confirm")

	total_cost = 0
	for i in cart_list:
		total_cost += i["food_cost"]

	return render_template("order_payment.html", form = form, cart_list = cart_list, new_address = new_address, 
		total_cost = total_cost, rname = rname, delivery_fee = delivery_fee, points = points)

@view.route("/order/<rname>/payment/cc", methods = ["GET","POST"])
def order_cc(rname):
	form = CreditCardForm()
	global card_used

	query = '''SELECT ccNumber,cardType from CreditCard where uname = %s'''
	cur.execute(query,(current_user.username,))
	card_rows = cur.fetchall()

	card_choices = []
	for i in card_rows:
		card_choices.append((str(i[0]),'xxxxxxxxxxxx' + i[0][-4:]))
	form.cc.choices = card_choices

	if form.validate_on_submit(): 
		cc = form.cc.data
		card_used = cc
		return redirect("/order/" + rname + "/confirm")

	return render_template("order_cc.html", form = form, rname = rname)

@view.route("/order/<rname>/confirm", methods = ["GET","POST"])
def order_confirm(rname):
	form = ConfirmForm()
	global cart_list
	global new_address
	global payment_type
	global fixed_delivery_fee
	global points_used

	delivery_fee = fixed_delivery_fee - points_used

	total_cost = 0
	for i in cart_list:
		total_cost += i["food_cost"]

	if form.validate_on_submit():

		#settle Orders start

		address = new_address[0]
		order_date = datetime.now().strftime("%m/%d/%Y")
		order_time = datetime.now().strftime("%H:%M:%S")
		query = "SELECT max(orderid) from Orders"
		cur.execute(query)
		maxid = int(cur.fetchone()[0])
		if maxid:
			newid = maxid + 1
		else:
			newid = 0
		food_cost = total_cost - delivery_fee
		query = '''INSERT INTO orders(orderId,cuname, payment_type, deliveryAddress,order_date,order_time,deliveryFee,foodCost) 
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
		cur.execute(query,(newid,current_user.username,payment_type,address,order_date,order_time,delivery_fee,food_cost))
		conn.commit()

		#settle Orders end

		#settle points start
		query = '''SELECT points from Customer where uname = %s'''
		cur.execute(query,(current_user.username,))
		points = cur.fetchone()[0]

		after_points = round(points - points_used + food_cost)
		query = '''UPDATE Customer SET points = %s where uname = %s'''
		cur.execute(query,(after_points,current_user.username))
		conn.commit()

		#settle points end

		#settle Contain start

		query = "SELECT distinct uname from Restaurant where rname = %s"
		try:
			cur.execute(query,(rname,))
		except:
			conn.rollback()	

		runame = cur.fetchone()[0]

		for i in cart_list:
			query = '''INSERT INTO Contain(orderId,runame,fname,quantity) values (%s,%s,%s,%s)'''
			cur.execute(query,(newid,runame,i['fname'],i['quantity']))
			conn.commit()

		#settle Contain end


		return redirect("/done")

	return render_template("order_confirm.html", form = form, rame = rname, cart_list = cart_list, new_address = new_address[0],
		total_cost = total_cost, delivery_fee = delivery_fee, points_used = points_used, payment_type = payment_type) 



@view.route("/done", methods = ["GET","POST"])
def order_done():
	global cart_list
	global new_address
	global payment_type
	global fixed_delivery_fee
	global points_used
	cart_list = []
	new_address = []
	payment_type = ""
	card_used = ""
	points_used = 0
	return render_template('order_done.html')


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
		firstName = form.firstName.data
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
			cur.execute(query,(username,firstName))
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
		return render_template('orders.html', status = [])
		

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
	if nav == "password":
		form = ChangePasswordForm()
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
	elif nav == "pastOrders":
		query = '''WITH new_contains as(
		select * from Contain c1 join Restaurant r1 on c1.runame = r1.uname
		)
		select * from Orders join (select distinct orderid, rname from new_contains) c2 using (orderid) 
		where cuname = %s and is_delivered = True order by orderid DESC'''

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
		return render_template("profile_pastOrders.html", status = order_list)
	elif nav == "currentOrders":
		query = '''WITH new_contains as(
		select * from Contain c1 join Restaurant r1 on c1.runame = r1.uname
		)
		select * from Orders join (select distinct orderid, rname from new_contains) c2 using (orderid) 
		where cuname = %s and is_delivered = False order by orderid DESC'''

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
		return render_template("profile_currentOrders.html", status = order_list)
	elif nav == "reviews":
		query = ''' WITH new_contains as(
		select * from Contain c1 join Restaurant r1 on c1.runame = r1.uname
		) 
		SELECT distinct orderid,rname,review from new_contains join Reviews using (orderid) 
		where orderid in (SELECT orderid from Orders where cuname = %s)'''
		cur.execute(query,(current_user.username,))
		review_table = cur.fetchall()
		if review_table:
			review_list = []
			for i in review_table:
				review_dict = {}
				review_dict["orderid"] = i[0]
				review_dict["rname"] = i[1]
				review_dict["review"] = i[2]
				review_list.append(review_dict)
			return render_template("profile_reviews.html",status = review_list)
		else:
			return render_template("profile_reviews.html",status = [])

	elif nav == "addCreditCard":
		form = AddCreditCardForm()
		if form.validate_on_submit():
			cc = form.cc.data
			bank = form.bank.data
			query = '''SELECT * from CreditCard where uname = %s and ccNumber = %s'''
			cur.execute(query,(current_user.username,cc))
			exist = cur.fetchone()
			if exist:
				form.cc.errors.append("Card already exists.")
			else:
				query = "INSERT INTO CreditCard VALUES (%s,%s,%s)"
				cur.execute(query,(current_user.username,cc,bank))
				conn.commit()
				flash('Card added!')
				return redirect(url_for('view.profile_nav', nav = "addCreditCard"))
		return render_template('profile_addCreditCard.html',form = form)

	elif nav == "viewCards":
		query = ''' SELECT * from CreditCard where uname = %s'''
		#uname,ccnumber,cardtype
		cur.execute(query,(current_user.username,))
		card_table = cur.fetchall()
		if card_table:
			card_list = []
			count = 1
			for i in card_table:
				card_dict = {}
				card_dict["entry"] = count
				card_dict["ccNumber"] = i[1]
				card_dict["restricted"] = 'xxxxxxxxxxxx' + i[1][-4:]
				card_dict["bank"] = i[2]
				card_dict["encoded"] = cipher_suite.encrypt(str.encode(i[1])).decode() # this is a string
				card_list.append(card_dict)
				count = count + 1
			return render_template("profile_viewCards.html", status = card_list)
		else:
			return render_template("profile_viewCards.html", status = [])
	else:
		template = "profile_" + nav + ".html"
		return render_template(template)

@view.route("/review/<rname>/<orderid>", methods = ["GET","POST"])
@login_required
def review(rname,orderid):
	form = ReviewForm()
	if form.validate_on_submit():
		review = form.review.data
		query = "INSERT INTO Reviews VALUES (%s,%s)"
		cur.execute(query,(orderid,review))
		conn.commit()
		return redirect("/")
	return render_template("review.html", form = form, rname = rname)

@view.route("/deleteCard/<ccNumber>", methods = ["GET","POST"])
@login_required
def deleteCard(ccNumber):
	ccNumber = cipher_suite.decrypt(str.encode(ccNumber)).decode() #gets back cc Number
	form = ConfirmForm()
	if form.validate_on_submit():
		if 'Yes' in request.form.getlist('action'):
			query = '''DELETE from CreditCard where ccNumber = %s and uname = %s'''
			cur.execute(query,(ccNumber,current_user.username))
			conn.commit()
			return redirect('/profile/viewCards')
		elif 'No' in request.form.getlist('action'):
			return redirect('/profile/viewCards')

	restrict = 'xxxxxxxxxxxx' + ccNumber[-4:]
	return render_template('profile_deleteCard.html',form = form, ccNumber = restrict)
	# return redirect("/profile/viewCards")

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

