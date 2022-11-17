import sqlite3 as sql

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
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	print(users)
	con.close()
	return users
