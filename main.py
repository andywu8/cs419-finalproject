"""main file to run flask app"""

from flask import Flask, render_template, request, redirect, url_for
from models import login, insert_friend, retrieve_potential_friends, retrieve_users, check_user_exists, insert_user, edit_profile_info, add_friend, get_my_friends, get_potential_matches, insert_dummy_users, match_users, retrieve_profile_info, get_matches_in_inbox, update_inbox, get_matched_boolean

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
            return redirect(url_for('match', username=username))
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
    confirmation_message = None
    show_header = True
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        residential_college = request.form.get('residential_college')
        class_year = request.form.get('class_year')
        gender = request.form.get('gender')
        orientation = request.form.get('orientation')
        match_preference = request.form.get('match_preference')

        edit_profile_info(username, phone_number, residential_college,
                          class_year, gender, orientation, match_preference)
        confirmation_message = "Profile has been updated"
        return render_template('profile.html', username=username, 
                                number=phone_number,
                                college=residential_college,
                                class_year=class_year,
                                gender=gender,
                                orientation=orientation,
                                match_preference=match_preference,
                                confirmation_message=confirmation_message,
                                show_header=show_header)
    dict_info = retrieve_profile_info(username)
    if dict_info["number"] == None:
        show_header = False
    return render_template('profile.html', username=username,
                           number=dict_info["number"],
                           college=dict_info["college"],
                           class_year=dict_info["class_year"],
                           gender=dict_info["gender"],
                           orientation=dict_info["orientation"],
                           match_preference=dict_info["match_preference"],
                           show_header=show_header)


# @app.route('/dashboard/<username>', methods=['POST', 'GET'])
# def dashboard(username):
#     """dashboard page"""
#     if request.method == 'POST':
#         residential_college = request.form.get('residential_college')
#         class_year = request.form.get('class_year')
#         gender = request.form.get('gender')
#         orientation = request.form.get('orientation')
#         match_preference = request.form.get('match_preference')

#         edit_profile_info(username, residential_college,
#                           class_year, gender, orientation, match_preference)

#     return render_template('dashboard.html', username=username)


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
            return redirect(url_for('profile', username=username))
        else:
            error_messages.append("Username already exists")

    users = retrieve_users()
    print("users", users)
    return render_template('signup.html', users=users, error_messages=error_messages)


@app.route('/find_friends/<username>', methods=['POST', 'GET'])
def find_friends(username):
    """find friends page"""
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


@app.route('/inbox/<username>', methods=['POST', 'GET'])
def inbox(username):
    """inbox page"""
    if request.method == 'GET':
        inbox_data = get_matches_in_inbox(username)
        print("inbox data is ", inbox_data)


        # dummy_inbox_data = [["ann1234", None], ["adl55", "ann", None], ["adl55", "ann1", True], ["adl55", "annettelee", False]]
        return render_template('inbox.html', username=username, inbox_data = inbox_data)
    else:
        match_status = request.form['Status']
        if match_status == "Accept":
            matched_boolean = True
        else:
            matched_boolean = False
    
        print("matched boolean", matched_boolean)
        match_user = request.form['potential_match']
        update_inbox(match_user, username, matched_boolean)
        print(match_user, "match user")
        #update the database accept/decline status to either True or False for that match username
        inbox_data = get_matches_in_inbox(username)
        print("inbox data is ", inbox_data)
        # dummy_inbox_data = [["adl55", "ann1234", None], ["adl55", "ann", None], ["adl55", "ann1", True], ["adl55", "annettelee", False]]
        return render_template('inbox.html', username=username, inbox_data = inbox_data)

    # format for dummy data
    # [matched_user1, matched_user2, matched_boolean]
    # make sure the user names are actually real usernames: these are just for example
    # example dummy_inbox_data = [["anwu8", "anwu888", None], ["anwu8", "anwu888", True], ["anwu8", "anwu888", False]]

@app.route('/inbox/<username>/view_profile', methods=['GET'])
def view_profile(username):
    """view matches' profile info"""
    match = request.args.get('match')
    dict_info = retrieve_profile_info(match)
    matched_boolean = get_matched_boolean(username, match)
    return render_template('view_profile.html', username=username,
                           matched_boolean=matched_boolean,
                           first_name=dict_info["first_name"],
                           last_name=dict_info["last_name"],
                           number=dict_info["number"],
                           college=dict_info["college"],
                           class_year=dict_info["class_year"],
                           gender=dict_info["gender"],
                           orientation=dict_info["orientation"])

# @app.route('/inbox/<username>/view_potential', methods=['GET'])
# def view_potential(username):
#     """view potential matches' profile info"""
#     potential_match = request.args.get('potential_match')
#     dict_info = retrieve_profile_info(potential_match)
#     return render_template('view_potential.html', username=username,
#                            first_name=dict_info["first_name"],
#                            last_name=dict_info["last_name"],
#                            college=dict_info["college"],
#                            class_year=dict_info["class_year"],
#                            gender=dict_info["gender"],
#                            orientation=dict_info["orientation"])

# @app.route('/inbox/<username>/view_matched', methods=['GET'])
# def view_matched(username):
#     """view matches' profile info"""
#     match = request.args.get('match')
#     dict_info = retrieve_profile_info(match)
#     return render_template('view_matched.html', username=username,
#                            first_name=dict_info["first_name"],
#                            last_name=dict_info["last_name"],
#                            number=dict_info["number"],
#                            college=dict_info["college"],
#                            class_year=dict_info["class_year"],
#                            gender=dict_info["gender"],
#                            orientation=dict_info["orientation"])


@app.route('/match/<username>', methods=['POST', 'GET'])
def match(username):
    """match page"""
    if request.method == "GET":
        my_friends = get_my_friends(username)
        return render_template('match.html', username=username, my_friends=my_friends)
    else:
        match1_username = request.form['match1_username']
        print("match1_username", match1_username)
        match2_username = request.form['match2_username']
        print("match2_username", match2_username)
        match_users(username, match1_username, match2_username)

        my_friends = get_my_friends(username)
        friend_username = request.args.get('friend_username')
        potential_matches = get_potential_matches(friend_username)
        print(potential_matches)
        return render_template('match.html', username=username, my_friends=my_friends)


if __name__ == '__main__':
    """runs the application on a server"""
    app.run(debug=False, host='0.0.0.0', port=8000)
