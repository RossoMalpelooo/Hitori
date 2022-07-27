#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

import g2d
from boardgame import BoardGame
from time import time

LONG_PRESS = 0.5
SYMBOLS = [(10,10,81,81),(112,11,81,81),(222,10,81,81),(324,12,81,81),
           (11,109,81,81),(116,110,81,81),(218,112,81,81),(335,115,81,81),
           (456,116,81,81),(11,211,81,81),(115,209,81,81),(222,211,81,81),
           (332,213,81,81),(452,213,81,81),(14,319,81,81),(129,313,81,81),
           (235,315,81,81),(340,314,81,81),(443,312,81,81)]

MATRICES = ["hitori-12x12-29512.txt", "hitori-9x9-168142.txt", "hitori-6x6-16075.txt"]

IMAGE = g2d.load_image('animation.png')
MENU_IMAGE = g2d.load_image('menu.png')
LEVEL_IMAGE = g2d.load_image('levels.png')
INSTRUCTION_IMAGE = g2d.load_image('instruction.png')
WIN_IMAGE = g2d.load_image('wins.png')

X_RECT_LEVEL = 115
Y_RECT_LEVEL = 225
W_RECT_LEVEL = 250
H_RECT_LEVEL = 210

class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._menu = True
        self._instruction = False
        self._finished = False
        self._downtime = 0
        self.update_buttons()

    def tick(self):
        if self._menu:
            mx, my = g2d.mouse_position()
            if X_RECT_LEVEL < mx < X_RECT_LEVEL + W_RECT_LEVEL and Y_RECT_LEVEL < my < Y_RECT_LEVEL + H_RECT_LEVEL:
                if g2d.key_pressed("LeftButton"):
                    self._menu = False
                    self._instruction = True
        elif self._instruction and not self._menu:
            if g2d.key_pressed("Enter"):
                self._instruction = False
        else:
            if not(self._finished):
                if g2d.key_pressed("Escape"):
                    self._menu = True
                if g2d.key_pressed("LeftButton"):
                    self._downtime = time()
                elif g2d.key_released("LeftButton"):
                    mouse = g2d.mouse_position()
                    x, y = mouse[0] // self._dim, mouse[1] // self._dim
                    if time() - self._downtime > LONG_PRESS:
                        self._game.flag_at((x, y))
                    else:
                        self._game.play_at((x, y))
                if g2d.key_released("t") or g2d.key_released("T"):
                    self._game.tip()
                if g2d.key_released("x") or g2d.key_released("X"):
                    self._game.circle_around_black()
                    self._game.black_double()

        if self._game.finished():
            g2d.draw_image(WIN_IMAGE, (0, 0))
            return 0

        self.update_buttons()

    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()
        if self._menu:
            mx, my = g2d.mouse_position()
            g2d.draw_image(MENU_IMAGE, (0, 0, 480, 480))
            if X_RECT_LEVEL < mx < X_RECT_LEVEL + W_RECT_LEVEL and Y_RECT_LEVEL < my < Y_RECT_LEVEL + H_RECT_LEVEL:
                for i in range(0,H_RECT_LEVEL,H_RECT_LEVEL//3):
                    if Y_RECT_LEVEL + i < my < Y_RECT_LEVEL + i + H_RECT_LEVEL//3:
                        self._scelta = abs(i//70 - 2)
                        g2d.set_color((255, 0, 0))
                        g2d.fill_rect((X_RECT_LEVEL, Y_RECT_LEVEL+i, W_RECT_LEVEL, H_RECT_LEVEL//3))
            g2d.draw_image(LEVEL_IMAGE, (0, 220, 480, 215))
        elif self._instruction:
            self._game = BoardGame(MATRICES[self._scelta])
            g2d.draw_image(INSTRUCTION_IMAGE, (0, 0, 480, 480))
        else:
            self._dim = 480 // (12 - self._scelta*3)

            for y in range(1, rows):
                    g2d.draw_line((0, y * self._dim), (cols * self._dim, y * self._dim))
            for x in range(1, cols):
                g2d.draw_line((x * self._dim, 0), (x * self._dim, rows * self._dim))
            for y in range(rows):
                for x in range(cols):
                    value = self._game.value_at((x, y))
                    center = x * self._dim + self._dim // 2, y * self._dim + self._dim // 2
                    g2d.draw_text_centered(value, center, self._dim // 2)
                    if value[len(value) - 1] == '!':
                        g2d.draw_image_clip(IMAGE, SYMBOLS[self._game.symbols((x, y))],
                                            (x * self._dim + 2, y * self._dim + 2, self._dim - 3, self._dim - 3))
                        g2d.draw_text_centered(value[:-1], center, self._dim // 2)
                    elif value[len(value) - 1] == '#':
                        g2d.draw_text_centered(value, center, self._dim // 2)
                        g2d.fill_rect((x * self._dim, y * self._dim, self._dim, self._dim))

        g2d.update_canvas()

def gui_play(game: BoardGame):
    '''g2d.init_canvas((game.cols() * W, game.rows() * H))'''
    g2d.init_canvas((480, 480))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)
