import sqlite3 as sql
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "SELECT count(*) FROM users WHERE username = ?"
    cur.execute(query, [username])
    (num_users_with_username_and_password,) = cur.fetchone()
    if num_users_with_username_and_password > 0:
        query = "SELECT password FROM users WHERE username = ?"
        cur.execute(query, [username])
        (hashed_password,) = cur.fetchone()
        con.commit()
        con.close()
        if check_password_hash(hashed_password, password):
            return True
    else:
        print('got here')
        return False


def update_inbox(user1, user2, matched_boolean):
    print("check that update inbox is working")
    con = sql.connect("database.db")
    cur = con.cursor()

    query = "SELECT * FROM inbox WHERE matched_user1 = ? AND matched_user2 = ? and user1_matched_boolean is NULL"
    cur.execute(query, [user1, user2])
    row = cur.fetchone()
    # print("row 2 is", row)
    if row:
        print("check here 1")
        query = "UPDATE inbox SET user1_matched_boolean = ? WHERE matched_user1 = ? AND matched_user2 = ? AND user1_matched_boolean is NULL"
        cur.execute(query, [matched_boolean, user1, user2])

    # current is matched user 2, have to set boolean
    query = "SELECT * FROM inbox WHERE matched_user2 = ? AND matched_user1 = ? and user2_matched_boolean is NULL"
    cur.execute(query, [user1, user2])
    row = cur.fetchone()
    # print("row 1 is", row)
    if row:
        print("check here 2")
        query = "UPDATE inbox SET user2_matched_boolean = ? WHERE matched_user2 = ? AND matched_user1 = ? AND user2_matched_boolean is NULL"
        cur.execute(query, [matched_boolean, user1, user2])

    query = "SELECT * FROM inbox WHERE matched_user2 = ? AND matched_user1 = ?"
    cur.execute(query, [user1, user2])
    row = cur.fetchone()
    print("row after is", row)
    con.commit()
    con.close()


def match_users(username, user1, user2):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "INSERT INTO inbox (username, matched_user1, matched_user2, user1_matched_boolean, user2_matched_boolean) VALUES (?, ?, ?, ?, ?)"
    cur.execute(query, [username, user1, user2, None, None])
    query = "SELECT * FROM inbox WHERE username = ?"
    cur.execute(query, [username])
    matches = []
    row = cur.fetchone()
    while row is not None:
        matches.append([row[0], row[1], row[2]])
        # print("your matches", row)
        row = cur.fetchone()
    con.commit()
    con.close()


def insert_dummy_users():
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "INSERT INTO users (first_name, last_name, username, password, phone_number, gender, preference) VALUES "
    query += "(?, ?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?, ?), "
    query += "(?, ?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?, ?), "
    query += "(?, ?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?, ?)"

    args = [
    "Adam", "Smith", "asmith", generate_password_hash("password"), "100-000-0000", "Male", "Female", 
    "Lily", "Porter", "lporter",generate_password_hash("password"), "100-000-0000",  "Female", "Male", 
    "John", "Doe", "jdoe", generate_password_hash("password"), "100-000-0000",  "Male", "Female",
    "Annette", "Lee", "alee", generate_password_hash("password"), "100-000-0000",  "Female", "Male",
    "Allen", "Chun", "achun", generate_password_hash("password"), "100-000-0000",  "Male", "Female",
    "Kishan", "Patel", "kpatel", generate_password_hash("password"), "100-000-0000",  "Male", "Female",
    "Bernard", "Kim", "bkim", generate_password_hash("password"), "100-000-0000",  "Male", "Male",
    "Kimmy", "Ball", "kball", generate_password_hash("password"), "100-000-0000",  "Female", "Female",
    "Carter", "Yin", "cyin", generate_password_hash("password"), "100-000-0000",  "Non-binary", "Male",

    ]

    cur.execute(query, args)
    con.commit()
    con.close()
    print("check")


