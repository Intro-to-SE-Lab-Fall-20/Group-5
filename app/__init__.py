from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

from app import routes #it is import this line goes after app =


from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)