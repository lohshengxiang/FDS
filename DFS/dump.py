# @view.route("/japanese", methods = ["GET","POST"])
# def japanese():
# 	form = OrderForm()
# 	query = "SELECT distinct rname from Food where category = 'Japanese'"
# 	cur.execute(query)
# 	rname_rows = cur.fetchall() # list of tuples
# 	rname_choices = []
# 	for row in rname_rows:
# 		rname_choices.append((row[0],row[0]))
# 	form.rname.choices = rname_choices 

# 	# get fnames
# 	# query = "SELECT distinct fname from Food where category = 'Japanese'" #issue here that wont submit form if food not jap
# 	query = "SELECT distinct fname from Food"
# 	cur.execute(query)
# 	fname_rows = cur.fetchall()
# 	fname_choices = []
# 	for row in fname_rows:
# 		fname_choices.append((row[0],row[0]))
# 	form.fname.choices = fname_choices

# 	query = "SELECT max(order_limit) from Food"
# 	try:
# 		cur.execute(query)
# 	except:
# 		conn.rollback()
# 	limit = int(cur.fetchone()[0])
# 	quantity_choices = []
# 	for i in range(1,limit+1):
# 		quantity_choices.append((i,i))
# 	form.quantity.choices = quantity_choices


# 	#create order
# 	if form.validate_on_submit():
# 		if not current_user.is_authenticated:
# 			return redirect('/login')
# 		else:
# 			username = current_user.username
# 			rname = form.rname.data
# 			order_time = datetime.now().strftime("%H:%M:%S")
# 			payment_type = "CC"

# 			# get food price
# 			query = "SELECT price from Food where rname = %s and fname = %s"
# 			cur.execute(query,(form.rname.data,form.fname.data))
# 			total_cost = int(cur.fetchone()[0])

# 			order_date = datetime.now().strftime("%m/%d/%Y")
# 			dropoff = 1 #whats this?
# 			date = datetime.now().strftime("%m/%d/%Y")
# 			time = datetime.now().strftime("%H:%M:%S")

# 			cart_list.append((username,rname,order_time,payment_type,total_cost,order_date,dropoff,date,time)) #insert tuple
# 			# query = '''INSERT INTO orders(orderid, username, payment_method, order_time) \
# 			# VALUES (%s ,%s, %s, %s)'''
# 			# cur.execute(query,(orderid,username,payment_method,order_time,))
# 			# conn.commit()
# 			return redirect("/cart")
# 	return render_template('japanese.html', form = form)


# @view.route('/fname/<rname>')
# def fname(rname):
# 	query = "SELECT fname from Food where rname = %s"
# 	cur.execute(query,(rname,))
# 	fname_rows = cur.fetchall()
# 	fname_choices = []

# 	for row in fname_rows:
# 		fname_choices.append((row[0],row[0]))
	
# 	fnameArray = []
# 	for row in fname_rows:
# 		fnameObj = {}
# 		fnameObj['id'] = row[0] #id is pizza
# 		fnameObj['fname'] = row[0] #fname also pizza
# 		fnameArray.append(fnameObj)
# 	return jsonify({'fname':fnameArray})

@view.route("/japanese",methods = ["GET","POST"])
def japanese():
	form = RestaurantForm()
	query = "SELECT distinct rname from Food where category = 'Japanese'"
	cur.execute(query)
	rname_rows = cur.fetchall() # list of tuples
	rname_choices = []
	for row in rname_rows:
		rname_choices.append((row[0],row[0]))
	form.rname.choices = rname_choices

	if form.validate_on_submit():
		return redirect('/restaurant/' + form.rname.data)
	return render_template('japanese2.html', form = form)

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