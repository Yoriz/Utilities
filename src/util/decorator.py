'''
Created on 17 Apr 2013

@author: Dave Wilson
'''
import functools
import threading


def run_async(func):
    '''Decorates a method to run in a separate thread'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_hl = threading.Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl
    return wrapper
