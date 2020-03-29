from flask import Blueprint, redirect, render_template, jsonify, flash, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import psycopg2
from __init__ import login_manager
from forms import LoginForm, RegistrationForm, OrderForm, RestaurantForm, \
PaymentForm, AddressForm, ChangePasswordForm, ReviewForm , AddCreditCardForm, \
ConfirmForm, AddAddressForm, CreditCardForm, CreatePromoForm, CreateRestaurantForm, \
CreateDeliveryStaffForm, CreateFoodItemForm, PromoForm, RateForm, FilterGeneralSummaryForm, \
FilterCustomerSummaryForm, FilterDeliverySummaryForm, FilterDeliveryStaffSummaryForm, ScheduleFormPT
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import calendar

key = Fernet.generate_key()
cipher_suite = Fernet(key)


#global
cart_list = []
new_address = []
payment_type = ""
fixed_delivery_fee = 5
card_used = ""
points_used = 0
promo_used = ""
promo_action = ""
nextWeekSchedules_list = []
submittedSchedule = False


# available_FT_list = []

view = Blueprint("view", __name__)

#change password before running
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
	fname = None
	price = None
	category = None
	availability = None

class Restaurant():
	runame = None 
	restaurantName = None
	restaurantaddress = None

class DeliveryStaff():
	duname = None
	dName = None
	dRating = None

class FDSPromotion(): 
	promoId = None
	promoCode = None
	startDate = None 
	endDate = None
	name = None

class Promotion():
	promoId = None
	start_date = None
	end_date = None
	message = None	

class DeliverySummary(): 
	north = None
	north_east = None
	east = None 
	west = None
	central = None
	time = None

# class Shift():
# 	shift_a_start = None
# 	shift_a_end = None
# 	shift_b_start = None
# 	shift_b_end = None

# shift1 = Shift()
# shift1.shift_a_start = '10:00:00'
# shift1.shift_a_end = '14:00:00'
# shift1.shift_b_start = '15:00:00'
# shift1.shift_b_end = '19:00:00'

# shift2 = Shift()
# shift2.shift_a_start = '11:00:00'
# shift2.shift_a_end = '15:00:00'
# shift2.shift_b_start = '16:00:00'
# shift2.shift_b_end = '20:00:00'

# shift3 = Shift()
# shift3.shift_a_start = '12:00:00'
# shift3.shift_a_end = '16:00:00'
# shift3.shift_b_start = '17:00:00'
# shift3.shift_b_end = '21:00:00'

# shift4 = Shift()
# shift3.shift_a_start = '13:00:00'
# shift3.shift_a_end = '17:00:00'
# shift3.shift_b_start = '18:00:00'
# shift3.shift_b_end = '22:00:00'

shift_dict = { "shift1" : ['10:00:00','14:00:00','15:00:00','19:00:00'],
				"shift2" : ['11:00:00','15:00:00','16:00:00','20:00:00'],
				"shift3" : ['12:00:00', '16:00:00', '17:00:00','21:00:00'],
				"shift4" : ['13:00:00', '17:00:00', '18:00:00', '22:00:00']}


day_option_dict = { 1 : ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], 
					2 : ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
					3 : ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
					4 : ["Monday", "Thursday", "Friday", "Saturday", "Sunday"],
					5 : ["Monday", "Tuesday", "Friday", "Saturday", "Sunday"],
					6 : ["Monday", "Tuesday", "Wednesday", "Saturday", "Sunday"],
					7 : ["Monday", "Tuesday", "Wednesday", "Thursday", "Sunday"]}


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
	foodItem_list = []
	foodItemQuery = "SELECT * from Food where runame = %s"
	cur.execute(foodItemQuery,(username,)) 
	food = cur.fetchall()
	fname_rows = []
	price_rows = []
	category_rows = []
	availability_rows = []

	for row in food:
		fname_rows.append(row[1])
		price_rows.append(row[3])
		category_rows.append(row[5])
		availability_rows.append(row[2])

	for x in range(len(fname_rows)):
		foodItem = FoodItem()
		foodItem.fname = fname_rows[x]
		foodItem.price = price_rows[x]
		foodItem.category = category_rows[x]
		foodItem.availability = availability_rows[x]
		foodItem_list.append(foodItem)

	return render_template('menuRestaurant.html', foodItem_list = foodItem_list)

@view.route("/addFoodItem", methods = ["POST"])
def addFoodItem():
	form = CreateFoodItemForm()
	if form.validate_on_submit() and request.method == "POST":
		fname = form.fname.data
		price = form.price.data
		order_limit = form.order_limit.data
		category = form.category.data
		runame = current_user.username
		availability = form.availability.data
		query = "INSERT INTO Food VALUES (%s,%s,%s,%s,%s, %s)"
		cur.execute(query, (runame, fname, availability, price, order_limit, category,))

		conn.commit() 
		#flash('New food item added!')
		return redirect("/menuRestaurant")
	return render_template('addFoodItem.html', form = form)

@view.route("/delete_foodItem/<string:fname>", methods=["POST"])
def delete_foodItem(fname): 
	cur.execute("DELETE FROM Food WHERE fname = %s", [fname])
	conn.commit()
	return redirect("/menuRestaurant")

@view.route("/adminRestaurant", methods = ["GET", 'POST'])
def adminRestaurant(): 
	return render_template('adminRestaurant.html')

@view.route("/adminRestaurant/managePromotions", methods = ["GET", "POST"])
def manageRestaurantPromotions():
	username = current_user.username
	promos_list = []
	promoQuery = "SELECT * from Promotion WHERE runame = %s"
	cur.execute(promoQuery,(username,)) 
	promos = cur.fetchall()
	promoid_rows = []
	start_date_rows = []
	end_date_rows = []
	message_rows = []

	for row in promos:
		promoid_rows.append(row[0])
		start_date_rows.append(row[1])
		end_date_rows.append(row[2])
		message_rows.append(row[3])

	for x in range(len(promoid_rows)):
		promotion = Promotion()
		promotion.promoId = promoid_rows[x]
		promotion.start_date = start_date_rows[x]
		promotion.end_date = end_date_rows[x]
		promotion.message = message_rows[x]
		promos_list.append(promotion)

	return render_template('managePromotions.html', promos_list = promos_list)

@view.route("/delete_restaurant_promo/<string:id>", methods=["POST"])
def delete_restaurant_promo(id): 
	cur.execute("DELETE FROM Promotion WHERE uname = %s", [id])
	conn.commit()
	return redirect(url_for('view.managePromotions'))

