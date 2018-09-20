#!/usr/bin/python

import sys
import os


def tree(path, prefix=''):
    more = '│  '
    files = os.listdir(path)
    for el in files:
        if files[-1] == el:
            print('%s└── %s' % (prefix, el))
            more = '   '
        else:
            print('%s├── %s' % (prefix, el))
        if os.path.isdir(os.path.join(path, el)):
            tree(os.path.join(path, el), prefix + more)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Need one arguments')
    else:
        path = sys.argv[1]
        if os.path.isdir(path):
            tree(path)
        else:
            print ('"%s" is not dir')