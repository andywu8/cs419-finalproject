from flask import Flask
from flask import render_template
from flask import request
import models as dbHandler

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    error_messages = []
    confirmation_message = None
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if dbHandler.login(username, password) == True:
            users = dbHandler.retrieveUsers()
            
            confirmation_message = "You are logged in! " + username

        else:
            error_messages.append("Incorrect username or password")
        return render_template('index.html', users = users, error_messages = error_messages, confirmation_message = confirmation_message)

    else:
        return render_template('index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    error_messages = []
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        if dbHandler.checkUserExists(username) == False:
            dbHandler.insertUser(firstname, lastname, username, password)
        else:
            error_messages.append("Username already exists")
    users = dbHandler.retrieveUsers()
    return render_template('signup.html', users = users, error_messages = error_messages)


@app.route('/add_friends', methods=['POST','GET'])
def add_friends():
    current_user_username = "anwu8"
    if request.method=='POST':
        print("check")
        print("check 2")
        user_username = "hardcoded username"
        # user_username = request.form["user_username"]
        print("user username", user_username)
        print("check after user username")
        dbHandler.insertFriend(current_user_username, user_username)
        print("check insert")

    users = dbHandler.retrieveUsers()
    friends = dbHandler.retrieveFriends(current_user_username)
    return render_template('add_friends.html', users = users, friends=friends)

@app.route('/inbox', methods=['POST','GET'])
def inbox():
    return render_template('inbox.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
