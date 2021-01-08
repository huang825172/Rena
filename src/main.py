#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/8 0008
# @Email : happy.huangyang@gmail.com

""" Rena: The terminal Craft. """

import system
import render
import asset
import event
import input
from layout import LayoutManager
import control


class Rena:
    """
    Rena main class.
    """

    def __init__(self):
        self.done = False
        self.selection_label = None
        self._main()

    def _end(self, e: input.KeyEvent):
        if e.key == 'q':
            self.done = True

    def _update_selection(self, e: control.Select.SelectionChangeEvent):
        self.selection_label.text = e.selection

    def _main(self):
        screen_width = 80
        screen_height = 24
        system.resize(screen_width, screen_height)
        renderer = render.Renderer(screen_width, screen_height)
        layout_manager = LayoutManager(renderer)
        event_bus = event.EventBus()
        keyboard_input = input.KeyboardInput(event_bus)

        keyboard_input.hook('q')
        event_bus.on(input.KeyEvent, self._end)

        v = LayoutManager.Vertical(60, layout_manager.root_layout, margin_left=11, back_color='BLUE')
        h_logo = LayoutManager.Horizontal(13, v, margin_top=1, back_color='CYAN')
        h_menu = LayoutManager.Horizontal(3, v, margin_top=1, back_color='GREEN')
        h_blocks = LayoutManager.Horizontal(4, v, margin_top=1, back_color='RED')
        v_block1 = LayoutManager.Vertical(25, h_blocks, margin_right=5, back_color='GREEN')
        v_block2 = LayoutManager.Vertical(25, h_blocks, margin_left=5, back_color='CYAN')
        LayoutManager.Image(asset.logo, h_logo, 'WHITE')
        control.Select(['Option A', 'Option B', 'Option C'], h_menu,
                       keyboard_input, event_bus,
                       fore_color='WHITE', back_color='GREEN')
        self.selection_label = LayoutManager.Label('', v_block1, 'WHITE', 'GREEN')
        LayoutManager.Block(10, 2, v_block2, 'BLACK')

        event_bus.on(control.Select.SelectionChangeEvent, self._update_selection)

        while not self.done:
            renderer.clear()
            layout_manager.draw()
            renderer.swap_buffer()

        system.clear()


if __name__ == '__main__':
    Rena()
