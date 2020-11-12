from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

load_dotenv()

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=os.getenv("POSTGRES_USER"),pw=os.getenv("POSTGRES_PW"),url=os.getenv("POSTGRES_URL"),db=os.getenv("POSTGRES_DB"))
UPLOAD_FOLDER = os.path.abspath('uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


db = SQLAlchemy(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)



from app import routes, models

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