# END OF RESTAURANT VIEW ROUTES

# START OF MANAGER VIEW ROUTES
@view.route("/homeManager", methods = ["GET", "POST"])
def managerHome(): 
	return render_template('Manager/homeManager.html')

@view.route("/adminManager", methods = ["GET", 'POST'])
def managerAdmin(): 
	return render_template('Manager/adminManager.html')

@view.route("/adminManager/manageRestaurants", methods = ["GET", "POST"])
def manageRestaurants():
	restaurant_list = []
	restaurantQuery = "SELECT * from Restaurant"
	cur.execute(restaurantQuery)
	restaurants = cur.fetchall()
	runame_rows = []
	rname_rows = []
	address_rows = []
	for row in restaurants:
		runame_rows.append(row[0])
		rname_rows.append(row[1])
		address_rows.append(row[2])

	for x in range(len(rname_rows)):
		restaurant = Restaurant()
		restaurant.runame = runame_rows[x]
		restaurant.restaurantName = rname_rows[x]
		restaurant.restaurantAddress = address_rows[x]
		restaurant_list.append(restaurant)

	return render_template('Manager/manageRestaurants.html', restaurant_list = restaurant_list)

@view.route("/delete_restaurant/<string:runame>", methods=["POST"])
def delete_restaurant(runame): 
	cur.execute("DELETE FROM Users WHERE uname = %s", [runame])
	conn.commit()
	return redirect(url_for('view.manageRestaurants'))

@view.route("/adminManager/manageDeliveryStaff", methods = ["GET", "POST"])
def manageDeliveryStaff():
	dstaff_list = []
	dstaffQuery = "SELECT * from Delivery_Staff" #avg rating need to query from delivers not dstaff
	cur.execute(dstaffQuery)
	dstaff = cur.fetchall()
	duname_rows = []
	dname_rows = []
	rating_rows = []
	for row in dstaff:
		duname_rows.append(row[0])
		dname_rows.append(row[1])
		rating_rows.append(row[2])

	for x in range(len(dname_rows)):
		dstaff = DeliveryStaff()
		dstaff.duname = duname_rows[x]
		dstaff.dName = dname_rows[x]
		dstaff.dRating = rating_rows[x]
		dstaff_list.append(dstaff)

	return render_template('Manager/manageDeliveryStaff.html', dstaff_list = dstaff_list)

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

	return render_template('Manager/managePromo.html', promo_list = promo_list)


@view.route("/delete_promo/<string:id>", methods=["POST"])
def delete_promo(id): 
	cur.execute("DELETE FROM FDS_Promo WHERE promoId = %s", [id])
	conn.commit()
	return redirect(url_for('view.managePromo'))

@view.route("/adminManager/managePromo/createPromo", methods = ["GET", "POST"]) 
def createPromo():
	form = CreatePromoForm()
	if form.validate_on_submit() and request.method == "POST":
		promoId = form.promoId.data
		promoCode = form.promoCode.data
		start_date = form.start_date.data
		end_date = form.end_date.data
		name = form.name.data
		query = "INSERT INTO FDS_Promo VALUES (%s,%s,%s,%s,%s, %s)"
		cur.execute(query, (promoId, promoCode, start_date, end_date, name, current_user.username,))

		conn.commit() 
		return redirect("/adminManager/managePromo")
	return render_template('Manager/createPromo.html', form = form)

@view.route("/adminManager/manageRestaurants/createRestaurant", methods =["GET", "POST"])
def createRestaurant():
	form = CreateRestaurantForm()
	if form.validate_on_submit() and request.method == "POST":
		uname = form.uname.data
		rname = form.rname.data
		address = form.address.data
		min_amt = form.min_amt.data
		password = form.password.data
		query1 = "INSERT INTO Users VALUES(%s,%s)"
		cur.execute(query1, (uname, password))
		conn.commit()
		query2 = "INSERT INTO Restaurant VALUES(%s,%s,%s,%s)"
		cur.execute(query2, (uname, rname, address, min_amt))
		conn.commit()
		return redirect("/adminManager/manageRestaurants")
	return render_template('Manager/createRestaurant.html', form = form)

@view.route("/adminManager/manageDeliveryStaff/createDeliveryStaff", methods=["GET", "POST"])
def createDeliveryStaff(): 
	form = CreateDeliveryStaffForm()
	if form.validate_on_submit() and request.method == "POST":
		uname = form.uname.data
		password = form.password.data
		dname = form.dname.data
		flatRate = form.flatRate.data
		staffType = form.staffType.data
		avgRating = 0
		query1 = "INSERT INTO Users VALUES(%s, %s)"
		cur.execute(query1, (uname, password))
		conn.commit()
		query2 = "INSERT INTO Delivery_Staff VALUES(%s, %s, %s, %s)"
		cur.execute(query2, (uname, dname, avgRating, flatRate))
		conn.commit()
		if staffType.lower() == "Full Time".lower(): 
			query3 = "INSERT INTO Full_Time VALUES(%s)"
			cur.execute(query3, (uname,))
			conn.commit()
		else: 
			query3 = "INSERT INTO Part_Time VALUES(%s)"
			cur.execute(query3, (uname,))
			conn.commit()
		return redirect("/adminManager/manageDeliveryStaff")
	return render_template('Manager/createDeliveryStaff.html', form = form)

@view.route("/delete_deliveryStaff/<string:duname>", methods=["POST"])
def delete_DeliveryStaff(duname): 
	cur.execute("DELETE FROM Users WHERE uname = %s", [duname])
	conn.commit()
	return redirect(url_for('view.manageDeliveryStaff'))

