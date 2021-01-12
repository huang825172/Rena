#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/8 0008
# @Email : happy.huangyang@gmail.com

""" Windows settings, input, etc. System dependence features. """

import os
import time
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


def start_python_console(file: str):
    """
    Start a python file in new console
    """
    if platform.system() == 'Windows':
        os.system('start python ' + file)
    time.sleep(0.5)
