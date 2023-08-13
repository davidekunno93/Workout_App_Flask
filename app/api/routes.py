from flask import Blueprint, request
from ..models import Exercise, Workout, User, Pexercise
from sqlalchemy.orm import aliased

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
    workouts = Workout.query.order_by(Workout.time_created).all()
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
    
@api.get('/pexercise-database')
def pexercise_database():

    pexercises = Pexercise.query.all() 
    data = [p.to_dict() for p in pexercises]

    return {
        "status": "OK",
        "data": data
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
    for m in data["muscles"]:
        muscles.append(m.strip().title())

    print(muscles)

    combos = []
    c = []

    # make a list of up to 3 muscle groups from entry muscles
    for m in muscles:
        if len(c) < 3:
            c.append(m)

    combos.append(c)

    # if combo length is 1 - pass, if 2 - reverse and add to combos, if 3 - 1,3,2 / 2,3,1 / 2,1,3 / 3,2,1 / 3,1,2 add all to combos
    if len(c) == 1:
        pass
    elif len(c) == 2:
        combos.append(list(reversed(c)))
    elif len(c) == 3:
        combos.append([c[0], c[2], c[1]])
        combos.append([c[1], c[2], c[0]])
        combos.append([c[1], c[0], c[2]])
        combos.append([c[2], c[1], c[0]])
        combos.append([c[2], c[0], c[1]])
    
    queries = []
    for combo in combos:
        query = "%".join(combo)
        queries.append("%"+query+"%")
    
    # print(queries, "<--COMBO METHOD")

    # join = "%"
    # l = 0
    # for m in muscles:
    #     if l < 3:
    #         join += m+"%"
    #         l += 1
    # print(join, "<--JOIN METHOD")

    # print(data["circuits"])

    workouts = []
    for query in queries:
        matches = Workout.query.filter(Workout.muscle_groups.like(query)).all()
        for match in matches:
            if match not in workouts:
                workouts.append(match)
    
    print(workouts)
    Workout.query.filter_by(intRating=data["intensity"])

    # print(workouts, "<--COMBO WOS")
    print(data["circuits"], data["intensity"])    

    workouts2 = []
    for m in muscles:
        if not data["circuits"] and not data["intensity"]:
            print("lane")
            subquery = Workout.query.filter(Workout.muscle_groups.like(f"%{m}%")).all()
        elif data["circuits"] and not data["intensity"]:
            subquery = Workout.query.filter(Workout.muscle_groups.like(f"%{m}%"), Workout.circuits > 1).all()
        elif not data["circuits"] and data["intensity"]:
            subquery = Workout.query.filter(Workout.muscle_groups.like(f"%{m}%"), Workout.intRating.like(data["intensity"])).all()
        elif data["circuits"] and data["intensity"]:
            subquery = Workout.query.filter(Workout.muscle_groups.like(f"%{m}%"), Workout.circuits > 1, Workout.intRating.like(data["intensity"])).all()

        for s in subquery:
            if s not in workouts2:
                workouts2.append(s)
    print(workouts2)
    finalworkouts = []
    for wo in workouts:
        if wo in workouts2:
            finalworkouts.append(wo)

    for wo in workouts2:
        if wo not in finalworkouts:
            finalworkouts.append(wo)
    
    print(finalworkouts)

    data = [wo.to_dict() for wo in finalworkouts]
    # print(data)

    return {
        "status" : status,
        "message" : "got it!",
        "data" : data
    }