def insert_friend(username, friend):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "INSERT INTO friends (username, friend) VALUES (?, ?)"
    cur.execute(query, (username, friend))
    query = "INSERT INTO friends (username, friend) VALUES (?, ?)"
    cur.execute(query, (friend, username))
    con.commit()
    con.close()



def add_friend(username, friend_username):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "INSERT INTO friends (username, friend) VALUES (?, ?)"
    cur.execute(query, [username, friend_username])
    cur.execute(query, [friend_username, username])


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

def get_match_recommendations(username, user1, my_made_matches):
    con = sql.connect("database.db")
    cur = con.cursor()
    print("check getting match recommendations")
    # WHERE username IN (SELECT friend from friends WHERE username = ?)
    query = "SELECT gender, preference FROM users "
    query += "WHERE username = ?"
    cur.execute(query, [user1])
    info = cur.fetchone()
    user1_gender = info[0]
    user1_preference = info[1]
    print("user1 gender is", user1_gender)
    print("user1 preference is", user1_preference)
    query = "SELECT first_name, last_name, username FROM users WHERE username IN (SELECT friend from friends WHERE username = ?) "
    args = []
    if my_made_matches:
        for match in my_made_matches:
            if user1 == match[0]:
                query += "AND username != ? "
                args.append(match[1])
            elif user1 == match[1]:
                query += "AND username != ? "
                args.append(match[0])
    query += "AND username != ? and preference = ? and gender = ?"
    args += [username, user1, user1_gender, user1_preference]
    print("query", query)
    cur.execute(query, args)
    match_recommendations = cur.fetchall()
    print("match recommendations", match_recommendations)
    con.close()
    return match_recommendations 


def retrieve_potential_friends(username, friends, first_name, last_name, residential_college, class_year, gender, orientation):
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
    if friends or first_name or last_name or residential_college or class_year or gender or orientation:
        query += "WHERE "
        if friends:
            len_friends = len(friends)
            for index, friend in enumerate(friends):
                query += "username != ? "
                friend_username = friend[2]
                # print("friend_username", friend_username)
                args.append(friend_username)
                if index < len_friends - 1:
                    query += "AND "
                else: 
                    if first_name or last_name or residential_college or class_year or gender or orientation:
                        query += "AND "
        

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
        query += "AND users.username != ? "
    else:
        query += "WHERE users.username != ? "

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
                 "college": college, "class_year": class_year, "gender": gender,
                 "orientation": orientation, "match_preference": match_preference}
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


def edit_profile_info(username, first_name, last_name, phone_number, residential_college, class_year, gender, orientation, match_preference):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "UPDATE users SET first_name = ?, last_name = ?, phone_number = ?, college = ?, class_year = ?, gender = ?, orientation = ?, preference = ? WHERE username = ?"
    cur.execute(query, [first_name, last_name, phone_number, residential_college, class_year,
                gender, orientation, match_preference, username])
    con.commit()
    con.close()



def get_matches_in_inbox(username):
    print("username in get matches", username)
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "SELECT matched_user1, user2_matched_boolean, user1_matched_boolean, users.first_name, users.last_name, users.phone_number from inbox "
    query += "JOIN users on inbox.matched_user1 = users.username "
    query += "WHERE inbox.matched_user2 = ?"
    cur.execute(query, [username])
    matches = cur.fetchall()
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "SELECT matched_user2, user1_matched_boolean, user2_matched_boolean, users.first_name, users.last_name, users.phone_number from inbox "
    query += "JOIN users on inbox.matched_user2 = users.username "
    query += "WHERE inbox.matched_user1 = ? "
    cur.execute(query, [username])
    matches += cur.fetchall()
    print("matches are", matches)
    con.close()
    return matches

def get_matches_made_by_me(username):
    print("username in get matches made by me", username)
    con = sql.connect("database.db")
    cur = con.cursor()
    query = "SELECT matched_user1, matched_user2 from inbox "
    query += "JOIN users on inbox.username = users.username "
    query += "WHERE inbox.username = ?"
    cur.execute(query, [username])
    matches = cur.fetchall()
    con.close()
    print("my made matches", matches)
    return matches


