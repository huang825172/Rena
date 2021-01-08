#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/9 0009
# @Email : happy.huangyang@gmail.com

""" Controls """

import event
import layout
import input


class Select:
    """
    Control for selecting in multiple choices.
    :param options: List of string representing options
    :param parent: Parent layout
    :param keyboard_input: Global instance for hooking keys
    :param event_bus: Global instance for responding to KeyEvents
    :param fore_color: Character color
    :param back_color: Background color
    """

    def __init__(self, options: list, parent: layout.Layout,
                 keyboard_input: input.KeyboardInput, event_bus: event.EventBus,
                 fore_color: str = 'black', back_color: str = ''):
        self.selection = 0
        self.root_layout = None
        self._layout = None
        self._options = options
        self._labels = []
        self._event_bus = event_bus

        w = max(map(len, options)) + 1
        if isinstance(parent, layout.LayoutManager.Vertical):
            self.root_layout = layout.LayoutManager.Horizontal(len(options), parent, back_color=back_color)
            self._layout = layout.LayoutManager.Vertical(w, self.root_layout, back_color=back_color)
        elif isinstance(parent, layout.LayoutManager.Horizontal):
            self.root_layout = layout.LayoutManager.Vertical(w, parent, back_color=back_color)
            self._layout = self.root_layout
        for o in self._options:
            h = layout.LayoutManager.Horizontal(1, self._layout, back_color=back_color)
            self._labels.append(layout.LayoutManager.Label(o, h, fore_color, back_color))
        self._select(0)

        keyboard_input.hook('w')
        keyboard_input.hook('s')
        self._event_bus.on(input.KeyEvent, self._select_event)

    def _select(self, i):
        self._create_selection_change_event()
        for j in range(len(self._options)):
            if j != i:
                self._labels[j].text = ' ' + self._options[j]
            else:
                self._labels[j].text = '>' + self._options[j]

    def _select_event(self, e: input.KeyEvent):
        if e.key == 'w' and e.action == 'down':
            self.selection -= 1
            if self.selection < 0:
                self.selection += len(self._options)
        if e.key == 's' and e.action == 'down':
            self.selection += 1
            self.selection %= len(self._options)
        self._select(self.selection)

    def _create_selection_change_event(self):
        self._event_bus.emit(Select.SelectionChangeEvent(self.selection, self._options[self.selection]))

    class SelectionChangeEvent(event.Event):
        """
        Event triggers on selection change.
        :param index: Index of selected element
        :param selection: Content of selected element
        """

        def __init__(self, index: int, selection: str):
            super(Select.SelectionChangeEvent, self).__init__("SelectionChangeEvent")
            self.index = index
            self.selection = selection
