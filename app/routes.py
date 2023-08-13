# importing app to route different web directories
from app import app
from .models import Exercise, db, User, Workout, Pexercise
from .myfunctions import getExercise, extra_exercies, top4, listToText, dashList
from flask import request, render_template
from flask_cors import cross_origin
from flask_login import login_user, logout_user, current_user, login_required

# if url = localhost:5000/ call this function and return this
@app.route('/')
def index():
    return render_template("index.html")


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

@app.route('/login', methods=["GET","POST"])
def login():
    
    # user = User.query.filter_by(username="davidekunno").first()
    # if user:
    #     login_user(user)
    #     print(user, "logged in")
    # return render_template('index.html')
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
        print("user logged in")
        user_dict = user.to_dict_secure()
        
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
    data = "successful logout"
    return {
            "status" : status,
            "data" : data,
        }

@app.route('/signin-check', methods=["POST"])
def signin_check():
    status = "OK"

    try:
        user = User.query.get(current_user.id)
        data = user.to_dict()
        print("returning data")
        return {
            "status" : status,
            "data" : data,
        }
    except:
        data = None
        print("no user")
        return {
                "status" : status,
                "data" : data,
            }
    
@app.route('/reload-user', methods=["POST"])
def reload_user():

    data = request.get_json()
    print(data)

    user_id = data["user_id"]
    user = User.query.filter_by(id=user_id).first()
    print(user)

    data = user.to_dict_secure()

    return data

@app.route('/create-workout', methods=["POST"])
def create_workout():

    status = "OK"
    data = request.get_json()

    if not data[-1]["info"]["name"]:
        return {
            "status" : status,
            "message" : "No name",
            "data" : "noName"
        }
    
    # muscles = []
    # names = []

    # for obj in data[:-1]:
    #     names.append(obj["name"])
    #     muscles.append(obj["muscle"])

    # ex_names_dash = "*".join(names)
    # print(names)
    # print(ex_names_dash)
    # print(listToText(list(set(names))))
    # # print(str(names))

    # print(muscles)
    # print(listToText(list(set(muscles))))
    # # print(str(muscles))

    # return {
    #     "status" : status,
    #     "message" : "working"
    # }

    # Creating the pexercises
    user_id = data[-1]["info"]["user_id"]
    for ex in data[:-1]:
        dup = Pexercise.query.filter_by(madeby_user_id=user_id, exercise_id=ex["id"], sets=ex["sets"], reps=ex["reps"], intensity=ex["intensity"]).first()
        if not dup:    
            # print(user_id, ex["id"], ex["sets"], ex["reps"], ex["intensity"])
            pexercise = Pexercise(user_id, ex["id"], ex["sets"], ex["reps"], ex["intensity"])
            db.session.add(pexercise)
    db.session.commit()
    
    pex_list = []
    for ex in data[:-1]:
        pex = Pexercise.query.filter_by(madeby_user_id=user_id, exercise_id=ex["id"], sets=ex["sets"], reps=ex["reps"], intensity=ex["intensity"]).first()
        pex_list.append(pex.id)

    # str_pex_list = str(pex_list)
    # print(str_pex_list)

    # return {
    #     "status" : status,
    #     "message" : "We are rolling",
    #     "data" : pex_list
    # }

    # defining new attributes of the workout
    muscles = []
    reps = 0
    t_reps = 0
    names = []
    intensities = []
    endurance = ""
    
    for obj in data[:-1]:
        names.append(obj["name"])
        muscles.append(obj["muscle"])
        reps += obj["reps"]*obj["sets"]
        intensities.append(obj["intensity"])

    t_reps = reps*int(data[-1]["info"]["circuits"])
    if t_reps <= 48:
        endurance = 1
    elif t_reps > 48 and t_reps <= 96:
        endurance = 2
    elif t_reps > 96 and t_reps <= 144:
        endurance = 3
    elif t_reps > 144 and t_reps <= 192:
        endurance = 4
    elif t_reps > 192:
        endurance = 5
    

    def intensityScore(ints):
        "takes list of intensities and returns an average intensity: light, medium or heavy"
        body_only = False
        score = 0
        ints_final = []
        for v in ints:
            if v == "light":
                score += 30
                ints_final.append(v)
            elif v == "medium":
                score += 60
                ints_final.append(v)
            elif v == "heavy":
                score += 100
                ints_final.append(v)
            # this line is irrelevant for functionality but shows the body only exs without an intesity aren't disrupting intScore or rating
            elif v == "na":
                pass
        if len(ints_final) == 0:
            body_only = True
            rating = "bodyOnly"
            avg_score = 0
        else:
            avg_score = score//(len(ints_final))
            if avg_score < 45:
                rating = "light"
            elif avg_score >= 45 and avg_score < 80:
                rating = "medium"
            elif avg_score >= 80:
                rating = "heavy"
        d = {}
        d["intScore"] = avg_score
        d["intRating"] = rating
        d["bodyOnly"] = body_only
        return d

    intensity = intensityScore(intensities)
    # print(names, muscles, t_reps, endurance, intensity, sep="\n")
    
    main_muscles = top4(muscles)

    # add new attributes to workout in the info section
    data[-1]["info"]["bodyOnly"] = intensity["bodyOnly"]
    data[-1]["info"]["totalReps"] = t_reps
    data[-1]["info"]["endScore"] = endurance
    data[-1]["info"]["intScore"] = intensity["intScore"]
    data[-1]["info"]["intRating"] = intensity["intRating"]
    data[-1]["info"]["muscle_groups"] = list(set(muscles))
    data[-1]["info"]["main_muscles"] = main_muscles
    data[-1]["info"]["ex_names"] = names



    names_text = (listToText(list(set(names))))
    muscles_text = (listToText(list(set(muscles))))
    main_muscles_text = (listToText(main_muscles))
    pex_list_dash = dashList(pex_list)
    ex_names_dash = "*".join(names)

    name_dup = Workout.query.filter_by(wo_name=data[-1]["info"]["name"]).first()
    if name_dup:
        return {
            "status" : "OK",
            "message" : "nameDuplicate",
            "data" : "nameDuplicate"
        }

    # workout inputs = Workout(user_id, wo_name, wo_desc, exercises, ex_names, muscle_groups, main_muscles, total_reps, intScore, intRating, endScore, circuits)
    workout = Workout(user_id, data[-1]["info"]["name"], data[-1]["info"]["desc"], pex_list_dash, names_text, ex_names_dash, muscles_text, main_muscles_text, t_reps, intensity["intScore"], intensity["intRating"], endurance, data[-1]["info"]["circuits"])
    # dup query returns None if no match
    dup = Workout.query.filter_by(pexercise_ids=pex_list_dash).first()
    if dup:
        return {
            "status" : status,
            "message" : "workoutDuplicate",
            "data" : "workoutDuplicate"
        }
    
    workout.save_workout()
    
    new_workout = Workout.query.filter_by(pexercise_ids=pex_list_dash).first()
    data = new_workout.to_dict()

    # print(data)
    message = "successful"
    return {
        "status" : status,
        "data" : data,
        "message" : message
    }


