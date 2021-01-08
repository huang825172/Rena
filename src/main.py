#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/8 0008
# @Email : happy.huangyang@gmail.com

""" Rena: The terminal Craft. """

import keyboard
import system
import render
import asset
import layout

screen_width = 80
screen_height = 24

if __name__ == '__main__':
    system.resize(screen_width, screen_height)
    renderer = render.Renderer(screen_width, screen_height)
    renderer.clear('BLACK')
    h = layout.Horizontal(screen_height)
    v = layout.Vertical(60, h, margin_left=11, back_color='BLUE')
    container = layout.Horizontal(15, v, margin_top=5, back_color='CYAN')
    layout.Image(asset.logo, container, 'WHITE')
    UI = layout.UI(h, renderer)
    UI.draw()
    renderer.point(1, 1)
    renderer.point(screen_width, screen_height)
    renderer.swap_buffer()
    while not keyboard.is_pressed('q'):
        pass
    system.clear()
