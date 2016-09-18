__author__ = 'Madness'

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from itsdangerous import URLSafeTimedSerializer

# APP
app = Flask(__name__)

'''
    Things to remember:
    When pushing to MASTER:
        - Make sure the servers are configured correctly below
        - Make sure the scripts are started in APO_v3.py, (transactionFinisher and fuelCrawler)
'''
APO_EMAIL = 'apo@stevens.edu'#todo add other apo emails
WEBMASTER_EMAIL = 'zmillard@stevens.edu'#todo use db lookup instead
# Configure

# PRODUCTION
# server = 'http://apota.org'
# DEBUG = False

# TESTING
server = 'http://apo-test.apotabig.com'
DEBUG = True



#LOCAL
# server = 'http://localhost:8000'
# DEBUG = True


SECRET_ADMIN_PASS = "thisisasecret" #todo generate random pass
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
    'username': '',
    'password': ''
}

#todo setup mail for stevens

# app.config['MAIL_SERVER'] = ''
# app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''


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

import APP.views.backend


# --- For Analytics

from flask import g
from datetime import datetime


@app.before_request
def init_request():
    g.start = datetime.utcnow()
    print('start')


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
