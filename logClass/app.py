#!/usr/bin/python3


import functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper


class MyLog():
    def __init__(self):
        for name in dir(self):
            attr = getattr(self, name)
            if callable(attr) and not name.startswith('_'):
                setattr(self, name, log(attr))


class A(MyLog):
    def add(self, a, b):
        return a + b

if __name__ == '__main__':
    a = A()
    a.add(1, 2)
    a.add(3, 4)