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

class USemester(db.DynamicEnbeddedDocument):
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
    semester = db.ObjectIdField()
    statusDeclared = db.IntField()
    statusAchieved = db.IntField()
    fellowshipHours = db.FloatField()
    serviceHours = db.FloatField()
    shifts = db.EmbeddedDocumentListField(Shift, required=False)
    interviews = db.ListField(db.ObjectIdField(), required=False)
    committees = db.EmbeddedDocumentListField(Committee, required=False)
    committeesPassed = db.EmbeddedDocumentListField(Committee, required=False)
    dues = db.DateTimeField(required=False)
    membershipPoints = db.EmbeddedDocumentListField(Shift, required=False)
    leadershipReqs = EmbeddedDocumentListField(Shift, required=False)


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
    answers = db.EmbeddedDocumentListField(Answer)


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
    userid = db.ObjectIdField()
    lastModified = db.DateTimeField(default=datetime.utcnow())


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

    eventId = db.ObjectIdField()
    dateStart = db.DateTimeField()
    dateEnd = db.DateTimeField()
    attendees = db.ListField(db.ObjectIdField())
    hours = db.ListField(db.FloatField())
    hoursApproved = db.BooleanField(default=False)
    isOpen = db.BooleanField(default=True)

#todo add other embeded docs


# ------------------------------------------- #
# ------------------ USER ------------------- #
# ------------------------------------------- #

class User(db.DynamicDocument):
    """
    User base object
    """
    #todo add pydoc outline to User

    meta = {
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
    pledgeClass = db.ObjectIdField()
    nicName = db.StringField()
    photopath = db.StringField()
    APO_id = db.IntField()
    family = db.ObjectIdField()
    big = db.ObjectIdField
    littles = db.ListField(db.ObjectIdField())
    semesters = db.EmbeddedDocumentListField(USemester)


class Event(db.DynamicDocument):
    """
    event base document
    """
    #shift info
    name = db.StringField(required=True, max_length=255)
    eventType = db.IntField(required=True)
    creator = db.ObjectIdField()
    chairs = db.ListField(db.ObjectIdField())
    coChair = db.ListField(db.ObjectField())
    notes = db.StringField()
    location = db.StringField()
    approved = db.BooleanField(default=False)
    questions = db.EmbeddedDocumentListField(Question)
    shifts = db.EmbeddedDocumentListField(Shift)

    #data info
    dateCreated = db.DateTimeField(default=datetime.utcnow())
    pastOccurrence = db.ObjectIdField()
#todo add other documents



