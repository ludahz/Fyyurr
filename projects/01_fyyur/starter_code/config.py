import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


DATABSE_NAME = 'fyyurr'
username = 'ludah'
url = 'localhost:5432'
SQLALCHEMY_DATABASE_URI = "postgresql://{}@{}/{}".format(
    username, url, DATABSE_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
