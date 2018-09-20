#!/usr/bin/python

import sys

g_dim = 0
g_board = [0] * g_dim * g_dim

def to1d(cx, cy):
    if cx < 0 or cx >= g_dim or cy < 0 or cy >= g_dim:
        return g_dim * g_dim
    else:
        return cy * g_dim + cx


# 返回[x, y]
def to2d(index):
    return [index % g_dim, index // g_dim]


def nineGrid(dim):
    print(g_dim)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Need one arguments')
    else:
        g_dim = int(sys.argv[1])
        nineGrid(g_dim)
