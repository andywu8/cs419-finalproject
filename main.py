"""main file to run flask app"""

from flask import Flask, render_template, request, redirect, url_for
from models import login, insert_friend, retrieve_potential_friends, retrieve_users, check_user_exists, insert_user, edit_profile_info, add_friend, get_my_friends, get_potential_matches, insert_dummy_users, match_users
import cgi #https://stackoverflow.com/questions/27046448/get-post-data-from-ajax-post-request-in-python-file
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    """home page"""
    error_messages = []
    users = None
    confirmation_message = None


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        correct_login = login(username, password)
        if correct_login:
            users = retrieve_users()
            print("users", users)
            return redirect(url_for('dashboard', username=username))
        else:
            error_messages.append("Incorrect username or password")
            return render_template('index.html',
                                   users=users,
                                   error_messages=error_messages,
                                   confirmation_message=confirmation_message)
    else:
        return render_template('index.html')


@app.route('/profile/<username>', methods=['POST', 'GET'])
def profile(username):
    """profile page"""
    return render_template('profile.html', username=username)


@app.route('/dashboard/<username>', methods=['POST', 'GET'])
def dashboard(username):
    """dashboard page"""
    if request.method == 'POST':
        residential_college = request.form.get('residential_college')
        class_year = request.form.get('class_year')
        gender = request.form.get('gender')
        orientation = request.form.get('orientation')
        match_preference = request.form.get('match_preference')

        edit_profile_info(username, residential_college,
                          class_year, gender, orientation, match_preference)

    return render_template('dashboard.html', username=username)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """signup page"""
    error_messages = []

    if request.method == 'POST':
        # insert_dummy_users()

        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user_exists = check_user_exists(username)

        if not user_exists:
            insert_user(first_name, last_name, username, password)
            return redirect(url_for('dashboard', username=username))
        else:
            error_messages.append("Username already exists")

    users = retrieve_users()
    print("users", users)
    return render_template('signup.html', users=users, error_messages=error_messages)


@app.route('/find_friends/<username>', methods=['POST', 'GET'])
def find_friends(username):
    """add friends page"""
    return render_template('find_friends.html', username=username)


@app.route('/add_friends/<username>', methods=['POST', 'GET'])
def add_friends(username):
    """add friends page"""
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        residential_college = request.args.get('residential_college')
        class_year = request.args.get('class_year')
        gender = request.args.get('gender')
        orientation = request.args.get('orientation')
        potential_friends = retrieve_potential_friends(
            username, first_name, last_name, residential_college, class_year, gender, orientation)
        return render_template('add_friends.html', username=username, potential_friends=potential_friends)
    else:
        friend_username = request.args.get('friend_username')
        add_friend(username, friend_username)
        return render_template('add_friends.html', username=username)


@app.route('/inbox', methods=['POST', 'GET'])
def inbox():
    """inbox page"""
    # format for dummy data
    # [matched_user1, matched_user2, matched_boolean]
    # make sure the user names are actually real usernames: these are just for example
    # example dummy_inbox_data = [["anwu8", "anwu888", None], ["anwu8", "anwu888", True], ["anwu8", "anwu888", False]]
    dummy_inbox_data = []
    return render_template('inbox.html', inbox_data = dummy_inbox_data)


@app.route('/match/<username>', methods=['POST', 'GET'])
def match(username):
    """match page"""
    if request.method == "GET":
        my_friends = get_my_friends(username)
        return render_template('match.html', username=username, my_friends=my_friends)
    else:
        # match_users()
        # data = cgi.FieldStorage()
        # username = data['username'].value
        # print("returned username", username)
        click = request.form['data']
        print("returned click", click)
        # match1 = request.args.get['match1']
        # print("match1", match1)
        # match1 = data['match1'].value
        # print("returned match1 ", match1)
        # match2 = data['match2'].value
        # print("Returned match 2", match2)

        # as_dict = request.form.getlist('myform')
        print("check that this works")
        # print (request)
        my_friends = get_my_friends(username)
        friend_username = request.args.get('friend_username')
        potential_matches = get_potential_matches(friend_username)
        print(potential_matches)
        return render_template('match.html', username=username, my_friends=my_friends)


if __name__ == '__main__':
    """runs the application on a server"""
    app.run(debug=False, host='0.0.0.0', port=8000)
