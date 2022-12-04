"""main file to run flask app"""

from flask import Flask, render_template, request, make_response, redirect, url_for, session
from models import login, insert_friend, retrieve_potential_friends, retrieve_users, check_user_exists, insert_user, edit_profile_info, add_friend, get_my_friends, insert_dummy_users, match_users, retrieve_profile_info, get_matches_in_inbox, update_inbox, get_match_recommendations, get_matches_made_by_me
from helper import login_required
from tempfile import mkdtemp
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    """home page"""
    session.clear()
    error_messages = []
    users = None
    confirmation_message = None
    # insert_dummy_users()


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        correct_login = login(username, password)
        if correct_login:
            users = retrieve_users()
            print("users", users)
            session["username"] = username
            return redirect(url_for('match', username=username))
        else:
            error_messages.append("Incorrect username or password")
            return render_template('index.html',
                                   users=users,
                                   error_messages=error_messages,
                                   confirmation_message=confirmation_message)
    else:
        return render_template('index.html')


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    """profile page"""
    confirmation_message = None
    show_header = True
    print("check profile")
    username = session["username"]
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        residential_college = request.form.get('residential_college')
        class_year = request.form.get('class_year')
        gender = request.form.get('gender')
        orientation = request.form.get('orientation')
        match_preference = request.form.get('match_preference')

        edit_profile_info(username, first_name, last_name, phone_number, residential_college,
                          class_year, gender, orientation, match_preference)
        confirmation_message = "Profile has been updated"
        return render_template('profile.html', username=username, 
                                firstname = first_name,
                                lastname = last_name,
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
                           firstname=dict_info["first_name"],
                           lastname=dict_info["last_name"],
                           number=dict_info["number"],
                           college=dict_info["college"],
                           class_year=dict_info["class_year"],
                           gender=dict_info["gender"],
                           orientation=dict_info["orientation"],
                           match_preference=dict_info["match_preference"],
                           show_header=show_header)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """signup page"""
    error_messages = []

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user_exists = check_user_exists(username)

        if not user_exists:
            print("check")
            insert_user(first_name, last_name, username, generate_password_hash(password))
            print("check1")
            session["username"] = username
            return redirect(url_for('profile'))
        else:
            error_messages.append("Username already exists")

    users = retrieve_users()
    print("users", users)
    return render_template('signup.html', users=users, error_messages=error_messages)


@app.route('/find_friends', methods=['POST', 'GET'])
@login_required
def find_friends():
    """find friends page"""
    username = session["username"]
    return render_template('find_friends.html', username=username)


@app.route('/add_friends', methods=['POST', 'GET'])
@login_required
def add_friends():
    """add friends page"""
    username = session["username"]
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        residential_college = request.args.get('residential_college')
        class_year = request.args.get('class_year')
        gender = request.args.get('gender')
        orientation = request.args.get('orientation')

        friends = get_my_friends(username)
        #print("friends", friends)

        potential_friends = retrieve_potential_friends(
            username, friends, first_name, last_name, residential_college, class_year, gender, orientation)

        html = render_template('add_friends.html', username=username, potential_friends=potential_friends)
        response = make_response(html)

        response.set_cookie('prev_first_name', first_name)
        response.set_cookie('prev_last_name', last_name)
        response.set_cookie('prev_residential_college', residential_college)
        response.set_cookie('prev_class_year', class_year)
        response.set_cookie('prev_gender', gender)
        response.set_cookie('prev_orientation', orientation)
        return response
    else:
        prev_first_name = request.cookies.get('prev_first_name')
        prev_last_name = request.cookies.get('prev_last_name')
        prev_residential_college = request.cookies.get('prev_residential_college')
        prev_class_year = request.cookies.get('prev_class_year')
        prev_gender =  request.cookies.get('prev_gender')
        prev_orientation = request.cookies.get('prev_orientation')
        friend_username = request.args.get('friend_username')

        add_friend(username, friend_username)
        friends = get_my_friends(username)
        #print("friends", friends)
        potential_friends = retrieve_potential_friends(
            username, friends, prev_first_name, prev_last_name, prev_residential_college, prev_class_year, prev_gender, prev_orientation)

        return render_template('add_friends.html', username=username, potential_friends=potential_friends)


