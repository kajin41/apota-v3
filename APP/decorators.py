__author__ = 'Madness'

FILE_TAG = __name__

from threading import Thread
import multiprocessing


def async(f):
    """
        Do in the background
        This is used for sending emails, when we want to split from the main App serving thread
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def multiprocess(f):
    def wrapper(*args, **kwargs):
        p = multiprocessing.Process(target=f, args=args, kwargs=kwargs)
        p.start()
    return wrapper
