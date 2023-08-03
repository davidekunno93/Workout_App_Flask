from flask import Blueprint, request
from ..models import Exercise, Workout, User

api = Blueprint('api', __name__, url_prefix='/api')

@api.get('/exercise-database')
def exercise_database():
    exercises = Exercise.query.all()
    database = [e.to_dict() for e in exercises]
    if database:
        return {
            'data' : database,
            'status' : 'ok'
        }
    else:
        return {
            'data' : 'Not Found',
            'status' : 404
        }
    
@api.get('/workout-database')
def workout_database():
    workouts = Workout.query.all()
    database = [w.to_dict() for w in workouts]
    if database:
        return {
            'data' : database,
            'status' : 'ok'
        }
    else:
        return {
            'data' : 'Not Found',
            'status' : 404
        }
    
@api.get('/users-database')
def users_database():
    users = User.query.all()
    database = [u.to_dict_secure() for u in users]
    if database:
        return {
            'data' : database,
            'status' : 'ok'
        }
    else:
        return {
            'data' : 'Not Found',
            'status' : 404
        }

@api.route('/exercise-search', methods=["POST"])
def exercise_search():
    
    data = request.get_json()
    m = False
    d = False
    n = False



    if "no-weights" in data:
        no_weights = data["no-weights"]
        n = True
    else:
        print("no no-weights")
    if data["difficulty"]:
        diff = data["difficulty"]
        d = True
    if data["muscle"]:
        muscle = data["muscle"]
        m = True


    if m and d and n:
        exercises = Exercise.query.filter_by(muscle=muscle, equipment=no_weights, difficulty=diff).all()
    elif m and d and not n:
        exercises = Exercise.query.filter_by(muscle=muscle, difficulty=diff).all()
    elif m and n and not d:
        exercises = Exercise.query.filter_by(muscle=muscle, equipment=no_weights).all()
    elif m and not d and not n:
        exercises = Exercise.query.filter_by(muscle=muscle).all()
    elif d and n and not m:
        exercises = Exercise.query.filter_by(equipment=no_weights, difficulty=diff).all()
    elif d and not m and not n:
        exercises = Exercise.query.filter_by(difficulty=diff).all()
    elif n and not m and not d:
        exercises = Exercise.query.filter_by(equipment=no_weights).all()
    else:
        exercises = Exercise.query.all()

    # print(f"muscle is {m}, diff is {d}, and no-weights is {n}")
    exercises = [e.to_dict() for e in exercises]

    ## Check the first 5 objects we're getting
    # k = 0
    # li = []
    # while k <= 5:
    #     for e in exercises:
    #         li.append(e.to_dict())
    #         k += 1
    #         if k >= 5:
    #             break
    # print(li)
    return {
        "status" : "OK",
        "data" : exercises
    }

@api.route('/search-workout', methods=["POST"])
def search_workout():

    status = "OK"
    data = request.get_json()
    print(data)

    muscles = []
    for m in data:
        muscles.append(m.strip().lower())
    
    print(muscles)

    for m in muscles:
        Workout.query.filter_by

    return {
        "status" : status,
        "message" : "got it!",
        "data" : "coming soon"
    }