@view.route("/homeManager/generalSummary", methods =["GET", "POST"])
def generalSummary():
	form = FilterGeneralSummaryForm()

	totalCustomers = 0
	totalOrders = 0
	totalCost = 0 #food cost + delivery fee

	if form.validate_on_submit() and request.method == "POST":
		month = form.month.data
		year = form.year.data
		query = "SELECT count(uname) FROM Customer WHERE EXTRACT(YEAR FROM date_created) = %s and EXTRACT(MONTH FROM date_created) = %s"
		cur.execute(query, (year, month))
		totalCustomers = cur.fetchone()[0]

		query1 = "SELECT count(orderId) from Orders WHERE EXTRACT(YEAR FROM order_date) = %s and EXTRACT(MONTH FROM order_date) = %s"
		cur.execute(query1, (year, month))
		totalOrders = cur.fetchone()[0]

		query2 = "SELECT sum(foodCost) FROM Orders WHERE EXTRACT(YEAR FROM order_date) = %s and EXTRACT(MONTH FROM order_date) = %s"
		cur.execute(query2, (year, month))
		foodCost = cur.fetchone()[0]
		if foodCost is not None: 
			totalCost = foodCost
		query3 = "SELECT sum(deliveryFee) FROM Orders WHERE EXTRACT(YEAR FROM order_date) = %s and EXTRACT(MONTH FROM order_date) = %s"
		cur.execute(query3, (year, month))
		dFee = cur.fetchone()[0]
		if dFee is not None: 
			totalCost += dFee
		return render_template('Manager/generalSummary.html', form = form, totalCustomers = totalCustomers, totalOrders = totalOrders, totalCost = totalCost)

	return render_template('Manager/generalSummary.html', form = form, totalCustomers = totalCustomers, totalOrders = totalOrders, totalCost = totalCost)

@view.route("/homeManager/customerSummary", methods =["GET", "POST"])
def customerSummary():
	form = FilterCustomerSummaryForm()
	customer_list = []
	customers = []
	customerQuery = "SELECT uname from Customer"
	cur.execute(customerQuery)
	customers = cur.fetchall()
	for row in customers: 
		customer_list.append(row[0])

	form.customer.choices = [(c, c) for c in customer_list]

	total_orders = 0
	total_cost = 0 #food cost + delivery fee from Orders

	if form.validate_on_submit() and request.method == "POST":
		month = form.month.data
		year = form.year.data
		uname = form.customer.data
		query = "SELECT count(orderId) FROM Orders WHERE cuname =%s and EXTRACT(YEAR FROM order_date) = %s and EXTRACT(MONTH FROM order_date) = %s"
		cur.execute(query, (uname,year,month))
		total_orders = cur.fetchone()[0]
		query1 = "SELECT sum(foodCost) FROM Orders WHERE cuname =%s and EXTRACT(YEAR FROM order_date) = %s and EXTRACT(MONTH FROM order_date) = %s"
		cur.execute(query1, (uname,year,month))
		foodCost = cur.fetchone()[0]
		if foodCost is not None: 
			total_cost = foodCost 
		query2 = "SELECT sum(deliveryFee) FROM Orders WHERE cuname =%s and EXTRACT(YEAR FROM order_date) = %s and EXTRACT(MONTH FROM order_date) = %s"
		cur.execute(query2, (uname,year,month))
		deliveryFee = cur.fetchone()[0]
		if deliveryFee is not None: 
			total_cost += deliveryFee
		return render_template('Manager/customerSummary.html', form = form, total_orders = total_orders, total_cost = total_cost)

	return render_template('Manager/customerSummary.html', form = form, total_orders = total_orders, total_cost = total_cost)

@view.route("/homeManager/deliverySummary", methods =["GET", "POST"])
def deliverySummary():
	form = FilterDeliverySummaryForm()
	summary_list = []
	summary = DeliverySummary()
	time_list = (('00:00:00', '01:00:00'), ('01:00:00', '02:00:00'), ('02:00:00', '03:00:00'), ('03:00:00', '04:00:00'), ('04:00:00', '05:00:00'), 
		('05:00:00', '06:00:00'), ('06:00:00', '07:00:00'), ('07:00:00', '08:00:00'), ('08:00:00', '09:00:00'), ('09:00:00', '10:00:00'), ('10:00:00', '11:00:00'), 
		('11:00:00', '12:00:00'), ('12:00:00', '13:00:00'), ('13:00:00', '14:00:00'), ('14:00:00', '15:00:00'), ('15:00:00', '16:00:00'), ('16:00:00', '17:00:00'), 
		('17:00:00', '18:00:00'), ('18:00:00', '19:00:00'), ('19:00:00', '20:00:00'), ('20:00:00', '21:00:00'), ('21:00:00', '22:00:00'), ('22:00:00', '23:00:00'), ('23:00:00', '24:00:00'))

	if form.validate_on_submit() and request.method == "POST":
		date = form.date.data
		for x, y in time_list: 
			summary = DeliverySummary() 
			summary.time = x
			query1 = "SELECT count(orderId) FROM Orders WHERE area ='West' and order_date =%s and order_time >= %s and order_time < %s"
			cur.execute(query1, (date,x,y))
			summary.west = cur.fetchone()[0]
			query2 = "SELECT count(orderId) FROM Orders WHERE area ='East' and order_date = %s and order_time >= %s and order_time < %s"
			cur.execute(query2, (date,x,y))
			summary.east = cur.fetchone()[0]
			query3 = "SELECT count(orderId) FROM Orders WHERE area ='North' and order_date = %s and order_time >= %s and order_time < %s"
			cur.execute(query3, (date,x,y))
			summary.north = cur.fetchone()[0]
			query4 = "SELECT count(orderId) FROM Orders WHERE area ='Central' and order_date = %s and order_time >= %s and order_time < %s"
			cur.execute(query4, (date,x,y))
			summary.central = cur.fetchone()[0]
			query5 = "SELECT count(orderId) FROM Orders WHERE area ='North-East' and order_date = %s and order_time >= %s and order_time < %s"
			cur.execute(query5, (date,x,y))
			summary.north_east = cur.fetchone()[0]
			summary_list.append(summary)
		return render_template('Manager/deliverySummary.html', form = form, summary_list = summary_list)
	return render_template('Manager/deliverySummary.html', form = form, summary = summary)

@view.route("/homeManager/deliveryStaffSummary", methods =["GET", "POST"])
def deliveryStaffSummary():
	form = FilterDeliveryStaffSummaryForm() 
	dstaff_list = []
	riders = []
	dstaffQuery = "SELECT uname from Delivery_Staff"
	cur.execute(dstaffQuery)
	riders = cur.fetchall()
	for row in riders: 
		dstaff_list.append(row[0])

	form.rider.choices = [(r, r) for r in dstaff_list]

	if form.validate_on_submit() and request.method == "POST":
		uname = form.year.rider

	return render_template('Manager/deliveryStaffSummary.html', form = form)

# END OF MANAGER VIEW ROUTES

# START OF DELIVERY STAFF VIEW ROUTES

@view.route("/homeDeliveryStaff", methods = ["GET", "POST"])
def deliveryStaffHome(): 
	return render_template('homeDeliveryStaff.html')

