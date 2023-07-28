# importing app to route different web directories
from app import app
from .models import Exercise, db, User
from .myfunctions import getExercise, extra_exercies
from flask import request
from flask_cors import cross_origin
from flask_login import login_user, logout_user, current_user, login_required

# if url = localhost:5000/ call this function and return this
@app.route('/')
def index():
    return "Home page"


@app.route('/registration', methods=["POST"])
def registration():

    data = request.get_json()
    print(data)
    name = data["name"]
    username = data["username"]
    sex = data["sex"]
    email = data["email"]
    password = data["password"]

    status = "OK"
    # check for email match in user table
    email_used = User.query.filter_by(email=email).first()
    if email_used:
        data = "emailUsed"
    # check for username match in user table
    username_taken = User.query.filter_by(username=username).first()
    if username_taken:
        data = "usernameTaken"
    
    # if email and username are unique to User database - add and send back successful creation data
    if not email_used and not username_taken:
        user = User(name, username, sex, email, password)
        user.save_user()
        data = "created"

    return {
        "status" : status,
        "data" : data
    }

@app.route('/login', methods=["POST"])
def login():
    
    data = request.get_json()
    print(data)

    status = "OK"

    username_email =  data["username_email"]
    password = data["password"]
    un_em_match = User.query.filter_by(username=username_email).first()
    if not un_em_match:
        un_em_match = User.query.filter_by(email=username_email).first()
        if not un_em_match:
            data = "wrongUsernameEmail"
            return {
                "status" : status,
                "data" : data
            }

    if un_em_match.password == password:
        data = "authenticated"
        user = un_em_match
        login_user(user)
        user_dict = user.to_dict()
        return {
            "status" : status,
            "data" : data,
            "user" : user_dict
        }
    else:
        data = "wrongPassword"
        return {
            "status" : status,
            "data" : data,
        }

@app.route('/logout', methods=["POST"])
def logout():
    status = "OK"
    logout_user()
    data = "successful"
    return {
            "status" : status,
            "data" : data,
        }

@app.route('/signin-check', methods=["POST"])
def signin_check():
    status = "OK"

    if current_user.username:
        user = User.query.get(current_user.id)
        data = user.to_dict()
        return {
            "status" : status,
            "data" : data,
        }
    
    data = None
    return {
            "status" : status,
            "data" : data,
        }











@app.route('/add-exercise/<password>')
def add_exercise(password):
    if password != "a-secret":
         return "Password was incorrect"
    
    # Add exercises to the elephant sql database using this route and password.
    # change the stop and start range values in the 'for k' loop. k is the 'page' value, on each page the getExercise function returns 10
    # exercises. The 'for j' block loope thru each exercise, checks if it is already in the sql database and adds it if it is not.

    # Current number of exercises: 427 <--- update number if any changes are made.

    master_li = []
    # loop thru pages of 10 exercises each i.e. 0-10 loops thru 100 total exercises
    for k in range(0,1):
        data = getExercise(k)
        li = []

        # loop thru each of the 10 exercises on the page
        for j in range(len(data)):

            name = data[j]["name"]
            tipo = data[j]["type"]
            muscle = data[j]["muscle"]
            equip = data[j]["equipment"]
            diff = data[j]["difficulty"]
            instruct = data[j]["instructions"]

            # duplicate check
            second_check = True
            duplicate = Exercise.query.filter_by(name=name).first()
            if duplicate:
                if duplicate.equipment == equip:
                    second_check = False
            if second_check:
                
                exercise = Exercise(name, tipo, muscle, equip, diff, instruct)
                # add exercise to list to be printed on the html page
                li.append(exercise.to_dict())
                # db.session.add(exercise)

        # add each exercise list (of 10) to a master list to be returned on html page
        master_li.append(li)

    # if no new exercises passed thru passed the duplicate test - Nothing new to commit is returned
    empty = True
    for l in master_li:
        if len(l) >= 1:
            empty = False
    if empty:    
        return "Nothing new to commit"
    
    # COMMENT IN 'db.session.add(exercise)' ABOVE AND 'db.session.commit()' BELOW TO ADD EXERCISES TO THE DATABASE
    # db.session.commit()

    return master_li


