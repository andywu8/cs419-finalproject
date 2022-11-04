from flask import Flask
from flask import render_template
from flask import request
import models as dbHandler

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        # dbHandler.insertUser(username, password)
        # users = dbHandler.retrieveUsers()
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dbHandler.insertUser(firstname, lastname, username, password)
        users = dbHandler.retrieveUsers()
        return render_template('signup.html', users=users)
    else:
        return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
