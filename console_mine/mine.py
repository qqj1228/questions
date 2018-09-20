#!/usr/bin/python3

import curses
import random

HEIGHT = 10
WIDTH = 10
MINEQTY = 15
# 分配所需长度+1的list，最后多出来的那个list元素用来表示超出棋盘范围的格子
g_mine_board = [0] * (HEIGHT * WIDTH + 1)
g_show_board = ['#'] * (HEIGHT * WIDTH + 1)
g_show_board[HEIGHT * WIDTH] = '9'


def to1d(cx, cy):
    if cx < 0 or cx >= WIDTH or cy < 0 or cy >= HEIGHT:
        return HEIGHT * WIDTH
    else:
        return cy * WIDTH + cx


# 返回[x, y]
def to2d(index):
    return [index % WIDTH, index // WIDTH]


def main(stdscr):
    init()
    stdscr.clear()

    # for j in range(0, HEIGHT):
    #     for i in range(0, WIDTH):
    #         stdscr.addstr(j, WIDTH + 22 + i, '%d' % g_mine_board[j * WIDTH + i])
    x = 4
    y = 4

    for cy in range(0, HEIGHT):
        for cx in range(0, WIDTH):
            stdscr.addstr(cy, cx, '%s' % g_show_board[to1d(cx, cy)])

    stdscr.addstr(0, WIDTH + 2, '# - 未挖部分')
    stdscr.addstr(1, WIDTH + 2, '  - 没有地雷')
    stdscr.addstr(2, WIDTH + 2, '1 - 周围雷数')
    stdscr.addstr(3, WIDTH + 2, '* - 地雷')
    stdscr.addstr(6, WIDTH + 2, '空格   - 挖雷')
    stdscr.addstr(7, WIDTH + 2, 'm      - 标记地雷')
    stdscr.addstr(8, WIDTH + 2, '方向键 - 移动光标')
    stdscr.move(y, x)
    stdscr.refresh()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_DOWN:
            y += 1
            y = y % HEIGHT
        elif c == curses.KEY_UP:
            y -= 1
            y = (y + HEIGHT) % HEIGHT
        elif c == curses.KEY_LEFT:
            x -= 1
            x = (x + WIDTH) % WIDTH
        elif c == curses.KEY_RIGHT:
            x += 1
            x = x % WIDTH
        elif c == ord('m'):
            g_show_board[to1d(x, y)] = '*'
        elif c == ord(' '):
            if scan(x, y) == -1:
                for i, v in enumerate(g_mine_board):
                    if v == 1:
                        point = to2d(i)
                        stdscr.addstr(point[1], point[0], '*', curses.A_REVERSE)
                stdscr.addstr(HEIGHT, 0, 'You Lost!', curses.A_REVERSE)
                break

        rest = 0
        for cy in range(0, HEIGHT):
            for cx in range(0, WIDTH):
                stdscr.addstr(cy, cx, '%s' % g_show_board[to1d(cx, cy)])
                if g_show_board[to1d(cx, cy)] == '#' or g_show_board[to1d(cx, cy)] == '*':
                    rest += 1
        if rest == MINEQTY:
            stdscr.addstr(HEIGHT, 0, 'You Win!', curses.A_REVERSE)
            break
        stdscr.move(y, x)
        stdscr.refresh()

    stdscr.getkey()


def init():
    mine = random.sample(range(0, HEIGHT * WIDTH), MINEQTY)
    for el in mine:
        g_mine_board[el] = 1


# 返回值代表当前格状态
# -1  - 触雷
#  0  - 无雷
# 1-8 - 周围格子雷数
def action(cx, cy):
    if g_mine_board[to1d(cx, cy)] == 1:
        return -1

    ret = g_mine_board[to1d(cx - 1, cy - 1)]   # 左上
    ret += g_mine_board[to1d(cx, cy - 1)]      # 上
    ret += g_mine_board[to1d(cx + 1, cy - 1)]  # 右上
    ret += g_mine_board[to1d(cx - 1, cy)]      # 左
    ret += g_mine_board[to1d(cx + 1, cy)]      # 右
    ret += g_mine_board[to1d(cx - 1, cy + 1)]  # 左下
    ret += g_mine_board[to1d(cx, cy + 1)]      # 下
    ret += g_mine_board[to1d(cx + 1, cy + 1)]  # 右下
    return ret


def scan(cx, cy):
    if g_show_board[to1d(cx, cy)] == '#':
        result = action(cx, cy)
        if result == 0:
            g_show_board[to1d(cx, cy)] = ' '
            scan(cx - 1, cy - 1)  # 左上
            scan(cx, cy - 1)      # 上
            scan(cx + 1, cy - 1)  # 右上
            scan(cx - 1, cy)      # 左
            scan(cx + 1, cy)      # 右
            scan(cx - 1, cy + 1)  # 左下
            scan(cx, cy + 1)      # 下
            scan(cx + 1, cy + 1)  # 右下
        elif result == -1:
            g_show_board[to1d(cx, cy)] = '*'
            return result
        else :
            g_show_board[to1d(cx, cy)] = '%d' % result
            return result


if __name__ == '__main__':
    curses.wrapper(main)
