'''
use this to create endpoints for websockest in reference to users
'''
from APP import app
from APP.models import Semester, NMClass
from APP.utility import make_gen_success
import datetime


@app.route('/test', methods=['GET'])
def root():
    return "success"


@app.route('/test/makeSemester', methods=['GET'])
def test_make_semester():
    new_semester = Semester(
        semesterNumber=2,
        name='test2',
        startDate=datetime.datetime.utcnow()
    ).save()
    return new_semester.to_json()
