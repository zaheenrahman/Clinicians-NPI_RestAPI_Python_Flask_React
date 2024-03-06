from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#Enable CORS for all routes
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from app import views

@app.route('/')
def hello():
    return "Testing Backend Initial"
