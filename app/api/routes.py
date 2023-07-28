from flask import Blueprint, request
from ..models import Exercise

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
    
@api.route('/exercise-search', methods=["POST"])
def exercise_search():
    
    data = request.get_json()
    
    muscle = data["muscle"]
    equip = data["equipment"]
    diff = data["difficulty"]

    exercises = Exercise.query.filter_by(muscle=muscle, equipment=equip, difficulty=diff).all()

    return {
        "status" : "OK",
        "data" : exercises
    }
