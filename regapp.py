from html import escape  # Used to thwart XSS attacks.
from time import strftime, localtime, asctime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from database import search_courses, get_details
import datetime

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

def get_current_time():
    datetime_object = datetime.datetime.now()
    return datetime_object.strftime("%Y-%m-%d, %I:%M %p")

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """render the home page."""

    html = render_template('home.html',
                           time=get_current_time())
    response = make_response(html)

    return response

#-----------------------------------------------------------------------

@app.route('/search', methods=['GET'])
def search_results():
    prev_department= request.cookies.get('prev_department')
    prev_course_number= request.cookies.get('prev_course_number')
    prev_subject= request.cookies.get('prev_subject')
    prev_title= request.cookies.get('prev_title')

    if len(request.args) == 0:
        if prev_department is None:
            prev_department = ''
        else:
            department = prev_department
        if prev_course_number is None:
            prev_course_number = ''
        else:
            course_number = prev_course_number
        if prev_subject is None:
            prev_subject = ''
        else:
            subject = prev_subject
        if prev_title is None:
            prev_title = ''
        else:
            title = prev_title
    else:
        department = request.args.get('Department')
        course_number = request.args.get('Course Number')
        subject = request.args.get('Subject')
        title = request.args.get('Title')


    print(department, course_number, subject, title)
    courses = search_courses(department, course_number, subject, title)

    html = render_template('search_results.html',
                           courses=courses,
                            department=department,
                            course_number=course_number,
                            subject=subject,
                            title=title,
                            time=get_current_time())
    response = make_response(html)

    response.set_cookie('prev_department', department)
    response.set_cookie('prev_course_number', course_number)
    response.set_cookie('prev_subject', subject)
    response.set_cookie('prev_title', title)

    return response


@app.route('/friends', methods=['GET'])
def friends():


    html = render_template('friends.html')
    response = make_response(html)

    return response