__author__ = 'Madness'

from APP import app
from APP.utility import make_gen_success


@app.route('/githook/push', methods=['POST'])
def git_push():
    # Todo make script to fetch new code and launch it from here
    # Will make a script to shutdown, pull, and restart the server
    return make_gen_success()
