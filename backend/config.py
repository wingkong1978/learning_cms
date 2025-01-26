import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///learning_cms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 