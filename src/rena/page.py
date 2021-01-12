#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/9 0009
# @Email : happy.huangyang@gmail.com

""" Page contains controls """

from rena import event
from rena import input
from rena import render
from rena import layout


class RouteEvent(event.Event):
    """
    Event triggers when routing.
    """

    def __init__(self, route_from: str, route_to: str):
        super(RouteEvent, self).__init__(self.__class__.__name__)
        self.route_from = route_from
        self.route_to = route_to


class Page:
    """
    Page instance
    :param name: Page name
    :param w: Page width in character
    :param h: Page height in character
    :param event_bus: Global EventBus
    """

    def __init__(self, name: str, w: int, h: int, event_bus: event.EventBus):
        self.name = name
        self.is_focus = False
        self._event_bus = event_bus
        self._event_bus.on(input.KeyEvent, self._on_key)
        self._keyboard_input = input.KeyboardInput(self._event_bus)
        self._renderer = render.Renderer(w, h)
        self._layout_manager = layout.LinearLayout(self._renderer)

    def _on_key(self, e: input.KeyEvent):
        pass

    def on_create(self):
        """
        Execute on page creation after __init__.
        """
        pass

    def on_pause(self):
        """
        Execute on page switched to background.
        """
        pass

    def on_resume(self):
        """
        Execute on page switched to front ground.
        """
        pass

    def on_destroy(self):
        """
        Execute on application ends.
        """
        pass

    def focus(self, is_focus: bool = True):
        """
        Set whether this page is focus.
        :param is_focus: Focus status
        """
        self.is_focus = is_focus
        self._keyboard_input.active(is_focus)

    def render(self, force: bool = False):
        """
        Render page to terminal.
        :param force: Force reprint all screen
        """
        self._renderer.clear()
        self._layout_manager.draw()
        self._renderer.swap_buffers(force)
