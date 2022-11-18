from flask import Flask
from flask import render_template
from flask import request
import models as dbHandler

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method=='POST':
        return render_template('index.html')
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
        friend_username = request.form['friend_username']
        dbHandler.insertFriend(current_user_username, friend_username)
    friends = dbHandler.retrieveFriends(current_user_username)
    users = dbHandler.retrieveUsers()
    current_user_username = "test"
    friends = dbHandler.retrieveFriends(current_user_username)
    return render_template('add_friends.html', users = users, friends=friends)

@app.route('/inbox', methods=['POST','GET'])
def inbox():
    return render_template('inbox.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
