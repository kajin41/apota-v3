__author__ = 'Madness'

from json import JSONEncoder, JSONDecoder, loads
from datetime import datetime

from APP.models import User as ActiveUser #todo change all instances of active user to user
from flask import jsonify, request
from flask import abort, make_response

FILE_TAG = __name__


def check_authentication(req_roles=None, form_data=False):
    """

    :param req_roles: a list of roles
    :param form_data: a boolean, whether the data is wrapped in the request form or not
    :return:
    """
    # Try to get the user from the email provided and then check auth
    if not(request.form or request.data) and form_data is None:
        throw_error("No Auth Data!", 403, request, FILE_TAG)
    else:
        if form_data:
            # Support for multi-part forms
            # could build dict data and always pass
            data = form_data
        else:
            if request.data:
                data = loads(request.data.decode('utf-8'))
            else:
                data = request.form

    try:
        user = ActiveUser.objects.get_from_email(data['email'])
        if user is None:
            throw_error('No User with email: ' + data['email'], 404, request, FILE_TAG)

        # auth_with_token returns a tuple, (bool, new_token=None)
        auth = user.auth_with_token(data['token'])
        if not auth[0]:
            # If they are unauthenticated, send a 403 response back
            # telling them to log in again
            return False, None

        new_token = None
        if auth[1] is not None:
            new_token = auth[1]

    except KeyError:
        throw_error('Key Error!', 403, request, FILE_TAG)

    if req_roles is not None:
        user_roles = user.get_roles()
        # Check to make sure all required roles are had by user

        if 'admin' in req_roles and 'admin' not in user_roles:
            return False, new_token

        # 'admin' is allowed all access
        if 'admin' not in user_roles:
            passes = True
            for r in req_roles:
                # Check if a listed role is not in the user roles
                if r not in user_roles:
                    passes = False
            if not passes:
                return False, new_token

    return True, new_token


# FROM https://gist.github.com/abhinav-upadhyay/5300137 THANK YOU
class DateTimeEncoder(JSONEncoder):
    """ Instead of letting the default encoder convert datetime to string,
        convert datetime objects into a dict, which can be decoded by the
        DateTimeDecoder
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
            }
        else:
            return JSONEncoder.default(self, obj)


# Updated from original gist.
# Added a failure return if the conversion was unsuccessful
class DateTimeDecoder(JSONDecoder):

    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)

    def dict_to_object(self, data):
        decode_failed = "failure"
        if '__type__' not in data:
            return decode_failed

        if isinstance(data, dict):
            type = data.pop('__type__', None)
            try:
                dateobj = datetime(**data)
                return dateobj
            except:
                data['__type__'] = type
                return decode_failed

        return decode_failed

'''
    NOT OPTIONAL:
    message : string
    code: int
    OPTIONAL
    (in *args)
    [0] request: the request so we can try to pull these out
            origin : header field to further identify our error maker guy
            user-agent : ditto ^
    (in **kwargs)
    cls_tag : a tag denoting the file that the error came from
'''
def throw_error(message, code, request, tag, exception=None):
    from APP import DEBUG
    from mongoengine import ValidationError

    if exception is not None:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        template.format(type(exception).__name__, exception.args)
        exception = template

    try:
        # Save the hopefully more descriptive error
        #todo make error database log
        Error(
            message=message,
            code=code,
            url_request=request.base_url,
            remote_addr=request.environ['REMOTE_ADDR'],
            user_agent=request.user_agent.string,
            tag=tag,
            exception=exception
        ).save()
    except ValidationError:
        # Could also just create a new error here
        # Just aborts
        pass

    # Could potentially send out a push notification to a PALLET DEV channel
    # to notify us whenever an error happens
    # Only send the message back to the client if we are in a dev setting
    # NEVER IN PRODUCTION
    if DEBUG:
        abort(code, message)
    abort(code)


def make_returnable_error(message, code, request, tag, exception=None):
    from mongoengine import ValidationError

    if exception is not None:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        template.format(type(exception).__name__, exception.args)
        exception = template

    try:
        # Save the hopefully more descriptive error
        Error(
            message=message,
            code=code,
            url_request=request.base_url,
            remote_addr=request.environ['REMOTE_ADDR'],
            user_agent=request.user_agent.string,
            tag=tag,
            exception=exception
        ).save()
    except ValidationError:
        # Could also just create a new error here
        # Just aborts
        pass

    abort(code)


def log_error(message, tag, exception=None):
    if exception is not None:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        template.format(type(exception).__name__, exception.args)
        exception = template
    Error(message=message, tag=tag, exception=exception).save()


# should be used whenever successfully returning a request
# IF NOT: must make sure to check the new_auth_token_field
def make_gen_success(new_token=None):
    return make_response(jsonify(message="Great Success", new_token=new_token), 200)


def make_custom_response(message, code):
    return make_response(jsonify(message=message), code)

def remove_special_chars(string):
    special_chars = ['!', '#', '$', '%', '&', '*', '+', '-', '/', '=', '?', '^',
                         '_', '`', '{', '|', '}', '~', '.', '@', 'á', 'é', 'í', 'ó', 'ú',
                         'ü', 'ñ', '<', ' ', '>']
    for char in special_chars:
        string = string.replace(char, "")

    return string


# Accounts for a few common date formats, should add more
# Returns none if no date format is found
# Could create our own exception to alert if the format is super weird
def format_string_to_date(datestring):
    formats = [
        '%m/%d/%Y-%H:%M:%S',
        '%m/%d/%Y',
        '%Y-%m-%d-%H:%M:%S',
        '%Y-%m-%d',
    ]

    date = None
    for form in formats:
        try:
            date = datetime.strptime(datestring, form)
            break
        except ValueError:
            pass

    return date


def make_simple_random_string(num_chars):
    import random
    return ''.join(random.choice('0123456789qwertyuioplkjhgfdsazxcvbnm') for i in range(num_chars))


