from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager

# instanciating app in Flask class
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)

# this line of code - directs the flask app to routes for web routes
from . import routes

from . import models

# new directory for organization
from .auth.routes import auth
app.register_blueprint(auth)

from .api.routes import api
app.register_blueprint(api)

# login persistence
login = LoginManager()
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login.init_app(app)
# login.login_view = ''