"""main file to run flask app"""

from flask import Flask, render_template, request, redirect, url_for
from models import login, insert_friend, retrieve_potential_friends, retrieve_users, check_user_exists, insert_user, edit_profile_info

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    """home page"""
    error_messages = []
    users = None
    confirmation_message = None

    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        correct_login = login(username, password)
        if correct_login:
            users = retrieve_users()
            return redirect(url_for('dashboard', username=username))
        else:
            error_messages.append("Incorrect username or password")
            return render_template('index.html',
                                   users = users,
                                   error_messages = error_messages,
                                   confirmation_message = confirmation_message)
    else:
        return render_template('index.html')

@app.route('/profile/<username>', methods=['POST', 'GET'])
def profile(username):
    """profile page"""
    return render_template('profile.html', username=username)

@app.route('/dashboard/<username>', methods=['POST', 'GET'])
def dashboard(username):
    """dashboard page"""
    if request.method=='POST':
        residential_college = request.form.get('residential_college')
        class_year = request.form.get('class_year')
        gender = request.form.get('gender')
        orientation = request.form.get('orientation')
        match_preference = request.form.get('match_preference')

        edit_profile_info(username, residential_college, class_year, gender, orientation, match_preference)

    return render_template('dashboard.html', username=username)

@app.route('/signup', methods=['POST','GET'])
def signup():
    """signup page"""
    error_messages = []

    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        user_exists = check_user_exists(username)

        if not user_exists:
            insert_user(firstname, lastname, username, password)
            return redirect(url_for('dashboard', username=username))
        else:
            error_messages.append("Username already exists")

    users = retrieve_users()
    return render_template('signup.html', users = users, error_messages = error_messages)

@app.route('/find_friends/<username>', methods=['POST','GET'])
def find_friends(username):
    """add friends page"""
    return render_template('find_friends.html', username=username)

@app.route('/add_friends/<username>', methods=['POST','GET'])
def add_friends(username):
    """add friends page"""
    residential_college = request.args.get('residential_college')
    class_year = request.args.get('class_year')
    gender = request.args.get('gender')
    orientation = request.args.get('orientation')

    potential_friends = retrieve_potential_friends(username, residential_college, class_year, gender, orientation)
    return render_template('add_friends.html', username=username, potential_friends=potential_friends)

@app.route('/inbox', methods=['POST','GET'])
def inbox():
    """inbox page"""
    return render_template('inbox.html')

if __name__ == '__main__':
    """runs the application on a server"""
    app.run(debug=False, host='0.0.0.0', port=8080)
