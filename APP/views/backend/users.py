'''
use this to create endpoints for websockest in reference to users
'''
from APP import app
from APP.models import Semester, NMClass
from APP.utility import make_gen_success
import datetime


@app.route('/', methods=['GET'])
def root():
    return "success"


@app.route('/test/makeSemester', methods=['GET'])
def test_make_semester():
    print('request received')
    new_semester = Semester(
        semesterNumber=1,
        name='test',
        startDate=datetime.datetime.utcnow()
    ).save()
    print('save')
    return make_gen_success()