@view.route("/deliveriesDeliveryStaff", methods = ["GET", "POST"])
def deliveryStaffDeliveries(): 
	return render_template('deliveriesDeliveryStaff.html')

@view.route("/deliveriesDeliveryStaff/currentDeliveries", methods = ["GET", 'POST'])
def deliveryStaffCurrentDeliveries(): 
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
		current_dict["rname"] = i[22]
		current_dict["restaurantAddress"] = i[23]
		current_dict["cuname"] = i[1]
		current_dict["order_date"] = i[7]
		current_dict["order_time"] = i[8]
		current_dict["deliveryAddress"] = i[3]
		current_dict["payment_type"] = i[2]
		current_dict["total_payment"] = i[9]+i[10]
		current_dict["depart_restaurant"] = i[15]
		current_dict["arrive_restaurant"] = i[16]
		current_dict["depart_customer"] = i[17]
		current_dict["arrive_customer"] = i[18]
		current_list.append(current_dict)

	return render_template('currentDeliveries.html', current_list = current_list)

@view.route("/update_departRestaurant/<string:orderId>", methods=["POST"])
def update_departRestaurant(orderId): 
	cur.execute("UPDATE Delivers SET depart_restaurant = %s WHERE orderId = %s", [datetime.now().strftime("%H:%M:%S"), orderId])
	conn.commit()
	return redirect(url_for('view.deliveryStaffCurrentDeliveries'))

@view.route("/update_arriveRestaurant/<string:orderId>", methods=["POST"])
def update_arriveRestaurant(orderId): 
	cur.execute("UPDATE Delivers SET arrive_restaurant = %s WHERE orderId = %s", [datetime.now().strftime("%H:%M:%S"), orderId])
	conn.commit()
	return redirect(url_for('view.deliveryStaffCurrentDeliveries'))

@view.route("/update_departCustomer/<string:orderId>", methods=["POST"])
def update_departCustomer(orderId): 
	cur.execute("UPDATE Delivers SET depart_customer = %s WHERE orderId = %s", [datetime.now().strftime("%H:%M:%S"), orderId])
	conn.commit()
	return redirect(url_for('view.deliveryStaffCurrentDeliveries'))

@view.route("/update_arriveCustomer/<string:orderId>", methods=["POST"])
def update_arriveCustomer(orderId): 
	cur.execute("UPDATE Delivers SET arrive_customer = %s WHERE orderId = %s", [datetime.now().strftime("%H:%M:%S"), orderId])
	conn.commit()
	return redirect(url_for('view.deliveryStaffCurrentDeliveries'))		

@view.route("/complete_delivery/<string:orderId>", methods=["POST"])
def complete_delivery(orderId): 
	cur.execute("UPDATE Orders SET is_delivered = true WHERE orderId = %s", [orderId])
	conn.commit()
	return redirect(url_for('view.deliveryStaffCurrentDeliveries'))

@view.route("/deliveriesDeliveryStaff/completedDeliveries", methods = ["GET", 'POST'])
def deliveryStaffCompletedDeliveries(): 
	username = current_user.username

	#completed deliveries
	# orderid 0|  cuname  1 | payment_type 2 |        deliveryaddress    3     | deliverypostalcode 4 |    area  5  | is_delivered 6 | 
	# order_date 7| order_time 8| deliveryfee 9| foodcost 10| promocode 11| orderid 12|  duname  13 | rating 14 | depart_restaurant 15 | 
	# arrive_restaurant 16 | depart_customer 17| arrive_customer 18| orderid 19|   runame  20  |    uname   21 |    rname  22  | address 23 | min_amt 24
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
		completed_dict["rname"] = i[22]
		completed_dict["restaurantAddress"] = i[23]
		completed_dict["cuname"] = i[1]
		completed_dict["order_date"] = i[7]
		completed_dict["order_time"] = i[8]
		completed_dict["deliveryAddress"] = i[3]
		completed_dict["payment_type"] = i[2]
		completed_dict["total_payment"] = i[9]+i[10]
		completed_dict["depart_restaurant"] = i[15]
		completed_dict["arrive_restaurant"] = i[16]
		completed_dict["depart_customer"] = i[17]
		completed_dict["arrive_customer"] = i[18]
		completed_dict["rating"] = i[14]
		completed_list.append(completed_dict)	
		
	return render_template('completedDeliveries.html', completed_list = completed_list)

@view.route("/scheduleDeliveryStaff", methods = ["GET", 'POST'])
def deliveryStaffSchedules(): 
	return render_template('scheduleDeliveryStaff.html')

