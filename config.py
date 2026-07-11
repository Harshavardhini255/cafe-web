import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'wakecup-secret-key-change-in-prod')
    _uri = os.environ.get('DATABASE_URL', 'sqlite:///wakecup.db')
    if _uri.startswith('postgres://'):
        _uri = _uri.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