@app.route('/inbox', methods=['POST', 'GET'])
@login_required
def inbox():
    """inbox page"""
    username = session["username"]
    if request.method == 'GET':
        inbox_data = get_matches_in_inbox(username)
        return render_template('inbox.html', username=username, inbox_data = inbox_data)
    else:
        match_status = request.form['Status']
        if match_status == "Accept":
            matched_boolean = True
        else:
            matched_boolean = False
    
        print("matched boolean", matched_boolean)
        match_user = request.form['potential_match']
        update_inbox(username, match_user, matched_boolean)
        print(match_user, "match user")
        #update the database accept/decline status to either True or False for that match username
        inbox_data = get_matches_in_inbox(username)
        # dummy_inbox_data = [["adl55", "ann1234", None], ["adl55", "ann", None], ["adl55", "ann1", True], ["adl55", "annettelee", False]]
        return render_template('inbox.html', username=username, inbox_data = inbox_data)

    # format for dummy data
    # [matched_user1, matched_user2, matched_boolean]
    # make sure the user names are actually real usernames: these are just for example
    # example dummy_inbox_data = [["anwu8", "anwu888", None], ["anwu8", "anwu888", True], ["anwu8", "anwu888", False]]

@app.route('/view_profile', methods=['GET'])
def view_profile():
    """view matches' profile info"""
    match = request.args.get('match')
    username = session["username"]
    dict_info = retrieve_profile_info(match)
    return render_template('view_profile.html', username=username,
                           first_name=dict_info["first_name"],
                           last_name=dict_info["last_name"],
                           number=dict_info["number"],
                           college=dict_info["college"],
                           class_year=dict_info["class_year"],
                           gender=dict_info["gender"],
                           orientation=dict_info["orientation"])

@app.route('/match', methods=['POST', 'GET'])
@login_required
def match():
    """match page"""
    username = session["username"]
    if request.method == "GET":
        my_friends = get_my_friends(username)
        match_recommendations = None
        return render_template('match.html', username=username, my_friends=my_friends, match_recommendations = match_recommendations)
    else:
        if request.form["type_of_post"] == "get_recommendations":
            print("check it gets here")
            match1_username = request.form['match1_username']
            my_made_matches = get_matches_made_by_me(username)
            my_friends = get_my_friends(username)
            match_recommendations = get_match_recommendations(username, match1_username, my_made_matches)
            html = '''
                <table>
                <tbody>
            '''
            pattern = '''
            <option class="friend-item" value=%s selected>%s %s</option>
            '''

            for friend in match_recommendations:
                html += pattern % (friend[2], friend[0], friend[1])
            html += '''
                </tbody>
                </table>
                '''
            print("html is", html)
            response = make_response(html)
            print("response is", response)
            return response
            # return match_recommendations
            # print("match_recommendations in main", match_recommendations)
        elif request.form["type_of_post"] == "get_match_results":
            match1_username = request.form['match1_username']
            print("match1_username", match1_username)
            match2_username = request.form['match2_username']
            print("match2_username", match2_username)
            match_users(username, match1_username, match2_username)
            my_friends = get_my_friends(username)
            match_recommendations = None
            html = "MATCH SUCCESSFUL"
            response = make_response(html)
            return response
            # response = make_response(render_template('match.html', username=username, my_friends=my_friends, match_recommendations = match_recommendations))

        return render_template('match.html', match1_username=match1_username, username=username, my_friends=my_friends, match_recommendations = match_recommendations)

@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    """runs the application on a server"""
    app.run(debug=False, host='0.0.0.0', port=8000)
