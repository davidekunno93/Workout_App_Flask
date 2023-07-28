# functions that you wish to incorporate in the route files
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), nullable=False, unique=True)
    sex = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    workout = db.relationship('Workout', backref='author', lazy=True)


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
        d["name"] = self.name
        d["username"] = self.username
        d["sex"] = self.sex
        d["email"] = self.email
        d["password"] = self.password
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
        d["name"] = self.name
        d["ex_type"] = self.ex_type
        d["muscle"] = self.muscle
        d["equipment"] = self.equipment
        d["difficulty"] = self.difficulty
        d["instructions"] = self.instructions
        return d

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdby_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    completedby_user_ids = db.Column(db.String)
    exercises = db.Column(db.String, nullable=False)
    rating = db.Column(db.Numeric(2,1))
    num_of_ratings = db.Column(db.Integer)
    num_of_favs = db.Column(db.Integer)
    reviews = db.Column(db.String)
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
    reviewed = db.relationship('User',
            secondary = 'reviews',
            backref = 'reviewed',
            lazy = 'dynamic'
            )
    
    def __init__(self, user, exercises, reviews, rating=None, num_of_ratings=0, num_of_favs=0):
        self.createdby = user
        self.exercises = exercises
        self.reviews = reviews
        self.rating = rating
        self.num_of_ratings = num_of_ratings
        self.num_of_favs = num_of_favs
    
    def addReview(self, review):
        # review must be dict of {user id: #, rating: #, review: ""}
        self.num_of_ratings += 1
        self.rating = round(((self.rating*(self.num_of_ratings-1) + review["rating"]) / self.num_of_ratings)*10)/10
        self.reviews.append(review)
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

favorites = db.Table(
    'favorites',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False),
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), nullable=False)
)

reviews = db.Table(
    'reviews',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False),
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), nullable=False)
)