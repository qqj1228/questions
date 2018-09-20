#!/usr/bin/env python

import functools
from inspect import signature
import time

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        bound = signature(func).bind(*args, **kw)
        argsList = []
        for k in bound.arguments.keys():
            arg = bound.arguments[k]
            if isinstance(arg, dict):
                for k1, v1 in arg.items():
                    if isinstance(v1, str):
                        argsList.append('%s="%s"' % (k1, v1))
                    else:
                        argsList.append('%s=%s' % (k1, v1))
            else:
                argsList.append('%s' % arg)
        strArgs = ', '.join(argsList)
        print('[%s] %s.%s(%s)' % (func.__self__.__class__.__bases__[0].__name__, func.__self__.__class__.__name__, func.__name__, strArgs))
        print('[Start] %s' % time.perf_counter())
        ret = func(*args, **kw)
        print('[ End ] %s' % time.perf_counter())
        print('[Result] %s' % ret)
        return func
    return wrapper


class MyLog():
    def __init__(self):
        for name in dir(self):
            attr = getattr(self, name)
            if callable(attr) and not name.startswith('__'):
                setattr(self, name, log(attr))


class Any(MyLog):
    def add(self, a, b, **kw):
        print('running...')
        return a + b


if __name__ == '__main__':
    any = Any()
    any.add(1, 2, k1='10')
    any.add(3, 4, k2=20)