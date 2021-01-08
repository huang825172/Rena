#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/8 0008
# @Email : happy.huangyang@gmail.com

""" Windows settings, input, etc. """

import os
import platform


def resize(x: int, y: int):
    """
    Resize the terminal window.
    :param x: expected width in characters
    :param y: expected height in characters
    """
    if platform.system() == 'Windows':
        os.system('mode con: cols={} lines={}'.format(x, y))


def clear():
    """
    Clear terminal.
    """
    if platform.system() == 'Windows':
        os.system('cls')
