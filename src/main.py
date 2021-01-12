#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/8 0008
# @Email : happy.huangyang@gmail.com

""" Rena: The terminal Craft. """
import asset
from rena import *


class Index(page.Page):
    """
    Index page
    """

    def __init__(self, name: str, w: int, h: int, event_bus: event.EventBus):
        super(Index, self).__init__(name, w, h, event_bus)

        self._selection_label = None
        self._layout()
        self._keyboard_input.hook('q')
        self._keyboard_input.hook('a')
        self._event_bus.on(control.Select.SelectionChangeEvent, self._on_selection_change)

    def _on_key(self, e: input.KeyEvent):
        if e.key == 'q' and e.action == 'down':
            self._event_bus.emit(page.RouteEvent(self.name, ''))
        if e.key == 'a' and e.action == 'down':
            self._event_bus.emit(page.RouteEvent(self.name, 'second'))

    def _on_selection_change(self, e: control.Select.SelectionChangeEvent):
        if e.control_name == 'Select1':
            self._selection_label.text = e.selection

    def _layout(self):
        v = LinearLayout.Vertical(60, self._layout_manager.root_layout,
                                  margin_left=11, back_color='BLUE')
        h_logo = LinearLayout.Horizontal(13, v, margin_top=1, back_color='CYAN')
        h_menu = LinearLayout.Horizontal(3, v, margin_top=1, back_color='GREEN')
        h_blocks = LinearLayout.Horizontal(4, v, margin_top=1, back_color='RED')
        v_block1 = LinearLayout.Vertical(25, h_blocks, margin_right=5, back_color='GREEN')
        v_block2 = LinearLayout.Vertical(25, h_blocks, margin_left=5, back_color='CYAN')
        LinearLayout.Image(asset.logo, h_logo, 'WHITE')
        control.Select(['Option A', 'Option B', 'Option C'], h_menu,
                       "Select1",
                       self._keyboard_input, self._event_bus,
                       fore_color='WHITE', back_color='GREEN').focus()
        self._selection_label = LinearLayout.Label('', v_block1, 'WHITE', 'GREEN')
        LinearLayout.Block(10, 2, v_block2, 'BLACK')


class SecondPage(page.Page):
    """
    Another page
    """

    def __init__(self, name: str, w: int, h: int, event_bus: event.EventBus):
        super(SecondPage, self).__init__(name, w, h, event_bus)
        self._keyboard_input.hook('e')
        self.logcat = Logcat('Second Page')

    def on_create(self):
        """
        Execute on page creation after __init__.
        """
        self.logcat.info('Second Page created.')

    def on_pause(self):
        """
        Execute on page switched to background.
        """
        self.logcat.info('Second Page paused.')

    def on_resume(self):
        """
        Execute on page switched to front ground.
        """
        self.logcat.info('Second Page resumed.')

    def _on_key(self, e: input.KeyEvent):
        if e.key == 'e' and e.action == 'down':
            self._event_bus.emit(page.RouteEvent(self.name, 'index'))


if __name__ == '__main__':
    app = Application('Rena', 80, 24)
    logcat = Logcat('Rena')
    logcat.info('Start')
    app.add_page(Index, 'index', is_index=True)
    app.add_page(SecondPage, 'second')
    app.run()
    logcat.close()
