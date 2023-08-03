# functions that you wish to incorporate in the route files
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), nullable=False, unique=True)
    sex = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    workout = db.relationship('Workout', backref='author', lazy=True)
    completes = db.relationship('Workout',
                secondary = 'completes',
                backref = 'completes',
                lazy = 'dynamic'
                )


    def __init__(self, name, username, sex, email, password):
        self.name = name
        self.username = username
        self.sex = sex
        self.email = email
        self.password = password

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["username"] = self.username
        d["sex"] = self.sex
        d["email"] = self.email
        d["password"] = self.password
        return d
    
    def to_dict_secure(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["username"] = self.username
        d["sex"] = self.sex
        d["email"] = self.email
        return d

class Exercise(db.Model):
    """
    params: name, ex_type, muscle, equipment, difficulty, instructions
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    ex_type = db.Column(db.String, nullable=False)
    muscle = db.Column(db.String, nullable=False)
    equipment = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    

    def __init__(self, name, ex_type, muscle, equipment, difficulty, instructions):
        self.name = name
        self.ex_type = ex_type
        self.muscle = muscle
        self.equipment = equipment
        self.difficulty = difficulty
        self.instructions = instructions

    
    def addExercise(self):
        db.session.add(self)
        db.session.commit()
    
    def create(self, user):
        self.created.append(user)
        db.session.commit()

    def unfavorite(self, user):
        self.favorited.remove(user)
        db.session.commit()

    def favorite(self, user):
        self.favorited.append(user)
        db.session.commit()

    def unfavorite(self, user):
        self.favorited.remove(user)
        db.session.commit()

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["ex_type"] = self.ex_type
        d["muscle"] = self.muscle
        d["equipment"] = self.equipment
        d["difficulty"] = self.difficulty
        d["instructions"] = self.instructions
        return d

class Pexercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    madeby_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.String)
    pexes = db.relationship('Workout',
            secondary = 'wo_pexes',
            backref = 'pexes',
            lazy = 'dynamic'
            )

    def __init__(self, user_id, exercise_id, sets, reps, intensity):
        self.madeby_user_id = user_id
        self.exercise_id = exercise_id
        self.sets = sets
        self.reps = reps
        self.intensity = intensity

    def save_pex(self):
        db.session.add(self)
        db.session.commit()

    

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdby_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wo_name = db.Column(db.String, unique=True, nullable=False)
    wo_desc = db.Column(db.String)
    completedby_user_ids = db.Column(db.String)
    pexercise_ids = db.Column(db.String, nullable=False, unique=True)
    ex_names = db.Column(db.String)
    ex_names_dash = db.Column(db.String)
    muscle_groups = db.Column(db.String)
    main_muscles = db.Column(db.String)
    total_reps = db.Column(db.Integer)
    intScore = db.Column(db.Integer)
    intRating = db.Column(db.String)
    endScore = db.Column(db.Integer)
    circuits = db.Column(db.Integer)
    avg_rating = db.Column(db.Numeric(3,2))
    num_of_ratings = db.Column(db.Integer)
    num_of_favs = db.Column(db.Integer)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    created = db.relationship('User',
            secondary = 'creations',
            backref = 'created',
            lazy = 'dynamic'
            )
    completed = db.relationship('User',
            secondary = 'completions',
            backref = 'completed',
            lazy = 'dynamic'
            )
    favorited = db.relationship('User',
            secondary = 'favorites',
            backref = 'favorited',
            lazy = 'dynamic'
            )

    
    def __init__(self, user_id, wo_name, wo_desc, pexercise_ids, ex_names, ex_names_dash, muscle_groups, main_muscles, total_reps, intScore, intRating, endScore, circuits, completedby = [], avg_rating=0, num_of_ratings=0, num_of_favs=0):
        self.createdby_user_id = user_id
        self.wo_name = wo_name
        self.wo_desc = wo_desc
        self.completedby_user_ids = completedby
        self.pexercise_ids = pexercise_ids
        self.ex_names = ex_names
        self.ex_names_dash = ex_names_dash
        self.muscle_groups = muscle_groups
        self.main_muscles = main_muscles
        self.total_reps = total_reps
        self.intScore = intScore
        self.intRating = intRating
        self.endScore = endScore
        self.circuits = circuits
        self.avg_rating = avg_rating
        self.num_of_ratings = num_of_ratings
        self.num_of_favs = num_of_favs
    
    def save_workout(self):
        db.session.add(self)
        db.session.commit()

    # haven't tried this command - not sure of its functionality
    def remove_workout(self):
        db.session.delete(self)
        db.session.commit()

    def update_rating(self, rating):
        # function called inside Review class function - add_review
        self.rating = round(((self.rating*(self.num_of_ratings) + rating) / self.num_of_ratings+1), 2)
        self.num_of_ratings += 1
        db.session.commit()

    def to_dict(self):
        d = {}
        user = User.query.get(self.createdby_user_id)
        d["createdby_id"] = self.createdby_user_id
        d["createdby_un"] = user.username
        d["wo_name"] = self.wo_name
        d["wo_desc"] = self.wo_desc
        d["completedby_user_ids"] = self.completedby_user_ids
        d["pexercise_ids"] = self.pexercise_ids
        d["ex_names"] = self.ex_names
        d["ex_names_dash"] = self.ex_names_dash
        d["muscle_groups"] = self.muscle_groups
        d["main_muscles"] = self.main_muscles
        d["totalReps"] = self.total_reps
        d["intScore"] = self.intScore
        d["intRating"] = self.intRating
        d["endScore"] = self.endScore
        d["circuits"] = self.circuits
        d["avgRating"] = self.avg_rating 
        d["numOfRatings"] = self.num_of_ratings
        d["numOfFavs"] = self.num_of_favs
        return d


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    madeby_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wo_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    rating = db.Column(db.Numeric(2,1), nullable=False)
    review = db.Column(db.String)
    
    def __init__(self, user_id, wo_id, rating, review=None):
        self.madeby_user_id = user_id
        self.wo_id = wo_id
        self.rating = rating
        self.review = review
    
    def add_review(self):
        workout = Workout.query.get(self.wo_id)
        workout.update_rating(self.rating)
        db.session.add(self)
        db.session.commit()

creations = db.Table(
    'creations',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False),
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), nullable=False)
)

completions = db.Table(
    'completions',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False),
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), nullable=False)
)

completes = db.Table(
    'completes',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False),
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), nullable=False)
)

favorites = db.Table(
    'favorites',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False),
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), nullable=False)
)

wo_pexes = db.Table(
    'wo_pexes',
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), nullable=False), 
    db.Column("pex_id", db.Integer, db.ForeignKey("pexercise.id"), nullable=False) 
)