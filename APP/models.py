__author__ = 'Madness'

from datetime import datetime, timedelta

from APP import mongo, bcrypt, serializer
from APP.customQuerySets import EventQuery #todo other query sets created make sure this step gets documented

db = mongo

FILE_TAG = __name__

TOKEN_EXPIRATION = timedelta(minutes=15)#todo maybe define the token expiration in init

# ------------------------------------------- #
# --------- EMBEDDED DOCUMENTS -------------- #
# ------------------------------------------- #


class Answer(db.DynamicEmbeddedDocument):
    """
    Answers for Questions

    Child of Question
    Parent of none

    answer          - String
    userid          - User object
    lastModified    - DateTime
    """

    answer = db.StringField()
    user = db.ReferenceField('User', name='user')
    lastModified = db.DateTimeField(default=datetime.utcnow())


class Question(db.DynamicEmbeddedDocument):
    """
    Questions for Events

    Child of Event
    Parent of Answer

    question        - String
    answerType      - String
    answers         - list Answer object
    """

    question = db.StringField()
    answerType = db.StringField()
    answers = db.ListField(db.ReferenceField('Answer', name='answers'))



class Shift(db.DynamicEmbeddedDocument):
    """
    Shifts for Events

    Child of Event
    Parent of none

    eventId         - Event object
    dateStart       - DateTime
    dateEnd         - DateTime
    attendees       - list User object
    hours           - list Float
    hoursApproved   - Boolean
    isOpen            - Boolean
    """

    event = db.ReferenceField('Event', name='event')
    dateStart = db.DateTimeField()
    dateEnd = db.DateTimeField()
    attendees = db.ListField(db.ReferenceField('User', name='attendees'))
    hours = db.ListField(db.FloatField())
    hoursApproved = db.BooleanField(default=False)
    isOpen = db.BooleanField(default=True)


class BoardMember(db.DynamicEmbeddedDocument):
    """
    Executive or Minor board member
    """
    user = db.ReferenceField('User', name='user')
    position = db.StringField()


class NMClass(db.DynamicEmbeddedDocument):
    """
    NM Class document
    """
    number = db.IntField(required=True)
    name = db.StringField
    members = db.ListField(db.ReferenceField('User', name='members'))
    namesake = db.StringField()
    quizes = db.ListField(db.ReferenceField('Quiz', name='quizes'))


class Quiz(db.DynamicEmbeddedDocument):
    number = db.IntField(required=True)
    name = db.StringField()
    member = db.ReferenceField('User', name='member')
    score = db.IntField()
    dateTaken = db.DateTimeField()


class Comment(db.DynamicEmbeddedDocument):
    type = db.IntField(required=True)
    subject = db.StringField()
    body = db.StringField()
    dateSubmitted = db.DateTimeField(default=datetime.utcnow())
    dateDiscussed = db.DateTimeField()
    dateAddressed = db.DateTimeField()
    dateArchived = db.DateTimeField()
    submitter = db.ReferenceField('User', name='submitter')


class Committee(db.DynamicEmbeddedDocument):
    chairs = db.ListField(db.ReferenceField('User', name='chairs'))
    name = db.StringField()
    members = db.ListField(db.ReferenceField('User', name='members'))
    membersPassed = db.ListField(db.ReferenceField('User', name='membersPassed'))


class FTOPoints(db.DynamicEmbeddedDocument):
    event = db.ReferenceField('Event', name='event')
    points = db.IntField()
    comment = db.StringField()


class FSemester(db.DynamicEmbeddedDocument):
    semester = db.ReferenceField('Semester', name='semester')
    ftoPoints = FTOPoints
    membersAdded = db.ListField(db.ReferenceField('User', name='membersAdded'))
    head = db.ReferenceField('User', name='head')
    events = db.ListField(db.ReferenceField('Event', name='Events'))
    photos = db.ListField(db.ReferenceField('File', name='photos'))


class USemester(db.DynamicEmbeddedDocument):
    """
    Used as a way to keep track of a USER's semester
    information for each semester they participate in APO

    Child of USER
    Parent of none

    semester        - SEMESTER object
    statusDeclared  - INT
    statusAchieved  - INT
    fellowshipHours - float
    serviceHours    - float
    shifts          - list SHIFT object
    interviews      - list USER object
    committees      - list Comittee object
    comitteesPassed - list Comittee object
    dues            - DATE
    membershipPoints- list SHIFT object
    leadershipReqs  - list SHIFT object
    """
    semester = db.ReferenceField('Semester', name='semester')
    statusDeclared = db.IntField()
    statusAchieved = db.IntField()
    fellowshipHours = db.FloatField()
    serviceHours = db.FloatField()
    shifts = db.ListField(db.ReferenceField('Shift', name='shifts'), required=False)
    interviews = db.ListField(db.ReferenceField('User', name='interviews'), required=False)
    committees = db.ListField(db.ReferenceField('Committee', name='comimittees'), required=False)
    committeesPassed = db.ListField(db.ReferenceField('Committee', name='committeesPassed'), required=False)
    dues = db.DateTimeField(required=False)
    membershipPoints = db.ListField(db.ReferenceField('Shift', name='membershipPoints'), required=False)
    leadershipReqs = db.ListField(db.ReferenceField('Shift', name='leadershipReqs'), required=False)


