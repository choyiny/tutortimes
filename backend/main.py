# imports
from flask import Flask, request, session, redirect, url_for, escape, jsonify
from users import *
import tutortimes


# initializes the flask app
app = Flask(__name__)
app.secret_key = 'HACKVALLEY2017FDU*AUHFDAOIJDA^*&(.'

# create a tutortimes object
server = tutortimes.TutorTimes()

@app.route("/")
def home():
    """() -> str
    The main page for Tutor Times
    """
    return "Welcome to Tutor Times"


@app.route("/api/register", methods=['POST'])
def register():
    """() -> json
    Creates a new user
    """
    json_data = request.json

    # get fields from form
    email = json_data['email']
    name = json_data['name']
    password = json_data['password']
    user_type = json_data['user_type']

    # if the user email is not registered yet
    if server.get_user(email) is None:

        # create a new user object
        new_user = User(name, email, password, user_type)

        # add the user to TutorTimes
        server.add_user(new_user)

        status = "success"

    # else do not allow them to register
    else:
        status = "User email already exists in database"

    # returns the success message
    return jsonify({'result': status})


@app.route("/api/login", methods=['POST'])
def login():
    """() -> json
    Logs in a user by giving them a session
    """

    json_data = request.json

    # check if it is a post method
    if request.method == "POST":

        # get the email in the field
        email = json_data['email']


        # get the password in the field
        password = json_data['password']

        # CASE 1: User is registered
        if server.get_user(email) is not None:

            # obtain their user object
            login_user = server.get_user(email)

            # If password matches
            if login_user.check_password(password):

                # Initiate a session for them
                # initiate a session
                session['email'] = email
                status = "success"

            # If password does not match
            else:

                # do something
                status = "passwords do not match"

        # CASE 2: User is not registered
        else:
            status = "user does not exist in database"

    # return json of result
    return jsonify({'result': status})


@app.route('/api/notify')
def notify():
    """() -> json
    Notifies users by push notifications
    """
    pass


@app.route('/api/new_course', methods=['POST'])
def new_course():
    """() -> json
    Creates a new course.
    """

    # get the course name from json
    json_data = request.json
    course_name = json_data['course_name']

    # get the admin that is creating the course
    admin = server.get_user(escape(session['email']))

    # create the course from the system, and get the course code
    course_code = server.add_course(admin, course_name)

    print(jsonify({'course_code': course_code}))

    # return the json of the course code
    return jsonify({'course_code': course_code})


@app.route('/api/course/<course_code>', methods=['POST', 'GET'])
def view_course(course_code):
    """ (str) -> json
    Get all the details of a course with json
    """
    # load the course from the system
    requested_course = server.get_course(course_code)

    # get the tutor events as a set
    tutor_events = requested_course.get_TutorEvents()

    # return the tutor events as json
    return jsonify({'events': tutor_events})


@app.route('/api/logout')
def logout():
    """() -> json
    Logs out the user and removes them from the session
    """
    session.pop('logged_in', None)

    # return the json of the result
    return jsonify({'result': 'success'})


if __name__ == "__main__":
    app.run()