__author__ = 'Madness'

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

from datetime import timedelta

# APP
app = Flask(__name__)

'''
    Things to remember:
    When pushing to MASTER:
        - Make sure the servers are configured correctly below
        - Make sure the scripts are started in drunknado.py, (transactionFinisher and fuelCrawler)
'''

# Configure

# PRODUCTION
# server = 'http://apota.org'
# DEBUG = False

# TESTING
# server = 'http://apo-test.apotabig.com'
# DEBUG = True



#LOCAL
server = 'http://localhost:8000'
DEBUG = True

SECRET_KEY = 'f^%TF5%FR5rfT56%5rf5'
app.config["DEBUG"] = DEBUG
app.config["SECRET_KEY"] = SECRET_KEY
app.config['DEFAULT_PARSERS'] = [
    'flask.ext.api.parsers.JSONParser',
    'flask.ext.api.parsers.URLEncodedParser',
    'flask.ext.api.parsers.MultiPartParser'
]

app.config["MONGODB_SETTINGS"] = {
    'db': 'APO_v3-test',
    'username': 'Site',
    'password': 'ebe11ud8agwa6ee'
}

#todo setup mail for stevens

# app.config['MAIL_SERVER'] = 'email-smtp.us-east-1.amazonaws.com'
# app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = 'AKIAJSSEQ6O7BEJ7W5AA'
# app.config['MAIL_PASSWORD'] = 'ArZBV7LBOrPxpIN5Q7cnA+VSpXU3f4iQ9MsZZNIiQMaA'


# INITIALIZE THE GOODIES
# MONGO
mongo = MongoEngine(app)

# FOR HASHING / ENCRYPTING
serializer = URLSafeTimedSerializer(app.secret_key)
bcrypt = Bcrypt(app)

# EMAIL for some notifications
mail = Mail(app)



#todo generate new keys
# ---- GLOBALS ---- #

# PARSE PUSH NOTIFICATIONS
if DEBUG:
    PARSE_MASTER = 'f3dDAZzLf9DMzrr64jwFYGDXe3M6yQh0HdtezxUL'
    PARSE_APP_ID = 'k9ZfmNoqvfqARweaRKYJJbuPz9rPFM3aSp0o4Iye'
    PARSE_REST_KEY = 'ms5FQ2rRUWx0hOjrJvzj7u7piyhKP5R75NWfp0ir'
else:
    PARSE_MASTER = 'ev3sjvFeMRUxMEBwbJxa4srcAKONY4n9BMlWbYpI'
    PARSE_APP_ID = '6Uggb7M4Mz5Hqk2mXoSEy0CIEZwNBFx3beiA1elb'
    PARSE_REST_KEY = '6LtRGPnNMSJ7AspVDyfCckiF7OrokknhmX8x80W6'

# An easy place to keep our versions
# FOR TESTING on the one server, use the /api path to get to the api, separating it from /web


import os

# Make sure that file file uploads area exists!
try:
    os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/temp')
except FileExistsError:
    os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/temp'
TEMP_MEDIA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/temp'


# --- For Analytics

from flask import g
from datetime import datetime


@app.before_request
def init_request():
    g.start = datetime.utcnow()


@app.after_request
def track_request(response):
    """
        Takes the response thrown back by Flask
        This is here to add tracking
        Could potentially also add statistics to the the API response content
    :param response:
    :return:
    """


    request_time = datetime.utcnow() - g.start
    return response
