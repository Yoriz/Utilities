'''
Created on 17 Apr 2013

@author: Dave Wilson
'''
from functools import wraps
from threading import Thread


def runAsync(func):
    '''Decorates a method to run in a separate thread'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl
    return wrapper
