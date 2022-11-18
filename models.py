import sqlite3 as sql

def checkUserExists(username):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "SELECT count(*) FROM users WHERE username = ?"
	cur.execute(query, [username])
	(num_users_with_username,) = cur.fetchone()
	con.commit()
	con.close()
	print(num_users_with_username)
	if num_users_with_username > 0:
		print("user already exists")
		return True 
	else:
		return False



def insertUser(firstname,lastname,username,password):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "INSERT INTO users (firstname, lastname, username, password) VALUES (?, ?, ?, ?)"
	# query += "WHERE NOT EXISTS ("
	# query += "SELECT username FROM users WHERE username = {})".format(username)
	cur.execute(query, (firstname, lastname, username, password))#, [(firstname, lastname, username, password), username])
	con.commit()
	con.close()

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username FROM users")
	users = cur.fetchall()
	print(users)
	con.close()
	return users


def retrieveFriends(current_user_username):
	"""
	Get's a list of the current user's friends
	"""
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "SELECT username FROM friends WHERE primary_friend = ?"
	cur.execute(query,[current_user_username])
	users = cur.fetchall()
	print(users)
	con.close()
	return users