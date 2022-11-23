import sqlite3 as sql

def login(username, password):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "SELECT count(*) FROM users WHERE username = ? AND password = ?"
	cur.execute(query, [username, password])
	(num_users_with_username_and_password,) = cur.fetchone()
	con.commit()
	con.close()
	if num_users_with_username_and_password > 0:
		return True
	else:
		return False

def insert_friend(username, friend):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "INSERT INTO friends (username, friend) VALUES (?, ?)"
	cur.execute(query, (username, friend))
	con.commit()
	con.close()

def retrieve_potential_friends(username, residential_college, class_year, gender, orientation):
	con = sql.connect("database.db")
	cur = con.cursor()
	args = []

	if residential_college == 'any':
		residential_college = None
	if class_year == 'any':
		class_year = None
	if gender == 'any':
		gender = None
	if orientation == 'any':
		orientation = None

	query = "SELECT id, firstname, lastname FROM users "
	if residential_college or class_year or gender or orientation:
		query += "WHERE "
		if residential_college:
			query += "college = ? "
			args.append(residential_college)
			if class_year or gender or orientation:
				query += "AND "
		if class_year:
			query += "class_year = ? "
			args.append(class_year)
			if gender or orientation:
				query += "AND "
		if gender:
			query += "gender = ? "
			args.append(gender)
			if orientation:
				query += "AND "
		if orientation:
			query += "orientation = ? "
			args.append(orientation)
		query += "AND username != ? "
	else:
		query += "WHERE username != ? "

	args.append(username)
	cur.execute(query, args)
	friends = []
	row = cur.fetchone()
	while row is not None:
		friends.append([row[0], row[1], row[2]])
		print(row)
		row = cur.fetchone()
	con.close()
	return friends

def retrieve_usernames(user_username):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "SELECT username FROM users WHERE username = ?"
	cur.execute(query, [user_username])
	con.commit()
	con.close()

def check_user_exists(username):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "SELECT count(*) FROM users WHERE username = ?"
	cur.execute(query, [username])
	(num_users_with_username,) = cur.fetchone()
	print(num_users_with_username)
	con.commit()
	con.close()
	if num_users_with_username > 0:
		return True
	else:
		return False

def insert_user(firstname,lastname,username,password):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "INSERT INTO users (firstname, lastname, username, password) VALUES (?, ?, ?, ?)"
	cur.execute(query, (firstname, lastname, username, password))
	con.commit()
	con.close()

def retrieve_users():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username FROM users")
	users = cur.fetchall()
	con.close()
	return users

def edit_profile_info(username, residential_college, class_year, gender, orientation, match_preference):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "UPDATE users SET college = ?, class_year = ?, gender = ?, orientation = ?, preference = ? WHERE username = ?"
	cur.execute(query,[residential_college, class_year, gender, orientation, match_preference, username])
	con.commit()
	con.close()