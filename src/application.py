#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : huang825172
# @CreateAt : 2021/1/9 0009
# @Email : happy.huangyang@gmail.com

""" Terminal GUI application """

import event
import page
import system


class Application:
    """
    Application instance.
    :param name: Name of application
    :param screen_width: Terminal width in character
    :param screen_height: Terminal height in character
    """

    def __init__(self, name: str, screen_width: int, screen_height: int):
        self.name = name
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._event_bus = event.EventBus()
        self._event_bus.on(page.RouteEvent, self._on_route)
        self._pages = []
        self._current_page = None

    def _on_route(self, e: page.RouteEvent):
        if e.route_to == '':
            self._current_page.focus(False)
            self._current_page = None
        elif e.route_to != self._current_page.name:
            for p in self._pages:
                if p['page'].name == e.route_to:
                    self._current_page.focus(False)
                    self._current_page = p['page']
                    self._current_page.focus()
                    break

    def add_page(self, new_page: type, name: str, is_index: bool = False):
        """
        Add new page to application.
        :param new_page: Page class to add
        :param name: Page name
        :param is_index: Whether the page is index of the application
        """
        self._pages.append({
            'index': is_index,
            'page': new_page(name, self.screen_width, self.screen_height, self._event_bus)
        })

    def run(self):
        """
        Start application
        """
        for p in self._pages:
            if p['index']:
                self._current_page = p['page']
                self._current_page.focus()
                break
        system.resize(self.screen_width, self.screen_height)
        current_name = self._current_page.name
        while self._current_page is not None:
            if current_name == self._current_page.name:
                self._current_page.render()
            else:
                self._current_page.render(force=True)
                current_name = self._current_page.name
        system.clear()
