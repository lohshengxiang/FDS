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