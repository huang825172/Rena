#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/8 0008
# @Email : happy.huangyang@gmail.com

""" Framebuffer, string, point rendering facilities. """

import colorama

colorama.init(autoreset=True)


class Renderer:
    """
    Renderer instance.
    :param w: Framebuffer width
    :param h: Framebuffer height
    """

    def __init__(self, w: int, h: int):
        self.frame_width = w
        self.frame_height = h
        self.frame_buffer = [[[' ' for _ in range(h)] for _ in range(w)] for _ in range(2)]
        self.clear_color = 'WHITE'

    def _write_fb(self, x: int, y: int, content: str, front: bool = False):
        if 0 <= x < self.frame_width and 0 <= y < self.frame_height:
            self.frame_buffer[0 if front else 1][x][y] = content

    def paste_fb(self, x: int, y: int, renderer):
        """
        Paste clip of framebuffer from another renderer
        :param x:
        :param y:
        :param renderer:
        """
        if isinstance(renderer, Renderer):
            for i in range(x - 1, x - 1 + renderer.frame_width):
                for j in range(y - 1, y - 1 + renderer.frame_height):
                    self._write_fb(i, j, renderer.frame_buffer[1][i - x + 1][j - y + 1])

    def clear(self, color: str = 'WHITE'):
        """
        Clear back buffer.
        :param color: Clear color
        """
        if len(color) > 0:
            self.clear_color = color.upper()
        for x in range(self.frame_width):
            for y in range(self.frame_height):
                self._write_fb(x, y, getattr(colorama.Fore, self.clear_color) + u'\u2589')

    def point(self, x: int, y: int, color: str = 'red'):
        """
        Render a point to framebuffer.
        :param x: Render position x
        :param y: Render position y
        :param color: Point color
        """
        self._write_fb(x - 1, y - 1, getattr(colorama.Fore, color.upper()) + u'\u2589')

    def block(self, x: int, y: int, w: int, h: int, color: str = 'black'):
        """
        Render a block with pure color to framebuffer.
        :param x: Render position x
        :param y: Render position y
        :param w: Block width in character
        :param h: Block height in character
        :param color:
        """
        c = getattr(colorama.Fore, color.upper())
        for i in range(x - 1, x - 1 + w):
            for j in range(y - 1, y - 1 + h):
                self._write_fb(i, j, c + u'\u2589')

    def string(self, art: str, x: int, y: int, fore_color: str = 'black', back_color: str = ''):
        """
        Render ascii art to framebuffer.
        :param art: ASCII art string
        :param x: Render position x
        :param y: Render position y
        :param fore_color: Character color
        :param back_color: Background color
        """
        lines = art.split('\n')
        f_color = getattr(colorama.Fore, fore_color.upper()) if len(fore_color) > 0 else colorama.Fore.BLACK
        b_color = getattr(colorama.Back, self.clear_color)
        if len(back_color) > 0:
            b_color = getattr(colorama.Back, back_color.upper())
        for i in range(y - 1, y - 1 + len(lines)):
            for j in range(len(lines[i - y + 1])):
                self._write_fb(x - 1 + j, i, f_color + b_color + lines[i - y + 1][j])

    def swap_buffers(self, force: bool = False):
        """
        Swap and render front and back buffer and print to screen.
        :param force: Force reprint all screen
        """
        self.frame_buffer[0], self.frame_buffer[1] = self.frame_buffer[1], self.frame_buffer[0]
        for y in range(self.frame_height):
            for x in range(self.frame_width):
                if force:
                    print(colorama.Cursor.POS(x + 1, y + 1) + self.frame_buffer[0][x][y], end='')
                elif self.frame_buffer[0][x][y] != self.frame_buffer[1][x][y]:
                    print(colorama.Cursor.POS(x + 1, y + 1) + self.frame_buffer[0][x][y], end='')
        print(colorama.Cursor.POS(1, 1))
