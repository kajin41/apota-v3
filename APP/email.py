__author__ = 'Madness'

from APP import app, mail, UPLOAD_FOLDER, server as base_web_url, APO_EMAIL, WEBMASTER_EMAIL
from APP.decorators import async

from flask import render_template
from flask_mail import Message

FILE_TAG = __name__

''' Sends the message in the background from our teampallet@gmail.com account! Whopdedooda!
    Builds from Master Fran's email templates found in
'''
@async
def send_async_mail(message):
    with app.app_context():
        mail.send(message)

# ---- ADMIN STUFF ---- #


def make_generic_email(recipients, header, body, link_text=None, link_url=None):
    message = Message(
        header,
        sender=APO_EMAIL,
        recipients=recipients)
    message.html = render_template('baseEmail.html', header=header, message_body=body,
                                   button_text=link_text, button_link=link_url)
    return message


def make_admin_error_email(error_header, error_code, error_message, url, data):
    message = Message(
        error_header,
        sender=APO_EMAIL,
        recipients=[WEBMASTER_EMAIL])

    message_body = "We got an error: {error_code}. It came with this message: {error_message}. It " \
                   "came from this endpoint: {url}. It had this data: {data}. Either we fucked up or they " \
                   "fucked up. Either way it needs a fixin'. " \
                   "Sincerely," \
                   "APO_BOT_3.0".format(error_code=error_code, error_message=error_message, url=url, data=data)
    message.html = render_template('baseEmail.html', name="Dev", header='ALERT ALERT ALERT', message_body=message_body)
    return message


# ---- NOT ADMIN STUFF ---- #
# SECTION #