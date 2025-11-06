import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY','dev_key') # Default secret key for development
    SQLALCHEMY_DATABASE_URI =  'sqlite:///database.db'  # Default SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications to save resources
    