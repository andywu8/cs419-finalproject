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

def match_users(username, user1, user2):
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "INSERT INTO inbox (username, matched_user1, matched_user2, inbox_message) VALUES (?, ?, ?, ?)"
	cur.execute(query, [username, user1, user2, "You've been matched"])
	con.commit()
	con.close()

def insert_dummy_users():
	con = sql.connect("database.db")
	cur = con.cursor()
	query = "INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?), (?, ?, ?, ?), (?, ?, ?, ?)"
	args = ["John", "Doe", "jdoe", "password", "John1", "Doe1", "jdoe", "password", "John2", "Doe2", "jdoe2", "password"]
	cur.execute(query, args)
	con.commit()
	con.close()
	print("check")

def insert_friend(username, friend):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "INSERT INTO friends (username, friend) VALUES (?, ?)"
    cur.execute(query, (username, friend))
    con.commit()
    con.close()


def retrieve_potential_friends(username, first_name, last_name, residential_college, class_year, gender, orientation):
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

    query = "SELECT username, first_name, last_name FROM users "
    if first_name or last_name or residential_college or class_year or gender or orientation:
        query += "WHERE "
        if first_name:
            query += "LOWER(first_name) LIKE ? "
            args.append(first_name.lower() + '%')
            if last_name or residential_college or class_year or gender or orientation:
                query += "AND "
        if last_name:
            query += "LOWER(last_name) LIKE ? "
            args.append(last_name.lower() + '%')
            if residential_college or class_year or gender or orientation:
                query += "AND "
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
    print("args: ", args)
    print("query", query)

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

def retrieve_profile_info(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cur.execute(query, [username])
    info = cur.fetchone()
    first_name = info[1]
    last_name = info[2]
    number = info[5]
    college = info[6]
    class_year = info[7]
    gender = info[8]
    orientation = info[9]
    match_preference = info[10]
    info_dict = {"first_name": first_name, "last_name": last_name, "number": number, 
                 "college":college, "class_year":class_year, "gender":gender, 
                 "orientation":orientation, "match_preference": match_preference}
    return info_dict
    

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


def insert_user(first_name, last_name, username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)"
    cur.execute(query, (first_name, last_name, username, password))
    con.commit()
    con.close()


def retrieve_users():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username FROM users")
    users = cur.fetchall()
    con.close()
    return users


def edit_profile_info(username, phone_number, residential_college, class_year, gender, orientation, match_preference):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "UPDATE users SET phone_number = ?, college = ?, class_year = ?, gender = ?, orientation = ?, preference = ? WHERE username = ?"
    cur.execute(query, [phone_number, residential_college, class_year,
                gender, orientation, match_preference, username])
    con.commit()
    con.close()


def add_friend(username, friend_username):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "INSERT INTO friends (username, friend) VALUES (?, ?)"
    cur.execute(query, [username, friend_username])
    con.commit()
    con.close()


def get_my_friends(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "SELECT first_name, last_name, username from users WHERE username IN (SELECT friend from friends WHERE username = ?)"
    cur.execute(query, [username])
    friends = []
    row = cur.fetchone()
    while row is not None:
        friends.append([row[0], row[1], row[2]])
        print(row)
        row = cur.fetchone()
    con.close()
    return friends


def get_potential_matches(friend_username):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "SELECT first_name, last_name, username from users WHERE gender IN (SELECT preference from users WHERE username = ?)"
    cur.execute(query, [friend_username])
    matches = cur.fetchall()
    con.close()
    return matches