@view.route("/scheduleDeliveryStaff/pastWorkSchedule", methods = ["GET", 'POST'])
def deliveryStaffPastWorkSchedules(): 
	username = current_user.username
	staffType = ""

	#if part time
	checkPartTime = "SELECT * FROM Part_Time WHERE duname = %s"
	cur.execute(checkPartTime, (username,))
	if len(cur.fetchall()) != 0:
		staffType = "Part_Time"
		scheduleQuery = "SELECT * FROM WWS WHERE duname = %s"
		cur.execute(scheduleQuery, (username,))
		schedules = cur.fetchall()
		schedules_list = []
		for row in schedules:
			schedules_dict = {}
			schedules_dict["wws_serialNum"] = row[0]
			schedules_dict["shift_date"] = row[2]
			schedules_dict["shift_day"] = row[3]
			schedules_dict["start_hour"] = row[4]
			schedules_dict["end_hour"] = row[5]
			
			numDeliveriesQuery = '''SELECT count(*) FROM Orders O JOIN Delivers D ON O.orderId = D.orderId 
								WHERE O.order_date = %s AND D.depart_restaurant > %s AND D.arrive_customer < %s AND D.duname = %s'''
			cur.execute(numDeliveriesQuery, (row[2], row[4], row[5], username))
			numDeliveries = cur.fetchone()[0]
			schedules_dict["num_deliveries"] = numDeliveries

			flatRateQuery = "SELECT flat_rate FROM Part_Time WHERE duname = %s"
			cur.execute(flatRateQuery, (username,))
			flatRate = cur.fetchone()[0]
			schedules_dict["salary_this_shift"] = "$" + str(numDeliveries*flatRate)

			schedules_list.append(schedules_dict)

	#if full time
	checkFullTime = "SELECT * FROM Full_Time WHERE duname = %s"
	cur.execute(checkFullTime, (username,))
	if len(cur.fetchall()) != 0:
		staffType = "Full_Time"
		scheduleQuery = "SELECT * FROM MWS WHERE duname = %s"
		cur.execute(scheduleQuery, (username,))
		schedules = cur.fetchall()
		schedules_list = []
		for row in schedules:

			ordersDateQuery = '''WITH temp1 AS (SELECT O.order_date, count(*) as num1 FROM Orders O 
								JOIN Delivers D ON O.orderId = D.orderId
								WHERE (select extract(month from O.order_date)) = %s
								AND O.order_time > %s AND O.order_time < %s AND D.duname = %s
								GROUP BY O.order_date),
								
								temp2 AS(SELECT order_date, count(*) AS num2 FROM Orders O 
								JOIN Delivers D ON O.orderId = D.orderId 
								WHERE (select extract(month from O.order_date)) = %s
								AND D.depart_restaurant > %s AND D.arrive_customer < %s AND D.duname = %s
								GROUP BY O.order_date)

								SELECT temp1.order_date, temp1.num1, temp2.num2
								FROM temp1 FULL OUTER JOIN temp2 ON temp1.order_date = temp2.order_date'''

			cur.execute(ordersDateQuery, (datetime.strptime(row[2], "%B").month, shift_dict['shift' + str(row[4])][0], shift_dict['shift' + str(row[4])][1], username, 
											datetime.strptime(row[2], "%B").month, shift_dict['shift' + str(row[4])][2], shift_dict['shift' + str(row[4])][3], username))
			ordersDateQuery = cur.fetchall()

			for i in ordersDateQuery:
				schedules_dict = {}
				schedules_dict["mws_serialNum"] = row[0]
				
				schedules_dict["date"] = i[0]
				schedules_dict["day"] = datetime.strptime(i[0].strftime("%Y-%m-%d"), "%Y-%m-%d").strftime("%A")

				schedules_dict["start_a"] = shift_dict['shift' + str(row[4])][0]
				schedules_dict["end_a"] = shift_dict['shift' + str(row[4])][1]
				schedules_dict["num_deliveries_a"] = i[1]

				schedules_dict["start_b"] = shift_dict['shift' + str(row[4])][2]
				schedules_dict["end_b"] = shift_dict['shift' + str(row[4])][3]
				schedules_dict["num_deliveries_b"] = i[2]
				
				flatRateQuery = "SELECT flat_rate FROM Full_Time WHERE duname = %s"
				cur.execute(flatRateQuery, (username,))
				flatRate = cur.fetchone()[0]
				schedules_dict["salary_this_shift"] = "$" + str((i[1] + i[2] )*flatRate)

				schedules_list.append(schedules_dict)

	return render_template('pastWorkScheduleDeliveryStaff.html', staffType = staffType, schedules_list = schedules_list)

@view.route("/scheduleDeliveryStaff/manageWorkSchedule", methods = ["GET", 'POST'])
def deliveryStaffManageWorkSchedule(): 
	username = current_user.username
	staffType = ""

	#if part time
	checkPartTime = "SELECT * FROM Part_Time WHERE duname = %s"
	cur.execute(checkPartTime, (username,))
	if len(cur.fetchall()) != 0:
		staffType = "Part_Time"

		date_obj = datetime.now()
		
		#this week's schedule
		start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
		end_of_week = start_of_week + timedelta(days=6)  # Sunday

		thisWeekQuery = "SELECT * FROM WWS WHERE duname = %s AND shift_date >= %s AND shift_date <= %s"
		cur.execute(thisWeekQuery, (username, start_of_week, end_of_week))
		thisWeekSchedules = cur.fetchall()
		thisWeekSchedules_list = []
		for row in thisWeekSchedules:
			schedules_dict = {}
			schedules_dict["wws_serialNum"] = row[0]
			schedules_dict["shift_date"] = row[2]
			schedules_dict["shift_day"] = row[3]
			schedules_dict["start_hour"] = row[4]
			schedules_dict["end_hour"] = row[5]

			thisWeekSchedules_list.append(schedules_dict)

		#next week's schedule
		form = ScheduleFormPT()
		global nextWeekSchedules_list
		global submittedSchedule
		totalHours = 0
		hourIntervalCheck = True
		overlapCheck = True

		def next_weekday(d, weekday):
			days_ahead = weekday - d.weekday()
			if days_ahead <= 0: # Target day already happened this week
				days_ahead += 7
			return d + timedelta(days_ahead)

		date_choices = []
		for i in range(0,6):
			str_date = next_weekday(date_obj, i).strftime("%Y-%m-%d")
			date_choices.append((str_date, str_date))		
		
		form.date.choices = date_choices

		start_choices = []
		for i in range(10,21):
			start_choices.append((str(i)+":00:00",str(i)+":00:00"))
		
		form.start.choices = start_choices

		end_choices = []
		for i in range(11,22):
			end_choices.append((str(i)+":00:00",str(i)+":00:00"))
		
		form.end.choices = end_choices

		if form.validate_on_submit() and request.method == "POST":
			wws_dict = {}
			wws_dict['username'] =  username
			wws_dict['shift_date'] =  form.date.data
			wws_dict['shift_day'] = datetime.strptime(form.date.data, "%Y-%m-%d").strftime("%A")
			wws_dict['shift_start'] = form.start.data
			wws_dict['shift_end'] =  form.end.data
			wws_dict['num_hours'] =  (int)(form.end.data[:2]) - (int)(form.start.data[:2])
			
			if wws_dict not in nextWeekSchedules_list and wws_dict['num_hours']<=4 and wws_dict['shift_start'] < wws_dict['shift_end']:
				nextWeekSchedules_list.append(wws_dict)

			return redirect("/scheduleDeliveryStaff/manageWorkSchedule")

		for wws in nextWeekSchedules_list:
			totalHours += wws['num_hours']

		for wws1 in nextWeekSchedules_list:
			for wws2 in nextWeekSchedules_list:
				if wws1['shift_date'] == wws2['shift_date'] and not(wws1['shift_start'] == wws2['shift_start'] and wws1['shift_end'] == wws2['shift_end']):
					if wws1['shift_start'] > wws2['shift_start'] and wws1['shift_start'] < wws2['shift_end']:
						overlapCheck = False
					if wws1['shift_start'] > wws2['shift_start'] and datetime.strptime(wws1['shift_start'], "%H:%M:%S") < datetime.strptime(wws2['shift_end'], "%H:%M:%S")+ timedelta(hours=1):
						hourIntervalCheck = False
					if wws1['shift_start'] == wws2['shift_start']:
						overlapCheck = False

		# for when it is submitted
		nextWeekScheduleSubmittedQuery = "SELECT * from WWS where duname = %s and shift_date >= %s and shift_date <= %s"
		cur.execute(nextWeekScheduleSubmittedQuery, (username, datetime.strptime(next_weekday(date_obj, 0).strftime("%Y-%m-%d"), "%Y-%m-%d"),
													datetime.strptime(next_weekday(date_obj, 6).strftime("%Y-%m-%d"), "%Y-%m-%d")))
		nextWeekScheduleSubmitted = cur.fetchall()
		nextWeekScheduleSubmitted_list = []
		
		for row in nextWeekScheduleSubmitted:
			nextWeekScheduleSubmitted_dict = {}
			nextWeekScheduleSubmitted_dict["wws_serialNum"] = row[0]
			nextWeekScheduleSubmitted_dict["shift_date"] = row[2]
			nextWeekScheduleSubmitted_dict["shift_day"] = row[3]
			nextWeekScheduleSubmitted_dict["start_hour"] = row[4]
			nextWeekScheduleSubmitted_dict["end_hour"] = row[5]
			nextWeekScheduleSubmitted_list.append(nextWeekScheduleSubmitted_dict)
		
		if len(nextWeekScheduleSubmitted_list) == 0:
			submittedSchedule = False
		else:
			submittedSchedule = True	
		
		return render_template('manageWorkSchedulePartTime.html', thisWeekSchedules_list = thisWeekSchedules_list, 
		nextWeekSchedules_list = nextWeekSchedules_list, form = form, totalHours = totalHours, hourIntervalCheck = hourIntervalCheck, 
		overlapCheck = overlapCheck, submittedSchedule = submittedSchedule, nextWeekScheduleSubmitted_list = nextWeekScheduleSubmitted_list)

	checkFullTime = "SELECT * FROM Full_Time WHERE duname = %s"
	cur.execute(checkFullTime, (username,))
	if len(cur.fetchall()) != 0:
		staffType = "Full_Time"

		return render_template('manageWorkScheduleFullTime.html')

