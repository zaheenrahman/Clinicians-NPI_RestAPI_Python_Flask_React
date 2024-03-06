import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '22844ec8f08a2bc7cc15dabe1a1497f1'  # Used for form validation