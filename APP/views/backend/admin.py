__author__ = 'Madness'

from APP import app, bcrypt, SECRET_ADMIN_PASS, TEMP_MEDIA_FOLDER, DEBUG
from APP.models import User
from APP.utility import check_authentication, make_gen_success, throw_error, format_string_to_date

from flask import request, jsonify, abort, make_response, send_from_directory
from mongoengine import ValidationError
import json


FILE_TAG = __name__


# AUTHENTICATION REQUIRED
@app.route('/admin/shutdown', methods=['POST'])
def shutdown_server():
    ''' SHUTDOWN THE API
        A pretty simple endpoint, for admin functionality only
        Just sending an empty post request to this endpoint will quickly shut down the whole server
    '''
    auth = check_authentication(req_roles=['admin'])
    if not auth[0]:
        abort(403)

    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('No Werkzeug server is running..')
    shutdown_func()
    return jsonify(response='Shutting down the server!')



# Server fuctionalitiy
@app.route('/admin/mongo/update', methods=['GET', 'PUT'])
def update_to():
    """
        A simple endpoint just to run the updater script, as it needs
        the Flask context to run.
    :return:
    """

    # First check if the request is legit, check that password
    data = json.loads(request.data.decode('utf-8'))

    if data['admin_password'] != SECRET_ADMIN_PASS:
        throw_error('Incorrect password!', 403, request, FILE_TAG)

    from APP.mongoUpdater import run_updater
    run_updater()

    return make_gen_success()