@view.route("/schedulePT/<shift_date>/<shift_start>/<shift_end>", methods = ["GET","POST"])
def schedule_delete(shift_date, shift_start, shift_end):
	global nextWeekSchedules_list
	for i in nextWeekSchedules_list:
		if i["shift_date"] == shift_date and i["shift_start"] == shift_start and i["shift_end"] == shift_end:
			nextWeekSchedules_list.remove(i)
			break
	return redirect("/scheduleDeliveryStaff/manageWorkSchedule")

@view.route("/submitSchedule", methods=["GET", 'POST'])
def insertSchedule(): 
	username = current_user.username
	global nextWeekSchedules_list
	global submittedSchedule 

	serialNumQuery = "SELECT COUNT(*) FROM WWS GROUP BY duname HAVING duname = %s"
	cur.execute(serialNumQuery, (username,))
	serialNum = cur.fetchone()[0]

	for wws in nextWeekSchedules_list:
		serialNum += 1
		submitQuery = '''INSERT INTO WWS(wws_serialNum, duname, shift_date, shift_day, start_hour, end_hour) 
					VALUES (%s,%s,%s,%s,%s,%s)'''
		cur.execute(submitQuery, (serialNum, username, datetime.strptime(wws['shift_date'], "%Y-%m-%d"),  wws['shift_day'],  
		datetime.strptime(wws['shift_start'], "%H:%M:%S"),  datetime.strptime(wws['shift_end'], "%H:%M:%S")))
		conn.commit()
	
	submittedSchedule = True
	return redirect(url_for('view.deliveryStaffManageWorkSchedule'))

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
	global promo_used
	global promo_action

	delivery_fee = fixed_delivery_fee
	new_address = []
	promo_used = ""
	promo_action = ""

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

	query = "SELECT min_amt from Restaurant where uname = %s"
	cur.execute(query,(runame,))
	min_amt = int(cur.fetchone()[0])

	
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

			order_date = datetime.now().strftime("%d/%m/%Y")
			
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

	#get reviews
	query = ''' WITH restaurant_orderids as(
		select orderId from Contain c1 join Restaurant r1 on c1.runame = r1.uname where r1.rname = %s
		)
		SELECT cuname,review from Reviews join Orders using (orderId) where orderId in (select orderId from restaurant_orderids) '''
	cur.execute(query,(rname,))
	review_list = cur.fetchall()
	if not review_list:
		review_list = []
			
	return render_template('order_food.html', form = form, rname = rname,  current_order_len = len(cart_list), 
	 runame = runame, total_cost = total_cost, cart_list = cart_list, delivery_fee = delivery_fee, min_amt = min_amt, review_list = review_list)

@view.route("/order/<rname>/<fname>/<quantity>", methods = ["GET","POST"])
def order_delete(rname,fname, quantity):
	global cart_list
	for i in cart_list:
		if i["fname"] == fname and i["quantity"] == quantity:
			cart_list.remove(i)
			break
	return redirect("/order/" + rname)


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

	query = "SELECT distinct deliveryAddress || ', ' || deliveryPostalCode from orders where cuname = %s limit 5" #change this to order by
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
		new_address.append(form.address.data + ', ' + form.postal.data)

		return redirect("/order/" + rname + "/address")

	return render_template("add_address.html", form = form)

