#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/9 0009
# @Email : happy.huangyang@gmail.com

""" Controls """

from rena import event
from rena import layout
from rena import input


class Control:
    """
    Control base.
    :param parent: Parent layout
    :param name: Control name
    :param keyboard_input: Global instance for hooking keys
    :param event_bus: Global instance for responding to KeyEvents
    """

    def __init__(self, parent: layout.Layout,
                 name: str,
                 keyboard_input: input.KeyboardInput, event_bus: event.EventBus):
        self.name = name
        self.root_layout = None
        self.is_focus = False
        self._parent = parent
        self._keyboard_input = keyboard_input
        self._event_bus = event_bus

    def focus(self, is_focus: bool = True):
        """
        Set whether a control is focused.
        :param is_focus: Focus status
        """
        self.is_focus = is_focus

    class ControlEvent(event.Event):
        """
        Control event base.
        :param name: Name of event
        :param name: Name of control that emits the event
        """

        def __init__(self, name: str, control_name: str):
            super(Control.ControlEvent, self).__init__(name)
            self.control_name = control_name


class Select(Control):
    """
    Control for selecting in multiple choices.
    :param options: List of string representing options
    :param parent: Parent layout
    :param name: Control name
    :param keyboard_input: Global instance for hooking keys
    :param event_bus: Global instance for responding to KeyEvents
    :param fore_color: Character color
    :param back_color: Background color
    """

    def __init__(self, options: list, parent: layout.Layout,
                 name: str,
                 keyboard_input: input.KeyboardInput, event_bus: event.EventBus,
                 fore_color: str = 'black', back_color: str = ''):
        super(Select, self).__init__(parent, name, keyboard_input, event_bus)

        self.selection = 0
        self._layout = None
        self._options = options
        self._labels = []

        w = max(map(len, options)) + 1
        if isinstance(parent, layout.LinearLayout.Vertical):
            self.root_layout = layout.LinearLayout.Horizontal(len(options), parent, back_color=back_color)
            self._layout = layout.LinearLayout.Vertical(w, self.root_layout, back_color=back_color)
        elif isinstance(parent, layout.LinearLayout.Horizontal):
            self.root_layout = layout.LinearLayout.Vertical(w, parent, back_color=back_color)
            self._layout = self.root_layout
        for o in self._options:
            h = layout.LinearLayout.Horizontal(1, self._layout, back_color=back_color)
            self._labels.append(layout.LinearLayout.Label(o, h, fore_color, back_color))
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
        if self.is_focus:
            if e.key == 'w' and e.action == 'down':
                self.selection -= 1
                if self.selection < 0:
                    self.selection += len(self._options)
            if e.key == 's' and e.action == 'down':
                self.selection += 1
                self.selection %= len(self._options)
            self._select(self.selection)

    def _create_selection_change_event(self):
        self._event_bus.emit(Select.SelectionChangeEvent(self.name, self.selection, self._options[self.selection]))

    class SelectionChangeEvent(Control.ControlEvent):
        """
        Event triggers on selection change.
        :param control_name: Name of the emit control
        :param index: Index of selected element
        :param selection: Content of selected element
        """

        def __init__(self, control_name: str, index: int, selection: str):
            super(Select.SelectionChangeEvent, self).__init__(self.__class__.__name__, control_name)
            self.index = index
            self.selection = selection
