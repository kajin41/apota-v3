'''
use this to create endpoints for websockest in reference to users
'''
from APP import app
from APP.models import User, NMClass
from APP.utility import make_gen_success
import datetime


@app.route('/test/makeUser', methods=['GET'])
def test_make_user():
    print('request received')
    new_user = User(

        #Authentication
        email = 'test@user.com',
        password = 'password',
        auth_token = 'authtoken',
        #User Personal Info
        firstName = 'Test',
        preferedName = 'T',
        lastName = 'User',
        middleName = '',
        birthdate = datetime.date.today(),
        address = '',
        phone = '',
        altemail = '',
        room = '',
        yearin = 4,
        yearoutof = 5,
        mailbox = 1300,
        shirtsize = 4,
        major = '',
        greekOrg = 0,

        #Apo stuff
        # nmClass = db.ReferenceField('NMClass', name='NewMemberClass'),
        # photopath = '',
        # APO_id = 1,
        # family = db.ReferenceField('Family', name='family'),
        # big = db.ReferenceField('User', name='big'),
        # littles = db.ListField(db.ReferenceField('User', name='littles')),
        # semesters = db.ListField(db.ReferenceField('USemester', name='semesters')),
    ).save()
    print('save')
    return new_user.to_json()
