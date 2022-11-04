[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8910261&assignment_repo_type=AssignmentRepo)
# Pset 3: Web Application (Version 1)

### This assignment is due **11:59 PM NHT (New Haven Time) on Sunday, October 30, 2022**

## Purpose

The purpose of this assignment is to help you learn or review server-side web programming and to gain familiarity with the [Flask](https://palletsprojects.com/p/flask/) web server framework and HTML templates.

## Rules

You may work with one teammate on this assignment, and we prefer that you do so.

It must be the case that either you submit all of your team’s files or your teammate submits all of your team’s files.
(It must not be the case that you submit some of your team’s files and your teammate submits some of your team’s files.)
Your `README` file and all of your source code files must contain your name and your teammate’s name.

## Your Task

As with Pset 1, assume you are working for Yale's Registrar's Office.
You've been given a database (in file `reg.sqlite`) containing data about classes and courses being offered this semester at Yale.
Your task is to create a web application that allows Yale students and other interested parties to query the database.

## The Database

The database is identical to the one from Pset 1.
Refer to the Pset 1 specification for the list of tables and fields in the database.
As with Pset 1, the database is in a file named `reg.sqlite` in this template repository.

## The Application

Compose a program named `runserver.py`.
When executed with `-h` as a command-line argument, the program must display the following help message describing the program's behavior:

```
$ python runserver.py -h
usage: runserver.py [-h] port

The registrar application

positional arguments:
  port        the port at which the server should listen

optional arguments:
  -h, --help  show this help message and exit
```

> **Note**: The specific verbiage of this help message should be the default for your version of the `argparse` module, which differs slightly between Python 3.9 and 3.10.

Your `runserver.py` must run an instance of the Flask server on the specified port, which must in turn run your application.

> **Note**: Your application code should *not* be in your `runserver.py` program, which should do nothing but start the Flask server on the provided port number.
> The file containing your application code may be named whatever you want, but we suggest something simple such as `regapp.py`.

When a client makes an HTTP request to the server, your application must return an HTML webpage appropriate to the request.
Beyond some [specific endpoints](#specific-endpoints) mentioned below, there are several requirements your application must satisfy:
* Your application's **primary web page** (*i.e.*, the webpage returned by a request to the server's root&mdash;*e.g.* `http://localhost:80/` if your server is running locally listening on port 80) must contain an HTML **`form`** element.
    
    * The form must include four text input fields labeled "Department", "Course Number", "Subject" and "Title".
    These should, respectively, allow the user to specify a department name, a course number, a subject, and a course title.

        > **Note**: The value for "Department" must be used to filter courses by **department name** (*i.e.*, the `deptname` column in the `departments` table).

    * In addition to the text input fields, your form&mdash;like any useable HTML form&mdash;must include a `submit` input field.
    For this assignment, the submit field must be a button labeled "Search".

    * The form may contain other input elements, but any additional elements you include in the form must be of the `hidden` type (that is, they must not be visible to the user when they view the webpage).

* Below the form, the webpage must display an HTML `table` containing the results of the query that was triggered by the most recent submission of the form (or nothing at all if the form has never been submitted), and the form input fields must be filled in with the parameters used to make the most recent query, that is, the values of the input fields as they were upon the most recent submission of the form (if the form has never been submitted, those fields should be empty).
    
    * The columns displayed in the table must be&mdash;in order&mdash;the `crn`, `deptname`, `subjectcode`, `coursenum`, and `title` of each **section** that matches the specified criteria, or of all sections in the database if the user specifies no criteria.
    The columns must be labeled "Department Name", "Subject Code", "Course Number", and "Title", respectively.

    * The table rows must be sorted; the primary sort must be by `deptname` in ascending order, the secondary sort must be by `coursenum` in ascending order, and tertiary sort must be by `crn` in ascending order.

    * A user must be able to click on the `crn` for any of the displayed classes to request more information about that class on a different webpage (the "secondary" page).

    * If the user has submitted the form with empty input fields, the table should contain *all sections* in the database.

* The secondary webpage may take one of any number of different forms, but it must satisfy these requirements:

    * The webpage must display at least the following information about the selected class:

        * `deptname`, `subjectcode`, `coursenum` in a single-row HTML `table`.
        These columns should be labeled "Department Name", "Subject Code", and "Course Number", respectively.
        * `title`, `descrip`, and `prereqs` each in their own section (each of which may be structured as an HTML `table` but does not have to be).
        These sections must be labeled "Title", "Description", and "Prerequisites", respectively.
        * `sectionnumber`, `crn`, `meetinginfo` in a single-row HTML `table`.
        These columns must be labeled "Section Number", "CRN", and "Meetings", respectively.
        * Crosslistings info (`subjectcode` and `coursenum`) in an HTML `table`.
        These columns must be labeled "Subject Code" and "Course Number", respectively.
        * Professors (*i.e.*, `profname`s) in a single-column HTML `table`.
        The column must be labeled "Professors".

    * The webpage must provide a **link** back to the primary webpage to allow the user to perform another class search.
    The resulting instance of the primary webpage must contain exactly the same content as was most recently displayed on the page before the user clicked a `crn` of a course to retrieve the secondary webpage, including both the course results table and filled-in input fields.

    > **Note**: Your application must be *stateful* to accomplish this. 
    > Review the lecture slides on how to create a stateful web application using, *e.g.*, cookies.

* Both webpages must additionally have some kind of header describing what webpage is.
It does not need to be fancy, but it must be there.

* There must also be a footer, **common to both pages**, containing the name and Yale netid of you and your partner, along with a string displaying the server's current day and time, formatted as:

    ```
    [4-digit year]-[month]-[day] [hour (12-hour clock)]:[minute] [AM/PM]
    ```

    > **Note**: To give a concrete example, the time at which this assignment is due would be displayed as "2022-10-30 11:59 PM".
    > A good tool for this job is the [`strftime` function](https://docs.python.org/3/library/datetime.html#datetime.datetime.strftime) in the [`datetime.datetime` class](https://docs.python.org/3/library/datetime.html#datetime.datetime) from the standard library.

## Additional Requirements for 519 Students

If you are enrolled in CPSC 519, your application must satisfy all of the above requirements plus the following:

* The default styling of an HTML table is quite ugly.
Use CSS to spruce up the table:
    * Add padding of `5px` to all sides of every cell in the table
    * Add a solid `1px` wide `gray` border between rows of the table
    * When the mouse hovers over a particular row of the table, change that row's background color to `lightgray`
    * If that's not enough, you are free to style it in any other manner that looks good to you (but nothing else is required)

* Place your CSS into a file named `styles.css` that is loaded by your primary and secondary webpages, but not included directly in those pages

* On the primary page, there must be a button or link labeled "Clear Previous Search" that, when clicked, displays a primary page with empty input fields and no table of results.
It must also be the case that clicking the button or link causes any stored state to be reset to an initial or empty state, including any state local to the browser (such as cookies) and any state stored on the server.

* On the secondary webpage, there must be a clickable item (either a button or a link) labeled "Edit" associated with each of the "Title", "Description", and "Prerequisites" sections.
Upon clicking this button, the user must be presented with a webpage containing a form with a `textarea` element (see [this webpage](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea) for details) initially populated with the current value of that field for the section, and a submit button labeled "Submit".
When the user **submit**s this form, it must send an HTTP `POST` request to your server that will change the value of the field for this course in the database to match the new text that the user entered in the text area.

By the way, even if you are in 419 and not 519, you are more than welcome to attempt these activities.
They will not have any bearing on your grade for this assignment, but they will provide valuable experience in adding features to a webpage that may prove useful in developing your final project.

## Specific Endpoints

There are three endpoints to which your application must respond (assume your server is running locally, listening on port 80):
1. `http://localhost:80/` must return the primary page
2. `http://localhost:80/search?...` must return the results of a search using the parameters in the query string (that is, the primary page).
3. `http://localhost:80/details?crn=...` must return the secondary page populated with information about the course with the `crn` provided in the query string.

All of the endpoints may accept arbitrarily many query parameters, and you may respond to additional endpoints, but you must *at least* respond to these.

Students completing the [additional 519 activities](#additional-requirements-for-519-students) must add endpoints to accomplish those tasks, but the exact names of those endpoints are not specified.

## Error Handling: Bad Server

Since you control the machine that is running both the server application and the database, there is not much we will force you to worry about for server-side errors.
The only error that your program must handle gracefully is the server being started with a port that is not a positive integer.
If the server is started with a command such as `$ python runserver.py notaport`, it should display a meaningful error message and exit with status 1.

## Error Handling: Bad Client

It is an unfortunate truth about web applications of this kind that a user can enter anything they want in their request to your server!
For example, anyone can send a request to a URL such as `http://yourserver:80/details?crn=gobbeldygook`, despite there being no class with crn "gobbeldygook" on which they could have clicked.
This means that starting with this assignment, we will be ramping up the error handling requirements on your software.
Specifically...

### Invalid `crn`

If the user requests a page at a URL such as the example above&mdash;in which the crn value does not appear in a database&mdash;the server must return an appropriate error page as HTML that displays, at a minimum, text that reads "Error: no class with crn gobbeldygook exists". (The "gobbeldygook" part should, of course, be replace with the actual nonexistent crn that was queried.)

Your application must respond with this error page for *any* missing crn, including numeric and non-numeric crns.

### Missing `crn`

If the user requests a page at a URL such as `http://yourserver:80/details` (that is, missing a `crn` query parameter), the application must return an appropriate error page as HTML that displays, at a minimum, text that reads "Error: missing crn in details request"

### Other invalid requests

There are many other requests that the user could send that are "wrong", such as:

* `http://yourserver:notyourport/`
* `http://yourserver:80/notyourapp`
* `http://yourserver:80/search?invalid/query/string`

The only requirement placed on your server in these cases (and similar ones) is that it does not crash when queried with such requests; that is, if the user sends a valid request immediately after an invalid one, the valid request must get the correct result.

## Source Code Guide

Here are the **requirements** for the source code of your solution.

* The `runserver.py` program must start a flask server for your application on the port provided as a command-line argument, listening on all IP addresses
* Your application program must communicate with a SQLite database in a file named `reg.sqlite`, organized as described above.
* Your application program must use SQL prepared statements for every database query.
(This protects the database against SQL injection attacks.)
* Every module used by your program(s) must either be from the Python standard library or written by your team (and included in your submission).
The only exceptions to this are the `flask` module for your web server and the scaffolding files we have provided you this semester (`dialog.py`, `table.py`).

Here are some **recommendations** for the source code of your solution.

* Reuse code from your solution to Pset 2 in this assignment.
* Modularize your application program so that database communication code is cleanly separated from response production code.
    * Use HTML templates to keep your repsonse production code as clear as possible
    * Structure your code according to MVC design principles (the HTML templates are your Views)
* Use cookies to keep track of the application's state

## Submission

Replace the provided `README.md` file (which contains this assignment specification) with your own `README.md` file that conforms to the following requirements.

1. Leave the first line of the file alone (it is the assignment title).

2. Thereafter your `README.md` file must contain:
    * Your name and Yale netid and your teammate’s name and Yale netid (if you worked with a partner)
    * A paragraph describing your contribution, and another paragraph describing your teammate’s contribution.
    Please be thorough; we are looking for two substantial paragraphs, not a sentence or two.
    * A description of whatever help (if any) you received from other people while doing the assignment.
    * A description of the sources of information that you used while doing the assignment, that are not direct help from other people.
    * An indication of how much time you spent doing the assignment, rounded to the nearest hour.
    * Your assessment of the assignment:
        * Did it help you to learn?
        * What did it help you to learn?
        * Do you have any suggestions for improvement? *Etc.*
    * (Optionally) Any information that will help us to grade your work in the most favorable light.
    In particular, describe all known bugs and explain why any `pylint` style warnings you received are unavoidable or why you know better than `pylint` (a convincing argument might negate some `pylint` style penalties you may accrue).

Your `README.md` file must be a plain text file.
**Do not** create your `README.md` file using Microsoft Word or any other word processor, although it may be formatted using [markdown](https://www.markdownguide.org/), like this provided `README.md` file.

Package your assignment files by [creating a release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) on GitHub in your assignment repository. There must be at least two files with the following (exact) names in that repository when you submit it:
* `README.md`
* `runserver.py`

Ensure that any additional files needed by your program (such as your application program or other Python modules) are in the repository snapshot (*i.e.*, commit) captured by the release.

Submit your solution to Canvas (in the assignment named "Web App Version A") as [a link to that release](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases).

As noted above in the [Rules](#rules) section, it must be the case that either you submit all of your team’s files or your teammate submits all of your team’s files.
(It must not be the case that you submit some of your team’s files and your teammate submits some of your team’s files.)
You and your team may submit multiple times; we will grade the latest files that you submit before the deadline unless a particular version is requested as the canonical version.

**Please follow the directions on what to submit and how.**
It will be a big help to us if you get the filenames right and submit exactly what’s asked for.
Thanks.

### Late Submissions

The deadline for this assignment is **11:59 PM NHT (New Haven Time) on Sunday October 30, 2022**.
There is a strict 15 minute grace period beyond the deadline, to be used in case of technical or administrative difficulties, and not for putting final touches on your solution.

Late submissions will receive a 1% deduction for every hour or part thereof after the deadline.
After 48 hours, the Canvas assignment will close and submissions after that time will not receive any credit.

## Grading

Your grade will be based upon:
* **Correctness**, that is, the correctness of your programs as specified by this document.
* **Style**, that is, the quality of your program style.
This includes not only style as qualitatively assessed by the graders (including modularity, cleanliness, and algorithmic efficiency) but also style as reported by the `pylint` tool, using the default settings, and when executed via the command `python -m pylint **/*.py`.

A small part of your grade will be based upon the quality of your program style as reported by `pylint`.
Your grader will start with the 10-point score reported by pylint.
Your *pylint style grade* is your pylint score rounded to the nearest integer (minimum 0).
For example, if your pylint score is 9.8, then your *pylint style grade* will be 10; if your pylint score is 7.4, then your *pylint style grade* will be 7.

If your code fails the tests on some particular functionality, your grader **will not** inspect your code manually to try to assign partial credit for that functionality.
If you believe there is a "quick fix" (*e.g.*, you're missing a closing tag for an HTML element), you may request a manual review for partial credit, but note that in doing so the grader reserves the right to review and re-grade your *entire* submission.