@app.route("/add-to-favorites", methods=["POST"])
def addToFavorites():

    data = request.get_json()

    print(data)

    # return "check"

    w_id = data["workout_id"]
    u_id = data["user_id"]

    workout = Workout.query.filter_by(id=w_id).first()
    print(workout)
    user = User.query.filter_by(id=u_id).first()
    print(user)

    print(user.favorited)
    if workout not in user.favorited:
        print("not in user favorited")
        workout.add_to_favorites(user)

    if workout in user.favorited:
        print("now in user favorited")

    print(user.favorited)

    workouts = Workout.query.order_by(Workout.time_created.desc()).all()
    data = [w.to_dict() for w in workouts]
    
    return {
        "status": "OK",
        "message" : "Complete",
        "data" : data
    }

@app.route("/remove-from-favorites", methods=["POST"])
def removeFromFavorites():

    data = request.get_json()

    print(data)

    # return "check"

    w_id = data["workout_id"]
    u_id = data["user_id"]

    workout = Workout.query.filter_by(id=w_id).first()
    print(workout)
    user = User.query.filter_by(id=u_id).first()
    print(user)

    print(user.favorited)
    if workout in user.favorited:
        print("in user favorited")
        workout.remove_from_favorites(user)

    if workout not in user.favorited:
        print("no longer in user favorited")

    # print(user.favorited)

    workouts = Workout.query.order_by(Workout.time_created.desc()).all()
    data = [w.to_dict() for w in workouts]
    return {
        "status": "OK",
        "message" : "Complete",
        "data" : data
    }




















@app.route('/update-workout/<password>')
def update_workout(password):
    if password != "a-secret":
         return "Password was incorrect"
    
    # pull model object from db to class object
    workout = Workout.query.get('2')

    # updated the attribute of the class object
    # workout.ex_names = 

    # add changes to database


    # commit changes to database
    
    return "Under construction"





















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


