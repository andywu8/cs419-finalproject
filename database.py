from sqlite3 import connect
from contextlib import closing
from course import Course
import table

_DATABASE_URL = 'reg.sqlite'

def search_courses(department, course_number, subject, title):
    """Search the database for the given
    query and return the results."""

    courses = []

    with connect(_DATABASE_URL, uri=True) as connection:
        with closing(connection.cursor()) as cursor:
            query = get_courses_query(department, course_number, subject, title)
            args = get_courses_prepared_args(department, course_number, subject, title)
            cursor.execute(query, args)

            row = cursor.fetchone()
            while row is not None:
                course = Course(row[0], row[1], row[2], row[3], row[4])
                courses.append(course)
                row = cursor.fetchone()

            return courses

def get_courses_query(department, course_number, subject, title):
    """Return the query to search for the given
    query and return the results."""

    query_str = "SELECT sections.crn, departments.deptname, coursenum, subjectcode, title "
    query_str += "FROM courses "
    query_str += "JOIN departments on courses.deptcode = departments.deptcode "
    query_str += "JOIN sections on courses.courseid = sections.courseid "

    if department or course_number or subject or title:
        query_str += "WHERE "
        if department:
            query_str += "LOWER(courses.deptcode) LIKE ? "
            if course_number or subject or title:
                query_str += "AND "
        if subject:
            query_str += "LOWER(subjectcode) LIKE ? "
            if course_number or title:
                query_str += "AND "
        if title:
            query_str += "LOWER(title) LIKE ? "
            if course_number:
                query_str += "AND "
        if course_number:
            query_str += "coursenum LIKE ? "

    query_str += "ORDER BY departments.deptname ASC, "
    query_str += "coursenum ASC, sections.crn ASC "

    return query_str

def get_courses_prepared_args(department, course_number, subject, title):
    """Return the prepared arguments for the query to search for the given
    query and return the results."""

    args = []

    if department:
        args.append('%' + department.lower() + '%')
    if subject:
        args.append('%' + subject.lower() + '%')
    if title:
        args.append('%' + title.lower() + '%')
    if course_number:
        args.append('%' + course_number + '%')
    return args

def get_details_query(query_number):
    """Return the query to search for the given crn and return the results."""

    query_str = None
    if query_number == 1:
        query_str = "SELECT departments.deptcode, departments.deptname, subjectcode, coursenum "
        query_str += "FROM courses "
        query_str += "JOIN departments on courses.deptcode = departments.deptcode "
        query_str += "JOIN sections on courses.courseid = sections.courseid "
        query_str += "WHERE sections.crn = ? "
    elif query_number == 2:
        query_str = "SELECT title FROM courses "
        query_str += "JOIN departments on courses.deptcode = departments.deptcode "
        query_str += "JOIN sections on courses.courseid = sections.courseid "
        query_str += "WHERE sections.crn = ? "
    elif query_number == 3:
        query_str = "SELECT descrip FROM courses "
        query_str += "JOIN departments on courses.deptcode = departments.deptcode "
        query_str += "JOIN sections on courses.courseid = sections.courseid "
        query_str += "WHERE sections.crn = ? "
    elif query_number == 4:
        query_str = "SELECT prereqs FROM courses "
        query_str += "JOIN departments on courses.deptcode = departments.deptcode "
        query_str += "JOIN sections on courses.courseid = sections.courseid "
        query_str += "WHERE sections.crn = ? "
    elif query_number == 5:
        query_str = "SELECT sections.sectionnumber, "
        query_str += "CAST(sections.crn AS CHAR) AS crn, meetinginfo "
        query_str += "FROM sections NATURAL JOIN (SELECT crn, "
        query_str += "GROUP_CONCAT((meetings.timestring || ' @ ' || meetings.locstring), '|') "
        query_str += "AS meetinginfo FROM meetings GROUP BY crn) AS meetinginfo "
        query_str += "WHERE sections.courseid IN "
        query_str += "(SELECT courses.courseid FROM COURSES NATURAL JOIN sections "
        query_str += "WHERE CAST(sections.crn AS CHAR) = ?) "
        query_str += "ORDER BY sections.sectionnumber ASC, crn ASC "
    elif query_number == 6:
        query_str = "SELECT courses.subjectcode, courses.coursenum FROM courses "
        query_str += "JOIN crosslistings on crosslistings.secondarycourseid = courses.courseid "
        query_str += "WHERE crosslistings.primarycourseid = (SELECT courses.courseid FROM courses "
        query_str += "NATURAL JOIN sections WHERE sections.crn = ?)"
        query_str += "ORDER BY courses.subjectcode ASC, courses.coursenum ASC "
    elif query_number == 7:
        query_str = "SELECT profname from profs "
        query_str += "JOIN coursesprofs on profs.profid = coursesprofs.profid "
        query_str += "JOIN sections on coursesprofs.courseid = sections.courseid "
        query_str += "WHERE sections.crn = ? "
        query_str += "ORDER BY profname ASC "

    return query_str

def get_details(crn):
    """Search the database for the given crn and return the results."""
    details = []

    with connect(_DATABASE_URL, uri=True) as connection:
        with closing(connection.cursor()) as cursor:
            for i in range(1, 8):
                query = get_details_query(i)
                cursor.execute(query, [crn])
                row = cursor.fetchone()
                batch = []
                while row is not None:
                    batch.append(row)
                    row = cursor.fetchone()
                details.append(batch)
            return details