# ------------------------------------------- #
# ---------------- Base Docs ---------------- #
# ------------------------------------------- #

class User(db.DynamicDocument):
    """
    User base object
    """
    #todo add pydoc outline to All Docs

    meta = {
        'collection': 'users_applied',
        'indexes':
            [
                'email'
                'curentStatus'
            ]
    }

    #Admin Fields
    last_login = db.DateTimeField(default=datetime.utcnow())
    last_request = db.DateTimeField(default=datetime.utcnow())
    approvedNicName = db.BooleanField(default=False)

    #Authentication
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(maz_length=255, required=True)
    auth_token = db.StringField(max_length=255, default="")
    roles = db.ListField(db.StringField(max_length=255), default=['NewMember'])

    #User Personal Info
    firstName = db.StringField(required=True, max_length=30)
    preferedName = db.StringField(required=True, max_length=30)
    lastName = db.StringField(required=True, max_length=30)
    middleName = db.StringField(required=True, max_length=30)
    birthdate = db.DateTimeField
    address = db.StringField(required=False, max_length=255)
    phone = db.StringField(required=False, min_length=10, max_length=10)
    altemail = db.EmailField(required=False)
    room = db.StringField(required=False, max_length=255)
    yearin = db.IntField(required=True)
    yearoutof = db.IntField(required=True)
    mailbox = db.IntField(required=False)
    shirtsize = db.IntField(required=True)
    major = db.StringField(required=False)
    greekOrg = db.IntField(required=False)

    #Apo stuff
    nmClass = db.ReferenceField('NMClass', name='NewMemberClass')
    nicName = db.StringField()
    photopath = db.ReferenceField('File', name='photo')
    APO_id = db.IntField()
    family = db.ReferenceField('Family', name='family')
    big = db.ReferenceField('User', name='big')
    littles = db.ListField(db.ReferenceField('User', name='littles'))
    semesters = db.ListField(db.ReferenceField('USemester', name='semesters'))


class Event(db.DynamicDocument):
    """
    event base document
    """
    #shift info
    name = db.StringField(required=True, max_length=255)
    eventType = db.IntField(required=True)
    creator = db.ReferenceField('User', name='creator')
    chairs = db.ListField(db.ReferenceField('User', name='chairs'))
    coChairs = db.ListField(db.ReferenceField('User', name='coChairs'))
    notes = db.StringField()
    location = db.StringField()
    approved = db.BooleanField(default=False)
    questions = db.ListField(db.ReferenceField('Question', name='questions'))
    shifts = db.ListField(db.ReferenceField('Shift', name='shifts'))

    #data info
    dateCreated = db.DateTimeField(default=datetime.utcnow())
    pastOccurrence = db.ReferenceField('Event', name='pastOccurrence')


class Semester(db.DynamicDocument):
    '''
    Semester Base Document
    '''

    meta = {'collection': 'semesters'}

    semesterNumber = db.IntField(required=True)
    name = db.StringField(required=True)
    startDate = db.DateTimeField(required=False)
    eBoard = db.ListField(db.ReferenceField('BoardMember', name='eboard'), default=[])
    minorBoard = db.ListField(db.ReferenceField('BoardMember', name='minorBoard'), default=[])
    nmClass = db.ReferenceField('NMClass', name='nmClass', required=False)
    comments = db.ListField(db.ReferenceField('Comment', name='comments'), default=[])
    committees = db.ListField(db.ReferenceField('Committee', name='committees'), default=[])
    events = db.ListField(db.ReferenceField('Event', name='events'), default=[])


class Family(db.DynamicDocument):
    name = db.StringField()
    members = db.ListField(db.ReferenceField('User', name='members'))
    semesters = db.ListField(db.ReferenceField('FSemester', name='semesters'))


class File(db.DynamicDocument):
    permission = db.IntField()
#    uploadDate = db.DateTimeField(datetime.utcnow())
#    modifiedDate = db.DateTimeField(datetime.utcnow())
    lastChangeBy = db.ReferenceField('User', name='lastChangedBy')
    link = db.StringField()



#todo add Asset documents