@view.route("/order/<rname>/payment", methods = ["GET","POST"])
def order_payment(rname):
	global cart_list
	global new_address
	global payment_type
	global fixed_delivery_fee
	global points_used
	global promo_used
	global promo_action

	delivery_fee = fixed_delivery_fee
	discount = 0
	form = PaymentForm()
	form2 = PromoForm()

	query = '''SELECT points from Customer where uname = %s'''
	cur.execute(query,(current_user.username,))
	points = cur.fetchone()[0]

	query = "SELECT distinct uname from Restaurant where rname = %s"
	try:
		cur.execute(query,(rname,))
	except:
		conn.rollback()	

	runame = cur.fetchone()[0]





	if form2.validate_on_submit() and 'promo' in request.form.getlist('action'):
		promo = form2.promo.data
		if promo:
			query = '''SELECT name,start_date,end_date from Promotion where promoCode = %s and runame = %s union
			SELECT name, start_date,end_date from FDS_Promo where promoCode = %s'''
			cur.execute(query,(promo,runame,promo))
			exist = cur.fetchone()
			if exist:
				name = exist[0]
				start_date = exist[1] #exist[1] is a datetime.date 
				end_date = exist[2]

				now = datetime.date(datetime.now())
				if start_date <= now and now <= end_date:
					promo_used = promo
					promo_action = name
					flash('Promo added!')
					redirect(url_for('view.order_payment', rname = rname))
				else:
					form2.promo.errors.append("Invalid Promo Code")
					redirect(url_for('view.order_payment', rname = rname))

			else:
				form2.promo.errors.append("Invalid Promo Code2")
				redirect(url_for('view.order_payment', rname = rname))

	food_cost = 0
	for i in cart_list:
		food_cost += i["food_cost"]

	#changes here need change to confirm page too
	discount = 0
	if promo_used != "" and promo_action != "":
		if promo_action == "free delivery":
			delivery_fee = 0
		elif "off" in promo_action and "%" in promo_action:
			discount_perc = int(promo_action.split('%')[0]) / 100
			discount = int(discount_perc * food_cost)


	if form.validate_on_submit() and 'pay' in request.form.getlist('action'): 
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
			

	return render_template("order_payment.html", form = form, form2 = form2, cart_list = cart_list, new_address = new_address, 
		food_cost = food_cost, rname = rname, delivery_fee = delivery_fee, points = points, discount = discount)

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
	global promo_used

	delivery_fee = fixed_delivery_fee - points_used

	food_cost = 0
	for i in cart_list:
		food_cost += i["food_cost"]

	discount = 0
	if promo_used != "" and promo_action != "":
		if promo_action == "free delivery":
			delivery_fee = 0
		elif "off" in promo_action and "%" in promo_action:
			discount_perc = int(promo_action.split('%')[0]) / 100
			discount = int(discount_perc * food_cost)

	if form.validate_on_submit():
		today_now = datetime.now() #+ timedelta(hours = 14) #use this if u doing this at night lol

		#settle Orders start
		try:
			address = new_address[0]
		except:
			return redirect("/")
		order_date = today_now.strftime("%m/%d/%Y")
		order_time = today_now.strftime("%H:%M:%S")
		query = "SELECT max(orderid) from Orders"
		cur.execute(query)
		maxid = int(cur.fetchone()[0])
		if maxid:
			newid = maxid + 1
		else:
			newid = 0

		deliveryAddress = new_address[0][:-8] 
		deliveryPostalCode = new_address[0][-6:]

		first2 = deliveryPostalCode[:2]

		if int(first2) in [11,12,13,60,61,62,63,64,65,66,67,68]:
			area = 'West'
		elif int(first2) in [42,43,44,45,46,47,48,49,50,81,51,52]:
			area = 'East'
		elif int(first2) in [53,54,55,56,57,79,80]:
			area = 'North-East'
		elif int(first2) in [69,70,71,72,73,75,76]:
			area = 'North'
		else:
			area = 'Central'

		#settle insert into Delivery start

		
		today_day = calendar.day_name[today_now.weekday()]
		today_month = calendar.month_name[today_now.month]
		today_year = today_now.year
		today_date = today_now.date()
		today_time = today_now.time()


		available_list = []

		#get part-timers start
		# query = '''WITH working_PT as (SELECT distinct duname from WWS where shift_date = %s and start_hour < %s and end_hour > %s)
		# 			SELECT uname from Delivery_Staff where uname in (select duname from working_PT) and is_delivering = false'''
		# cur.execute(query,(today_date,today_time, today_time))
		# exist = cur.fetchall()
		# if exist:
		# 	for tup in exist:
		# 		if tup[0] not in available_list:
		# 			available_list.append(tup[0])


		# #get part-timers end


		# #get full-timers start 
		
		# shift_list = [] #possible shifts
		# shift = 1

		# global shift_dict
		# for i in ['shift1','shift2','shift3','shift4']:
		# 	if (order_time >= shift_dict[i][0] and order_time < shift_dict[i][1]) or (order_time >= shift_dict[i][2] and order_time < shift_dict[i][3]):
		# 		shift_list.append(shift)
		# 	shift += 1

		# day_option_list = [] #possible day options
		# global day_option_dict
		# for i in [1,2,3,4,5,6,7]:
		# 	if today_day in day_option_dict[i]:
		# 		day_option_list.append(i)

		
		# for i in shift_list:
		# 	for j in day_option_list:
		# 		query = '''WITH working_FT as 
		# 					(SELECT duname from MWS where work_month = %s and work_year = %s and day_option = %s and shift = %s) 
		# 					select uname from Delivery_Staff where uname in (select duname from working_FT) and is_delivering = false
		# 					'''
		# 		cur.execute(query,(today_month,today_year,j,i))
		# 		exist = cur.fetchall()
		# 		if exist: #list of tuples
		# 			for tup in exist:
		# 				if tup[0] not in available_list:
		# 					available_list.append(tup[0])

		#get full-timers end

		#testing
		shift_list = [] #possible shifts
		shift = 1

		global shift_dict
		for i in ['shift1','shift2','shift3','shift4']:
			if (order_time >= shift_dict[i][0] and order_time < shift_dict[i][1]) or (order_time >= shift_dict[i][2] and order_time < shift_dict[i][3]):
				shift_list.append(shift)
			else:
				shift_list.append(0)
			shift += 1


		day_option_list = [] #possible day options
		global day_option_dict
		for i in [1,2,3,4,5,6,7]:
			if today_day in day_option_dict[i]:
				day_option_list.append(i)
			else:
				day_option_list.append(0)

		query = '''SELECT * from get_workers(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
		cur.execute(query, (today_date, today_time, today_month, today_year, day_option_list[0], day_option_list[1], day_option_list[2],
			day_option_list[3], day_option_list[4], day_option_list[5], day_option_list[6], shift_list[0], shift_list[1], shift_list[2],
			shift_list[3]))
		exist = cur.fetchall()
		if exist:
			for tup in exist:
				if tup[0] not in available_list:
					available_list.append(tup[0])

		test = (today_date, today_time, today_month, today_year, day_option_list[0], day_option_list[1], day_option_list[2],
			day_option_list[3], day_option_list[4], day_option_list[5], day_option_list[6], shift_list[0], shift_list[1], shift_list[2],
			shift_list[3])

		#testing end

		if len(available_list) > 0:

			query = '''INSERT INTO orders(orderId,cuname, payment_type, deliveryAddress, deliveryPostalCode, area, order_date,order_time,deliveryFee,foodCost,promoCode) 
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
			cur.execute(query,(newid,current_user.username,payment_type,deliveryAddress,deliveryPostalCode,area,order_date,order_time,delivery_fee,food_cost - discount,promo_used))
			conn.commit()

			query = '''INSERT INTO Delivers(orderId,duname) VALUES (%s,%s)'''
			cur.execute(query, (newid, available_list[0]))
			conn.commit()

			query = '''UPDATE Delivery_Staff SET is_delivering = True where uname = %s'''
			cur.execute(query, (available_list[0],))
		else:
			return render_template("order_failed.html", test = test)

		#settle insert into Deliver end


		# query = '''INSERT INTO orders(orderId,cuname, payment_type, deliveryAddress, deliveryPostalCode, area, order_date,order_time,deliveryFee,foodCost,promoCode) 
		# 			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
		# cur.execute(query,(newid,current_user.username,payment_type,deliveryAddress,deliveryPostalCode,area,order_date,order_time,delivery_fee,food_cost - discount,promo_used))
		# conn.commit()

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

	return render_template("order_confirm.html", form = form, rname = rname, cart_list = cart_list, new_address = new_address[0],
		food_cost = food_cost, delivery_fee = delivery_fee, points_used = points_used, payment_type = payment_type, 
		promo_used = promo_used, discount = discount) 



@view.route("/done", methods = ["GET","POST"])
def order_done():
	global cart_list
	global new_address
	global payment_type
	global fixed_delivery_fee
	global points_used
	global promo_used
	cart_list = []
	new_address = []
	payment_type = ""
	card_used = ""
	points_used = 0
	promo_used = ""

	# global available_FT_list
	# test = available_FT_list
	# available_FT_list = []
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
			today_now = datetime.now()
			today_date = today_now.strftime("%Y-%m-%d")
			query = "INSERT INTO Users VALUES (%s,%s)"
			cur.execute(query,(username,password))
			conn.commit()
			query = "INSERT INTO Customer VALUES (%s,%s,0,%s)"
			cur.execute(query,(username,firstName,today_date))
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
	select * from Orders join (select distinct orderid, rname from new_contains) c2 using (orderid) where cuname = %s and is_delivered = False order by orderid DESC'''

	# query = "SELECT * from get_orders(%s)"
	try: 
		cur.execute(query,(current_user.username,))
	except:
		conn.rollback()
	order_table = cur.fetchall() ##order_table is a list of tuples
	order_list = []
	for i in order_table:
		one_order_dict = {}
	
		#(orderId, cuname, payment_type, deliveryAddress, deliveryPostalCode, area, is_delivered, order_date, order_time, deliveryFee, foodCost, promoCode, rname) 
		one_order_dict["orderid"] = i[0]
		one_order_dict["payment_type"] = i[2]
		one_order_dict["address"] = i[3] + ', ' + i[4]
		one_order_dict["is_delivered"] = i[6]
		one_order_dict["order_date"] = i[7]
		one_order_dict["order_time"] = i[8]
		one_order_dict["deliveryFee"] = i[9]
		one_order_dict["foodCost"] = i[10]
		one_order_dict["promoCode"] = i[11]
		one_order_dict["rname"] = i[12]
		order_list.append(one_order_dict)
	if order_list:  
		return render_template('orders.html', status = order_list)
	else:
		return render_template('orders.html', status = [])
		
# START OF PROFILE

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
		
			#(orderId, cuname, payment_type, deliveryAddress, deliveryPostalCode, area, is_delivered, order_date, order_time, deliveryFee, foodCost, promoCode, rname)  
			one_order_dict["orderid"] = i[0]
			one_order_dict["payment_type"] = i[2]
			one_order_dict["address"] = i[3] + ', ' + i[4]
			one_order_dict["is_delivered"] = i[6]
			one_order_dict["order_date"] = i[7]
			one_order_dict["order_time"] = i[8]
			one_order_dict["deliveryFee"] = i[9]
			one_order_dict["foodCost"] = i[10]
			if i[11] == None:
				one_order_dict["promoCode"] = ''
			else:
				one_order_dict["promoCode"] = i[11]
			one_order_dict["rname"] = i[12]

			query = '''SELECT review from Reviews 
			join (select orderid, cuname from Orders where cuname = %s) c using(orderid) 
			where orderid = %s'''
			cur.execute(query,(current_user.username,i[0]))
			exist = cur.fetchone()

			if exist:
				one_order_dict["reviewed"] = True
			else:
				one_order_dict["reviewed"] = False


			query = '''SELECT rating from Delivers where orderId = %s'''
			cur.execute(query,(i[0],))
			try: #reason for try is this will give (None,) if false then cannot subscript
				exist = cur.fetchone()[0]
				if exist:
					one_order_dict["rated"] = True
				else:
					one_order_dict["rated"] = False
			except:
				one_order_dict["rated"] = True # if cannot find means order has no driver

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
		
			#(orderId, cuname, payment_type, deliveryAddress, deliveryPostalCode, area, is_delivered, order_date, order_time, deliveryFee, foodCost, promoCode, rname)
			one_order_dict["orderid"] = i[0]
			one_order_dict["payment_type"] = i[2]
			one_order_dict["address"] = i[3] + ', ' + i[4]
			one_order_dict["is_delivered"] = i[6]
			one_order_dict["order_date"] = i[7]
			one_order_dict["order_time"] = i[8]
			one_order_dict["deliveryFee"] = i[9]
			one_order_dict["foodCost"] = i[10]
			if i[11] == None:
				one_order_dict["promoCode"] = ''
			else:
				one_order_dict["promoCode"] = i[11]
			one_order_dict["rname"] = i[12]

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
		return redirect("/profile/pastOrders")
	return render_template("review.html", form = form, rname = rname)

@view.route("/rate/<orderid>", methods = ["GET","POST"])
@login_required
def rate(orderid):
	form = RateForm()
	query = '''SELECT duname from Delivers where orderId = %s'''
	cur.execute(query,(orderid,))
	duname = cur.fetchone()[0]

	query = '''SELECT dname from Delivery_Staff where uname = %s'''
	cur.execute(query,(duname,))
	dname = cur.fetchone()[0]

	if form.validate_on_submit():
		rating = form.rating.data
		query = '''UPDATE Delivers set rating = %s where orderid = %s'''
		cur.execute(query,(rating,orderid))
		conn.commit()
		return redirect("/profile/pastOrders")

	return render_template('rate.html',form = form, dname = dname)



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

# END OF PROFILE

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

